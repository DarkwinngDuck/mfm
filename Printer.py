"""Printer device control."""

import time
from typing import Callable, List, Optional, Protocol, Tuple, Union

from serial_interface import BaseSerialDevice, SerialPort
from gcode import GcodeBuilder, GcodeCommand
from constants import DEFAULT_MOVE_SPEED, HOME_POSITION


class PositionChecker(Protocol):
    """Protocol for position verification strategies."""

    def is_at_position(self, target: Tuple[float, float, float]) -> bool:
        """Check if printer is at target position.

        Args:
            target: Target (x, y, z) coordinates.

        Returns:
            True if at target position.
        """
        ...


class TimeDelayPositionChecker:
    """Position checker that uses time delay (simplified approach).

    Assumes movement completes within a fixed time.
    """

    def __init__(self, delay: float = 0.5):
        """Initialize with delay time.

        Args:
            delay: Time to wait for movement completion.
        """
        self._delay = delay

    def is_at_position(self, target: Tuple[float, float, float]) -> bool:
        """Wait and assume position reached.

        Args:
            target: Target position (ignored).

        Returns:
            Always True after delay.
        """
        time.sleep(self._delay)
        return True


class Printer(BaseSerialDevice):
    """3D printer controller for positioning.

    Sends G-code commands to control printer head movement.
    """

    def __init__(
        self,
        port: SerialPort,
        position_checker: Optional[PositionChecker] = None,
        command_callback: Optional[Callable[[str], None]] = None,
    ):
        """Initialize printer.

        Args:
            port: SerialPort implementation for communication.
            position_checker: Strategy for verifying position.
            command_callback: Optional callback for logging commands.
        """
        super().__init__(port=port)
        self._position_checker = position_checker or TimeDelayPositionChecker()
        self._command_callback = command_callback or self._noop

    @staticmethod
    def _noop(*args, **kwargs) -> None:
        """No-op callback."""
        pass

    def _send_gcode(self, command: Union[GcodeCommand, str]) -> List[str]:
        """Send G-code command and collect responses.

        Args:
            command: G-code command to send.

        Returns:
            List of response lines from printer.
        """
        command_str = str(command)
        self._command_callback(f"Sending G-code: {command_str}")

        self._write(command_str.encode())

        responses = []
        while True:
            line = self._readline().decode().strip()
            if line:
                self._command_callback(f"Printer output: {line}")
                responses.append(line)
            if line.lower() == "ok":
                break

        return responses

    def move_to_position(
        self,
        position: Tuple[float, float, float] = HOME_POSITION,
        speed: int = DEFAULT_MOVE_SPEED,
    ) -> bool:
        """Move printer head to position.

        Args:
            position: Target (x, y, z) coordinates.
            speed: Movement speed (feed rate).

        Returns:
            True if movement succeeded.
        """
        command = GcodeBuilder.move(position=position, speed=speed)
        self._send_gcode(command)

        while not self._position_checker.is_at_position(position):
            time.sleep(0.1)

        self._command_callback("Printer: position reached")
        return True

    def move_to_home_position(self) -> bool:
        """Move printer head to home position.

        Returns:
            True if homing succeeded.
        """
        command = GcodeBuilder.move_to_home()
        self._send_gcode(command)
        return True

    def get_current_position(self) -> Optional[Tuple[float, float, float]]:
        """Query current printer position.

        Returns:
            Current (x, y, z) position or None if parsing fails.
        """
        command = GcodeBuilder.check_position()
        responses = self._send_gcode(command)

        for response in responses:
            if "X:" in response and "Y:" in response and "Z:" in response:
                try:
                    parts = response.split()
                    x = y = z = 0.0
                    for part in parts:
                        if part.startswith("X:"):
                            x = float(part[2:])
                        elif part.startswith("Y:"):
                            y = float(part[2:])
                        elif part.startswith("Z:"):
                            z = float(part[2:])
                    return (x, y, z)
                except ValueError:
                    pass
        return None
