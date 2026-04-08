"""Mock serial port for testing."""

from typing import Callable, List, Optional


class MockSerialPort:
    """Mock serial port for testing without hardware.

    Implements the SerialPort Protocol with configurable behavior.
    """

    def __init__(
        self,
        port: str = "/dev/mock",
        baudrate: int = 9600,
        timeout: float = 1.0,
        response_generator: Optional[Callable[[], bytes]] = None,
    ):
        """Initialize mock serial port.

        Args:
            port: Mock port identifier (for compatibility).
            baudrate: Mock baudrate (for compatibility).
            timeout: Mock timeout (for compatibility).
            response_generator: Optional callable that returns responses.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._response_generator = response_generator or self._default_response
        self._is_open = False
        self._written_data: List[bytes] = []

    def _default_response(self) -> bytes:
        """Default response generator returns 'ok'."""
        return b"ok"

    def open(self) -> None:
        """Open the mock serial port."""
        self._is_open = True
        print(f"MockSerialPort: opened {self.port}")

    def close(self) -> None:
        """Close the mock serial port."""
        self._is_open = False
        print(f"MockSerialPort: closed {self.port}")

    def write(self, data: bytes) -> int:
        """Record written data and return byte count.

        Args:
            data: Bytes to write.

        Returns:
            Number of bytes written.
        """
        self._written_data.append(data)
        print(f"MockSerialPort: write {data!r}")
        return len(data)

    def readline(self) -> bytes:
        """Return a response from the generator.

        Returns:
            Response bytes.
        """
        response = self._response_generator()
        print(f"MockSerialPort: readline -> {response!r}")
        return response

    def flushInput(self) -> None:
        """Clear input buffer (no-op for mock)."""
        print("MockSerialPort: flushInput")

    def flushOutput(self) -> None:
        """Clear output buffer (no-op for mock)."""
        print("MockSerialPort: flushOutput")

    @property
    def is_open(self) -> bool:
        """Check if port is open."""
        return self._is_open

    def get_written_data(self) -> List[bytes]:
        """Get all data that was written.

        Returns:
            List of bytes that were written.
        """
        return self._written_data.copy()

    def set_response_generator(self, generator: Callable[[], bytes]) -> None:
        """Set a custom response generator.

        Args:
            generator: Callable that returns response bytes.
        """
        self._response_generator = generator
