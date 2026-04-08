import time

from serial import Serial
from config import SerialConfig, ENCODE, HOME_POSITION, DEFAULT_MOVE_SPEED, Command


class Printer(Serial):
    """
    A Printer class to send commands to printer and move its head into
    different positions.
    """

    def __init__(self, config: SerialConfig):
        super().__init__(
            port=config.port,
            baudrate=config.baudrate,
            timeout=config.timeout,
        )

    def send_gcode(self, command_code: str) -> list[str]:
        """
        Send gcode command to the device and return list of output strings.

        Args:
            command_code (str): device command.

        Returns:
            (list[str]): output strings from the device.

        # TODO: add proper logging
        """
        print("Sending G-code: ", command_code)

        self.write(command_code.encode(ENCODE))

        device_outputs = []

        while True:
            line = self.readline().decode(ENCODE, errors="ignore").strip()

            if line:
                print("Printer output: ", line)
                device_outputs.append(line)

            if line.lower() == "ok":
                break

        return device_outputs

    def move_to_position(
        self,
        position: tuple[float, float, float] = HOME_POSITION,
        speed=DEFAULT_MOVE_SPEED,
    ) -> bool:
        """
        Move to position xyz.

        Args:
            position (tuple[float, float, float]): Position coordinates.
            speed (int): Speed.

        Returns:
            (bool): True if movement command succeed.

        TODO: single responsibility not reached
        """

        x, y, z = position

        gcode = f"{Command.MOVE} X{x} Y{y} Z{z} F{speed}"

        self.send_gcode(gcode)

        while not self.is_at_position(position):
            time.sleep(0.1)

        print("Printer: position reached")
        return True

    def is_at_position(
        self, target_position: tuple[float, float, float] = HOME_POSITION
    ) -> bool:
        """
        TODO: Write function to check position
        """
        time.sleep(10)
        return True

    def move_to_home_position(self) -> bool:
        """
        Move to home position.

        Returns:
            (bool): True if movement succeed.
        """
        self.send_gcode(f"{Command.MOVE_TO_HOME}")
        return True
