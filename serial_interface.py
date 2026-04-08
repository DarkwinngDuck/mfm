"""Abstract interface for serial communication."""

from abc import ABC, abstractmethod
from typing import Protocol


class SerialReader(Protocol):
    """Interface for reading from serial port."""

    def readline(self) -> bytes:
        """Read a line from the serial port."""
        ...

    def flushInput(self) -> None:
        """Clear input buffer."""
        ...


class SerialWriter(Protocol):
    """Interface for writing to serial port."""

    def write(self, data: bytes) -> int:
        """Write data to the serial port."""
        ...

    def flushOutput(self) -> None:
        """Clear output buffer."""
        ...


class SerialPort(SerialReader, SerialWriter, Protocol):
    """Combined interface for serial port communication."""

    def open(self) -> None:
        """Open the serial port."""
        ...

    def close(self) -> None:
        """Close the serial port."""
        ...


class BaseSerialDevice(ABC):
    """Abstract base class for serial devices.

    Provides common serial communication functionality while
    allowing concrete implementations for real hardware and mocks.
    """

    def __init__(self, port: SerialPort):
        """Initialize device with a serial port.

        Args:
            port: SerialPort implementation for communication.
        """
        self._port = port

    def open(self) -> None:
        """Open the serial connection."""
        self._port.open()

    def close(self) -> None:
        """Close the serial connection."""
        self._port.close()

    def _write(self, data: bytes) -> int:
        """Write bytes to the serial port.

        Args:
            data: Bytes to write.

        Returns:
            Number of bytes written.
        """
        return self._port.write(data)

    def _readline(self) -> bytes:
        """Read a line from the serial port.

        Returns:
            Bytes read from the port.
        """
        return self._port.readline()

    def _flush_input(self) -> None:
        """Clear the input buffer."""
        self._port.flushInput()

    def _flush_output(self) -> None:
        """Clear the output buffer."""
        self._port.flushOutput()
