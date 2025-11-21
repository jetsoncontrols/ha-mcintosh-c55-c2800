"""McIntosh C2800 TCP client."""
from __future__ import annotations

import asyncio
import logging
from typing import Callable

from .const import COMMAND_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class McIntoshC2800Client:
    """TCP client for McIntosh C2800 preamplifier."""

    def __init__(self, host: str, port: int, status_callback: Callable | None = None):
        """Initialize the client."""
        self.host = host
        self.port = port
        self._status_callback = status_callback
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._read_task: asyncio.Task | None = None
        self._connected = False
        self._lock = asyncio.Lock()
        
        # Current state
        self._power = False
        self._volume = 0
        self._muted = False
        self._source = None

    @property
    def connected(self) -> bool:
        """Return connection status."""
        return self._connected

    async def connect(self) -> bool:
        """Connect to the device."""
        try:
            _LOGGER.debug("Connecting to %s:%s", self.host, self.port)
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=COMMAND_TIMEOUT,
            )
            self._connected = True
            _LOGGER.info("Connected to McIntosh C2800 at %s:%s", self.host, self.port)
            
            # Start background task to read responses
            self._read_task = asyncio.create_task(self._read_responses())
            
            return True
        except (asyncio.TimeoutError, OSError, ConnectionError) as err:
            _LOGGER.error("Failed to connect to %s:%s: %s", self.host, self.port, err)
            self._connected = False
            return False

    async def disconnect(self):
        """Disconnect from the device."""
        self._connected = False
        
        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass
            self._read_task = None
        
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception as err:
                _LOGGER.debug("Error closing connection: %s", err)
            finally:
                self._writer = None
                self._reader = None

    async def _read_responses(self):
        """Background task to read responses from the device."""
        try:
            while self._connected and self._reader:
                try:
                    line = await self._reader.readuntil(b'\r\n')
                    response = line.decode('ascii').strip()
                    if response:
                        _LOGGER.debug("Received: %s", response)
                        self._parse_response(response)
                except asyncio.IncompleteReadError:
                    _LOGGER.warning("Connection closed by device")
                    break
                except Exception as err:
                    _LOGGER.error("Error reading response: %s", err)
                    break
        except asyncio.CancelledError:
            pass
        finally:
            self._connected = False
            if self._status_callback:
                self._status_callback()

    def _parse_response(self, response: str):
        """Parse a response from the device."""
        parts = response.split()
        if not parts:
            return
        
        command = parts[0].upper()
        
        try:
            if command == "PWR":
                if len(parts) > 1:
                    self._power = parts[1] == "1"
                    if self._status_callback:
                        self._status_callback()
            elif command == "VOL":
                if len(parts) > 1:
                    self._volume = int(parts[1])
                    if self._status_callback:
                        self._status_callback()
            elif command == "MUT":
                if len(parts) > 1:
                    self._muted = parts[1] == "1"
                    if self._status_callback:
                        self._status_callback()
            elif command == "INP":
                if len(parts) > 1:
                    self._source = " ".join(parts[1:])
                    if self._status_callback:
                        self._status_callback()
        except (ValueError, IndexError) as err:
            _LOGGER.debug("Error parsing response '%s': %s", response, err)

    async def _send_command(self, command: str) -> bool:
        """Send a command to the device."""
        if not self._connected or not self._writer:
            _LOGGER.warning("Not connected, cannot send command: %s", command)
            return False
        
        async with self._lock:
            try:
                _LOGGER.debug("Sending command: %s", command)
                self._writer.write(f"{command}\r\n".encode('ascii'))
                await self._writer.drain()
                return True
            except Exception as err:
                _LOGGER.error("Error sending command '%s': %s", command, err)
                self._connected = False
                return False

    async def power_on(self) -> bool:
        """Turn the device on."""
        return await self._send_command("PWR 1")

    async def power_off(self) -> bool:
        """Turn the device off."""
        return await self._send_command("PWR 0")

    async def set_volume(self, volume: int) -> bool:
        """Set volume (0-100)."""
        if 0 <= volume <= 100:
            return await self._send_command(f"VOL {volume}")
        return False

    async def volume_up(self) -> bool:
        """Increase volume by 1%."""
        return await self._send_command("VOL U")

    async def volume_down(self) -> bool:
        """Decrease volume by 1%."""
        return await self._send_command("VOL D")

    async def mute_on(self) -> bool:
        """Mute the device."""
        return await self._send_command("MUT 1")

    async def mute_off(self) -> bool:
        """Unmute the device."""
        return await self._send_command("MUT 0")

    async def select_source(self, source: str) -> bool:
        """Select input source."""
        return await self._send_command(f"INP {source}")

    async def query_status(self) -> bool:
        """Query current status."""
        # Query all status
        commands = ["PWR", "VOL", "MUT", "INP"]
        success = True
        for cmd in commands:
            if not await self._send_command(cmd):
                success = False
        return success

    @property
    def power(self) -> bool:
        """Return power state."""
        return self._power

    @property
    def volume(self) -> int:
        """Return current volume (0-100)."""
        return self._volume

    @property
    def is_muted(self) -> bool:
        """Return mute state."""
        return self._muted

    @property
    def source(self) -> str | None:
        """Return current source."""
        return self._source
