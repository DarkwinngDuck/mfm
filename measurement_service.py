"""Measurement service for coordinating devices."""

from dataclasses import dataclass
from typing import Callable, Iterator, Optional, Protocol, Tuple

from Printer import Printer
from Gaussmeter import Gaussmeter


@dataclass
class MeasurementRecord:
    """A single measurement record.

    Attributes:
        x: X coordinate.
        y: Y coordinate.
        z: Z coordinate.
        magnetic_field: Magnetic field value at position.
    """

    x: float
    y: float
    z: float
    magnetic_field: float

    def to_tuple(self) -> Tuple[float, float, float, float]:
        """Convert to (x, y, z, b) tuple."""
        return (self.x, self.y, self.z, self.magnetic_field)


class PositionProvider(Protocol):
    """Protocol for providing measurement positions."""

    def get_positions(self) -> Iterator[Tuple[float, float, float]]:
        """Yield positions to measure.

        Yields:
            (x, y, z) coordinate tuples.
        """
        ...


class MeasurementService:
    """Service for performing magnetic field measurements.

    Coordinates between printer positioning and gaussmeter measurement.
    """

    def __init__(
        self,
        printer: Printer,
        gaussmeter: Gaussmeter,
        output_file: str = "output.dat",
    ):
        """Initialize measurement service.

        Args:
            printer: Printer device for positioning.
            gaussmeter: Gaussmeter device for measurement.
            output_file: Path to output file for results.
        """
        self._printer = printer
        self._gaussmeter = gaussmeter
        self._output_file = output_file

    def measure_at_position(
        self, position: Tuple[float, float, float]
    ) -> MeasurementRecord:
        """Perform measurement at a single position.

        Args:
            position: (x, y, z) coordinates.

        Returns:
            MeasurementRecord with coordinates and field value.
        """
        x, y, z = position

        self._printer.move_to_position(position)
        magnetic_field = self._gaussmeter.get_magnetic_field()

        return MeasurementRecord(x=x, y=y, z=z, magnetic_field=magnetic_field)

    def measure_positions(
        self,
        positions: Iterator[Tuple[float, float, float]],
        on_progress: Optional[Callable[[MeasurementRecord], None]] = None,
    ) -> Iterator[MeasurementRecord]:
        """Perform measurements at multiple positions.

        Args:
            positions: Iterator of (x, y, z) coordinates.
            on_progress: Optional callback called after each measurement.

        Yields:
            MeasurementRecord for each position.
        """
        for position in positions:
            record = self.measure_at_position(position)
            self._save_record(record)

            if on_progress:
                on_progress(record)

            yield record

    def _save_record(self, record: MeasurementRecord) -> None:
        """Append measurement record to output file.

        Args:
            record: Measurement record to save.
        """
        with open(self._output_file, "a") as f:
            x, y, z, b = record.to_tuple()
            f.write(f"{x}\t{y}\t{z}\t{b}\n")
