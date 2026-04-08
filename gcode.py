"""G-code command builder for 3D printer control."""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union

from commands import PrinterCommand
from constants import DEFAULT_MOVE_SPEED, HOME_POSITION


@dataclass
class GcodeCommand:
    """Represents a G-code command string.

    Attributes:
        command: The G-code command (e.g., 'G20', 'G28').
        parameters: Optional parameters for the command.
    """

    command: str
    parameters: Optional[Dict[str, Union[str, int, float]]] = None

    def __str__(self) -> str:
        """Render command as G-code string.

        Returns:
            G-code command string ready to send to printer.
        """
        if not self.parameters:
            return self.command

        params = " ".join(f"{k}{v}" for k, v in self.parameters.items())
        return f"{self.command} {params}"


class GcodeBuilder:
    """Builder for constructing G-code commands."""

    @staticmethod
    def move(
        position: Tuple[float, float, float] = HOME_POSITION,
        speed: int = DEFAULT_MOVE_SPEED,
    ) -> GcodeCommand:
        """Create a move command.

        Args:
            position: Target (x, y, z) coordinates.
            speed: Movement speed (feed rate).

        Returns:
            GcodeCommand for moving to position.
        """
        x, y, z = position
        return GcodeCommand(
            command=PrinterCommand.MOVE.value,
            parameters={"X": x, "Y": y, "Z": z, "F": speed},
        )

    @staticmethod
    def move_to_home() -> GcodeCommand:
        """Create a move-to-home command.

        Returns:
            GcodeCommand for homing.
        """
        return GcodeCommand(command=PrinterCommand.MOVE_TO_HOME.value)

    @staticmethod
    def check_position() -> GcodeCommand:
        """Create a position check command.

        Returns:
            GcodeCommand for querying current position.
        """
        return GcodeCommand(command=PrinterCommand.CHECK_POSITION.value)
