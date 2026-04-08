"""Gaussmeter device for magnetic field measurement."""

from typing import Callable, Optional, Protocol

from serial_interface import BaseSerialDevice, SerialPort
from commands import GaussmeterCommand


class MagneticFieldParser(Protocol):
    """Protocol for parsing magnetic field readings."""

    def parse(self, response: bytes) -> float:
        """Parse response bytes into magnetic field value.

        Args:
            response: Raw response from device.

        Returns:
            Magnetic field value as float.
        """
        ...


class SimpleFloatParser:
    """Simple parser that extracts float from response."""

    def parse(self, response: bytes) -> float:
        """Parse float from response string.

        Args:
            response: Raw response bytes.

        Returns:
            Parsed float value.

        Raises:
            ValueError: If response cannot be parsed.
        """
        text = response.decode().rstrip("\n\r")
        return float(text)


class Gaussmeter(BaseSerialDevice):
    """Gaussmeter for measuring magnetic field strength.

    Sends measurement commands and parses responses.
    """

    def __init__(
        self,
        port: SerialPort,
        parser: Optional[MagneticFieldParser] = None,
        command_callback: Optional[Callable[[str], None]] = None,
    ):
        """Initialize gaussmeter.

        Args:
            port: SerialPort implementation for communication.
            parser: Strategy for parsing responses.
            command_callback: Optional callback for logging commands.
        """
        super().__init__(port=port)
        self._parser = parser or SimpleFloatParser()
        self._command_callback = command_callback or self._noop

    @staticmethod
    def _noop(*args, **kwargs) -> None:
        """No-op callback."""
        pass

    def get_magnetic_field(self) -> float:
        """Measure magnetic field.

        Sends measurement command and parses response.

        Returns:
            Magnetic field value. Units depend on device configuration.

        Raises:
            ValueError: If response cannot be parsed.
        """
        command = GaussmeterCommand.MEASURE.value
        self._command_callback(f"Sending measurement command: {command!r}")

        self._flush_input()
        self._flush_output()
        self._write(command.encode())
        response = self._readline()

        return self._parser.parse(response)
