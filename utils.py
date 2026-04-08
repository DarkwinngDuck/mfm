"""Measurement utilities."""

from itertools import product
from typing import Iterable, Iterator, Tuple


def create_mesh(
    x_max: float,
    y_max: float,
    z_max: float,
    step: float = 0.01,
    start: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> Iterator[Tuple[float, float, float]]:
    """Generate a 3D mesh of float points.

    Args:
        x_max: Maximum X coordinate.
        y_max: Maximum Y coordinate.
        z_max: Maximum Z coordinate.
        step: Step size for all axes.
        start: Starting (x, y, z) coordinates.

    Yields:
        (x, y, z) coordinate tuples.
    """
    import numpy as np

    x_start, y_start, z_start = start

    x_range = np.round(np.arange(x_start, x_max + step, step), 2)
    y_range = np.round(np.arange(y_start, y_max + step, step), 2)
    z_range = np.round(np.arange(z_start, z_max + step, step), 2)

    return product(x_range, y_range, z_range)


def save_xyzb(
    file_path: str,
    magnetic_field: float,
    position: Tuple[float, float, float],
    delimiter: str = "\t",
) -> None:
    """Append a single measurement to file.

    Args:
        file_path: Path to output file.
        magnetic_field: Magnetic field measurement.
        position: (x, y, z) coordinates.
        delimiter: Field delimiter (default: tab).
    """
    x, y, z = position
    with open(file_path, "a") as f:
        f.write(f"{x}{delimiter}{y}{delimiter}{z}{delimiter}{magnetic_field}\n")


def format_measurement_record(
    magnetic_field: float,
    position: Tuple[float, float, float],
    delimiter: str = "\t",
) -> str:
    """Format a measurement record as a string.

    Args:
        magnetic_field: Magnetic field measurement.
        position: (x, y, z) coordinates.
        delimiter: Field delimiter.

    Returns:
        Formatted record string.
    """
    x, y, z = position
    return f"{x}{delimiter}{y}{delimiter}{z}{delimiter}{magnetic_field}"
