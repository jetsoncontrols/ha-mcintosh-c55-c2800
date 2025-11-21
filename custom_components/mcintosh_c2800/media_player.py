"""Media player platform for McIntosh C2800."""
from __future__ import annotations

import logging

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, INPUT_SOURCES
from .coordinator import McIntoshC2800Coordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the McIntosh C2800 media player."""
    coordinator: McIntoshC2800Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([McIntoshC2800MediaPlayer(coordinator, entry)])


class McIntoshC2800MediaPlayer(CoordinatorEntity, MediaPlayerEntity):
    """Representation of a McIntosh C2800 media player."""

    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(
        self,
        coordinator: McIntoshC2800Coordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the media player."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_media_player"
        self._attr_name = f"McIntosh C2800 ({entry.data[CONF_HOST]})"
        self._attr_source_list = INPUT_SOURCES

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.client.connected

    @property
    def state(self) -> MediaPlayerState:
        """Return the state of the device."""
        if not self.coordinator.client.connected:
            return MediaPlayerState.OFF

        if self.coordinator.data and self.coordinator.data.get("power"):
            return MediaPlayerState.ON

        return MediaPlayerState.OFF

    @property
    def volume_level(self) -> float | None:
        """Volume level of the media player (0..1)."""
        if self.coordinator.data:
            volume = self.coordinator.data.get("volume", 0)
            return volume / 100.0
        return None

    @property
    def is_volume_muted(self) -> bool | None:
        """Boolean if volume is currently muted."""
        if self.coordinator.data:
            return self.coordinator.data.get("muted", False)
        return None

    @property
    def source(self) -> str | None:
        """Return the current input source."""
        if self.coordinator.data:
            return self.coordinator.data.get("source")
        return None

    async def async_turn_on(self) -> None:
        """Turn the media player on."""
        await self.coordinator.client.power_on()

    async def async_turn_off(self) -> None:
        """Turn the media player off."""
        await self.coordinator.client.power_off()

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        volume_percent = int(volume * 100)
        await self.coordinator.client.set_volume(volume_percent)

    async def async_volume_up(self) -> None:
        """Volume up the media player."""
        await self.coordinator.client.volume_up()

    async def async_volume_down(self) -> None:
        """Volume down the media player."""
        await self.coordinator.client.volume_down()

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        if mute:
            await self.coordinator.client.mute_on()
        else:
            await self.coordinator.client.mute_off()

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        await self.coordinator.client.select_source(source)
