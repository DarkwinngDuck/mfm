from serial import Serial
from config import SerialConfig


class Gaussmeter(Serial):
    """
    A Gaussmeter class to perform magnetic field measuremets.
    TODO: add units
    """

    def __init__(self, config: SerialConfig):
        super().__init__(
            port=config.port,
            baudrate=config.baudrate,
            timeout=config.timeout,
        )

    def get_magnetic_field(self):
        """
        Measure magnetic field.

        Returns:
            (float): field value in TODO: units.
        """

        befehl = ":MEAS?\r"
        self.flushInput()
        self.flushOutput()
        self.write(befehl.encode())
        res = (self.ser.readline()).decode()
        return float(res.rstrip("\n"))
