# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python application for measuring magnetic field as a function of 3D coordinates. Controls a gaussmeter via serial communication and a 3D printer to position the sensor.

## Architecture

### Core Modules

- **constants.py** - Application constants (encoding, positions, speeds, timeouts)
- **commands.py** - Device command enums (`PrinterCommand`, `GaussmeterCommand`)
- **config.py** - Configuration loading, `SerialConfig` dataclass, factory functions
- **serial_interface.py** - `SerialPort` Protocol and `BaseSerialDevice` abstract base class
- **serial_impl.py** - `RealSerialPort` using pyserial library
- **serial_mock.py** - `MockSerialPort` for testing without hardware

### Device Layers

- **gcode.py** - `GcodeCommand` dataclass and `GcodeBuilder` for constructing printer commands
- **Printer.py** - `Printer` class with pluggable `PositionChecker` strategy
- **Gaussmeter.py** - `Gaussmeter` class with pluggable `MagneticFieldParser` strategy

### Service Layer

- **device_manager.py** - `DeviceManager` for device lifecycle (context manager pattern)
- **measurement_service.py** - `MeasurementService` coordinating printer + gaussmeter
- **utils.py** - `create_mesh()` generator, `save_xyzb()` and formatting utilities

### Entry Point

- **main.py** - `run_measurement()` function using service layer

## Commands

```bash
# Run the application
python main.py

# Activate virtual environment (if needed)
source .venv/bin/activate
```

## Configuration

Copy `.env.example` to `.env` and configure:
- `PRINTER_PORT` / `GAUSSMETER_PORT` - Serial ports (e.g., `/dev/ttyUSB0`, `COM1`)
- `PRINTER_BAUDRATE` / `GAUSSMETER_BAUDRATE` - Default: 9600
- `DEFAULT_TIMEOUT` - Serial timeout in seconds
- `DEFAULT_MOVE_SPEED` - Printer movement speed

## Key Details

- Measurement output: tab-separated `X\tY\tZ\tB` format in `output.dat`
- Default mesh: from (1.0, 1.0, 1.0) to (2.1, 2.1, 1.1) with 0.1 step (configurable start)
- Uses `pyserial` for serial communication
- Python 3.9+

## Design Principles Applied

- **SOLID**: Single responsibility per class, dependency inversion via Protocols
- **GRASP**: High cohesion, low coupling, indirection via service layer
- **Strategy Pattern**: Pluggable `PositionChecker` and `MagneticFieldParser`
- **Context Manager**: `DeviceManager.managed_device()` for lifecycle
