"""Device command definitions."""

from enum import Enum


class PrinterCommand(Enum):
    """G-code commands for printer control."""

    MOVE = "G20"
    CHECK_POSITION = "M114"
    MOVE_TO_HOME = "G28"


class GaussmeterCommand(Enum):
    """Commands for gaussmeter control."""

    MEASURE = ":MEAS?\r"
