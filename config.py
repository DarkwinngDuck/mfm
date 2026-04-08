"""Configuration loading and environment setup."""

import os
from dataclasses import dataclass

from dotenv import dotenv_values

from constants import DEFAULT_BAUDRATE, DEFAULT_TIMEOUT


def load_environment(env_file: str = ".env") -> None:
    """Load environment variables from file.

    Args:
        env_file: Path to the environment file.
    """
    os.environ.update(dotenv_values(env_file))


@dataclass
class SerialConfig:
    """Configuration for serial device connection.

    Attributes:
        port: Serial port identifier (e.g., '/dev/ttyUSB0', 'COM1').
        baudrate: Communication speed in bits per second.
        timeout: Read timeout in seconds.
        bytesize: Number of bits per byte.
        parity: Parity checking mode.
        stopbits: Number of stop bits.
    """

    port: str
    baudrate: int = DEFAULT_BAUDRATE
    timeout: float = DEFAULT_TIMEOUT
    bytesize: int = 8
    parity: str = "N"
    stopbits: int = 1

    @classmethod
    def from_env(cls, port_env_var: str, baudrate_env_var: str) -> "SerialConfig":
        """Create config from environment variables.

        Args:
            port_env_var: Name of environment variable for port.
            baudrate_env_var: Name of environment variable for baudrate.

        Returns:
            SerialConfig instance with values from environment.
        """
        port = os.getenv(port_env_var)
        baudrate = int(os.environ.get(baudrate_env_var, DEFAULT_BAUDRATE))
        timeout = float(os.environ.get("DEFAULT_TIMEOUT", DEFAULT_TIMEOUT))

        return cls(port=port, baudrate=baudrate, timeout=timeout)


def create_printer_config() -> SerialConfig:
    """Create configuration for printer device.

    Returns:
        SerialConfig for printer connection.
    """
    return SerialConfig.from_env("PRINTER_PORT", "PRINTER_BAUDRATE")


def create_gaussmeter_config() -> SerialConfig:
    """Create configuration for gaussmeter device.

    Returns:
        SerialConfig for gaussmeter connection.
    """
    return SerialConfig.from_env("GAUSSMETER_PORT", "GAUSSMETER_BAUDRATE")
