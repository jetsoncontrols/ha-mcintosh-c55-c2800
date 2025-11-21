"""Data coordinator for McIntosh C2800."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .client import McIntoshC2800Client
from .const import DOMAIN, RECONNECT_DELAY

_LOGGER = logging.getLogger(__name__)


class McIntoshC2800Coordinator(DataUpdateCoordinator):
    """Coordinator to manage McIntosh C2800 updates."""

    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.client = McIntoshC2800Client(
            host=host,
            port=port,
            status_callback=self._handle_status_update,
        )
        self._reconnect_task: asyncio.Task | None = None
        self._should_reconnect = True

    async def _async_update_data(self):
        """Fetch data from the device."""
        if not self.client.connected:
            # Try to connect if not connected
            if not await self.client.connect():
                raise UpdateFailed("Not connected to device")
        
        # Query status
        if not await self.client.query_status():
            raise UpdateFailed("Failed to query device status")
        
        return {
            "power": self.client.power,
            "volume": self.client.volume,
            "muted": self.client.is_muted,
            "source": self.client.source,
        }

    def _handle_status_update(self):
        """Handle status update from client."""
        if not self.client.connected:
            # Connection lost, schedule reconnection
            _LOGGER.warning("Connection lost, will attempt to reconnect")
            self._schedule_reconnect()
        else:
            # Update Home Assistant with new data (this is thread-safe in Home Assistant)
            self.hass.loop.call_soon_threadsafe(
                self.async_set_updated_data,
                {
                    "power": self.client.power,
                    "volume": self.client.volume,
                    "muted": self.client.is_muted,
                    "source": self.client.source,
                }
            )

    def _schedule_reconnect(self):
        """Schedule a reconnection attempt."""
        if self._reconnect_task and not self._reconnect_task.done():
            return  # Already scheduled
        
        if not self._should_reconnect:
            return
        
        self._reconnect_task = asyncio.create_task(self._reconnect_loop())

    async def _reconnect_loop(self):
        """Reconnection loop."""
        while self._should_reconnect and not self.client.connected:
            _LOGGER.info("Attempting to reconnect in %s seconds", RECONNECT_DELAY)
            await asyncio.sleep(RECONNECT_DELAY)
            
            try:
                if await self.client.connect():
                    _LOGGER.info("Reconnected successfully")
                    # Query initial status after reconnection
                    await self.client.query_status()
                    self._handle_status_update()
                    break
            except Exception as err:
                _LOGGER.error("Reconnection failed: %s", err)

    async def async_shutdown(self):
        """Shutdown the coordinator."""
        self._should_reconnect = False
        
        if self._reconnect_task:
            self._reconnect_task.cancel()
            try:
                await self._reconnect_task
            except asyncio.CancelledError:
                pass
        
        await self.client.disconnect()
