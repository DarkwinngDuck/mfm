import os
from dataclasses import dataclass
from enum import Enum

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
from dotenv import dotenv_values


os.environ.update(dotenv_values(".env"))


PRINTER_PORT = os.getenv("PRINTER_PORT")
PRINTER_BAUDRATE = int(os.environ.get("PRINTER_BAUDRATE"), 0)
GAUSSMETER_PORT = os.getenv("GAUSSMETER_PORT")
GAUSSMETER_BAUDRATE = int(os.getenv("GAUSSMETER_BAUDRATE"), 0)
DEFAULT_BAUDRATE = int(os.environ.get("DEFAULT_BAUDRATE"), 0)
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT"), 0)
DEFAULT_MOVE_SPEED = int(os.getenv("DEFAULT_MOVE_SPEED"), 0)


class Command(Enum):
    # TODO: add list of all needed commands
    MOVE = "G20"
    CHECK_POSITION = "M114"
    MOVE_TO_HOME = "G28"


@dataclass
class SerialConfig:
    port: str
    baudrate: int = DEFAULT_BAUDRATE
    timeout: float = DEFAULT_TIMEOUT
    bytesize: int = EIGHTBITS
    parity: str = PARITY_NONE
    stopbits: int = STOPBITS_ONE


printer_config = SerialConfig(port=PRINTER_PORT, baudrate=PRINTER_BAUDRATE)
gaussmeter_config = SerialConfig(port=GAUSSMETER_PORT, baudrate=GAUSSMETER_BAUDRATE)

ENCODE = "ascii"
HOME_POSITION = (0, 0, 0)
DEFAULT_MOVE_SPEED = 150
