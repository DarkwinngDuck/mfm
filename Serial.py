"""Legacy Serial class - deprecated.

This module is kept for backward compatibility.
Use serial_interface.BaseSerialDevice with serial_impl.RealSerialPort
or serial_mock.MockSerialPort instead.
"""

from serial_interface import BaseSerialDevice
from serial_mock import MockSerialPort


class Serial(BaseSerialDevice):
    """Legacy Serial class using mock port.

    Deprecated: Use BaseSerialDevice with explicit port implementation.
    """

    def __init__(self, port, baudrate, timeout):
        """Initialize with mock serial port.

        Args:
            port: Port identifier (used for mock).
            baudrate: Baud rate (used for mock).
            timeout: Timeout in seconds (used for mock).
        """
        mock_port = MockSerialPort(port=port, baudrate=baudrate, timeout=timeout)
        super().__init__(port=mock_port)
