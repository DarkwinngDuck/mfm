"""Device lifecycle management."""

from typing import ContextManager, List, Optional, TypeVar

from serial_interface import BaseSerialDevice, SerialPort
from config import SerialConfig
from serial_impl import RealSerialPort


T = TypeVar("T", bound=BaseSerialDevice)


class DeviceManager:
    """Manages device creation and lifecycle.

    Provides context manager for automatic open/close handling.
    """

    def __init__(self):
        """Initialize device manager."""
        self._open_devices: List[BaseSerialDevice] = []

    def create_serial_port(self, config: SerialConfig) -> SerialPort:
        """Create a real serial port from configuration.

        Args:
            config: SerialConfig with connection parameters.

        Returns:
            RealSerialPort instance.
        """
        return RealSerialPort(config)

    def open_device(self, device: BaseSerialDevice) -> BaseSerialDevice:
        """Open a device and track it for later cleanup.

        Args:
            device: Device to open.

        Returns:
            The opened device.
        """
        device.open()
        self._open_devices.append(device)
        return device

    def close_device(self, device: BaseSerialDevice) -> None:
        """Close a device and remove from tracking.

        Args:
            device: Device to close.
        """
        device.close()
        if device in self._open_devices:
            self._open_devices.remove(device)

    def close_all(self) -> None:
        """Close all tracked devices."""
        for device in list(self._open_devices):
            try:
                device.close()
            except Exception:
                pass
        self._open_devices.clear()

    def managed_device(
        self, device: BaseSerialDevice
    ) -> ContextManager[BaseSerialDevice]:
        """Create a context manager for device lifecycle.

        Args:
            device: Device to manage.

        Returns:
            ContextManager that opens on enter and closes on exit.
        """
        return _DeviceContext(self, device)


class _DeviceContext:
    """Context manager for device lifecycle."""

    def __init__(self, manager: DeviceManager, device: BaseSerialDevice):
        self._manager = manager
        self._device = device

    def __enter__(self) -> BaseSerialDevice:
        self._manager.open_device(self._device)
        return self._device

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._manager.close_device(self._device)
