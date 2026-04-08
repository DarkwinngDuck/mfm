"""Real serial port implementation using pyserial."""

from typing import Optional

import serial
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

from config import SerialConfig


class RealSerialPort:
    """Real serial port implementation using pyserial library.

    Implements the SerialPort Protocol for actual hardware communication.
    """

    def __init__(self, config: SerialConfig):
        """Initialize serial port configuration.

        Args:
            config: SerialConfig with port and communication settings.
        """
        self._config = config
        self._connection: Optional[serial.Serial] = None

    def open(self) -> None:
        """Open the serial port connection."""
        self._connection = serial.Serial(
            port=self._config.port,
            baudrate=self._config.baudrate,
            timeout=self._config.timeout,
            bytesize=self._config.bytesize,
            parity=self._config.parity,
            stopbits=self._config.stopbits,
        )

    def close(self) -> None:
        """Close the serial port connection."""
        if self._connection and self._connection.is_open:
            self._connection.close()
            self._connection = None

    def write(self, data: bytes) -> int:
        """Write bytes to the serial port.

        Args:
            data: Bytes to write.

        Returns:
            Number of bytes written.

        Raises:
            RuntimeError: If port is not open.
        """
        if not self._connection or not self._connection.is_open:
            raise RuntimeError("Serial port is not open")
        return self._connection.write(data)

    def readline(self) -> bytes:
        """Read a line from the serial port.

        Returns:
            Bytes read from the port.

        Raises:
            RuntimeError: If port is not open.
        """
        if not self._connection or not self._connection.is_open:
            raise RuntimeError("Serial port is not open")
        return self._connection.readline()

    def flushInput(self) -> None:
        """Clear the input buffer."""
        if self._connection and self._connection.is_open:
            self._connection.reset_input_buffer()

    def flushOutput(self) -> None:
        """Clear the output buffer."""
        if self._connection and self._connection.is_open:
            self._connection.reset_output_buffer()
