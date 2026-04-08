from Printer import Printer
from Gaussmeter import Gaussmeter
from config import gaussmeter_config, printer_config
from utils import create_mesh, save_xyzb


def perform_measurement(x: float, y: float, z: float, output_file="output.dat"):
    printer.move_to_position(position=(x, y, z))
    magnetic_field = gaussmeter.get_magnetic_field()
    save_xyzb(output_file, magnetic_field=magnetic_field, position=(x, y, z))
    return

if __name__ == '__main__': 
    # TODO: init into separate function
    gaussmeter = Gaussmeter(gaussmeter_config)
    printer = Printer(printer_config)

    gaussmeter.open()
    printer.open()
    printer.move_to_home_position()

    mesh = create_mesh(2.1, 2.1, 1.1, 0.1)

    for point in mesh:
        x, y, z = point
        perform_measurement(x, y, z)

    gaussmeter.close()
    printer.close()
