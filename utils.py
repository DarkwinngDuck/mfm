from itertools import product
from typing import Iterator
import numpy as np

def create_mesh(
    x_max: float, y_max: float, z_max: float, step: float = 0.01
) -> Iterator[float]:
    """
    Generate a 3D mesh of float points from (1.0, 1.0, 1.0) to (x_max, y_max, z_max)
    with the given step.
    """
    x_range = np.round(np.arange(1.0, x_max + step, step), 1)
    y_range = np.round(np.arange(1.0, y_max + step, step), 1)
    z_range = np.round(np.arange(1.0, z_max + step, step), 1)

    return product(x_range, y_range, z_range)


def save_xyzb(file_path: str, magnetic_field: float, position: tuple[float, float, float]):
    """
    Append a single measurement (X, Y, Z, B) to the file.

    Args:
        file_path: Path to the output file.
        point: (x, y, z) coordinates.
        magnetic_field: Magnetic field measurement at that point.
    """
    x, y, z = position
    with open(file_path, "a") as f:  # 'a' = append mode
        f.write(f"{x}\t{y}\t{z}\t{magnetic_field}\n")
