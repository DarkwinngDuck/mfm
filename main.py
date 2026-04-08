"""Main entry point for magnetic field measurement application."""

from config import load_environment, create_printer_config, create_gaussmeter_config
from serial_impl import RealSerialPort
from Printer import Printer, TimeDelayPositionChecker
from Gaussmeter import Gaussmeter
from device_manager import DeviceManager
from measurement_service import MeasurementService
from utils import create_mesh


def run_measurement(
    x_max: float = 2.1,
    y_max: float = 2.1,
    z_max: float = 1.1,
    step: float = 0.1,
    output_file: str = "output.dat",
) -> None:
    """Run magnetic field measurement over a 3D mesh.

    Args:
        x_max: Maximum X coordinate.
        y_max: Maximum Y coordinate.
        z_max: Maximum Z coordinate.
        step: Step size for mesh.
        output_file: Path to output file.
    """
    load_environment()

    printer_config = create_printer_config()
    gaussmeter_config = create_gaussmeter_config()

    manager = DeviceManager()

    printer_port = manager.create_serial_port(printer_config)
    gaussmeter_port = manager.create_serial_port(gaussmeter_config)

    printer = Printer(
        port=printer_port,
        position_checker=TimeDelayPositionChecker(delay=0.5),
    )
    gaussmeter = Gaussmeter(port=gaussmeter_port)

    with manager.managed_device(printer):
        with manager.managed_device(gaussmeter):
            printer.move_to_home_position()

            service = MeasurementService(
                printer=printer,
                gaussmeter=gaussmeter,
                output_file=output_file,
            )

            positions = create_mesh(x_max, y_max, z_max, step)

            for record in service.measure_positions(positions):
                print(f"Measured: ({record.x}, {record.y}, {record.z}) -> {record.magnetic_field}")


if __name__ == "__main__":
    run_measurement()
