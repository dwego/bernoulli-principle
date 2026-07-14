# bernoulli-principle

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Documentation: CC BY 4.0](https://img.shields.io/badge/Documentation-CC%20BY%204.0-lightgrey.svg)](./LICENSE-DOCUMENTATION)

[Versão em português](./README.md)

A school physics project developed to demonstrate how a wing generates lift by analyzing the airflow above and below an aerodynamic profile.

The experiment uses a 3D-printed wing, two custom anemometers, incremental encoders, an ESP32 running MicroPython, and a wind tunnel built from a PVC pipe.

## Overview

Two anemometers are positioned around the wing:

- one above the upper surface;
- one below the lower surface.

Each anemometer is connected to an incremental encoder. The ESP32 reads the quadrature channels, calculates rotational speed in RPM, and sends the measurements to a computer through USB serial.

The computer can use the measurements to estimate:

- airflow velocity;
- pressure difference;
- lift force;
- airflow behavior around the wing.

## How it works

```text
Air inlet
    ↓
[ Fan ]
    ↓
[ Top anemometer    ]
[        Wing       ]
[ Bottom anemometer ]
    ↓
Tunnel outlet
```

The ESP32 sends measurements using the following format:

```text
rpm_bottom,rpm_top
```

Example:

```text
312.45,389.21
```

## Main components

- ESP32-WROOM-32D;
- two through-bore incremental encoders;
- two 3D-printed cup anemometers;
- 3D-printed experimental wing;
- four `10 kΩ` pull-up resistors;
- PVC pipe with an approximate diameter of `24 cm`;
- fan;
- computer for data reading and processing.

## Directories

- [`firmware/`](./firmware/) — MicroPython code running on the ESP32;
- [`electronics/`](./electronics/) — schematic and wiring;
- [`hardware/`](./hardware/) — CAD models, STL files, and assembly;
- [`software/`](./software/) — serial reading, calculations, and graphs;
- [`report/`](./report/) — complete LaTeX report.

## Hardware

The mechanical assembly contains three main elements.

### Wing

The wing has a curved upper surface and an approximately flat lower surface.

CAD and STL files should be stored in:

```text
hardware/cad/wing.step
hardware/stl/wing.stl
```

### Anemometers

Each anemometer uses three cups distributed around a central shaft connected to an incremental encoder.

The files should be stored in:

```text
hardware/cad/anemometer.step
hardware/stl/anemometer.stl
```

### Wind tunnel

The airflow is guided by a wind tunnel built from a PVC pipe.

The files should be stored in:

```text
hardware/cad/pvc-wind-tunnel.step
hardware/stl/pvc-wind-tunnel.stl
```

See the complete assembly documentation:

[`hardware/hardware.md`](./hardware/hardware_en.md)

## Electronics

The two encoders are connected to the ESP32 using four signal lines.

| Sensor | Channel | GPIO |
|---|---|---:|
| Top encoder | A | GPIO 32 |
| Top encoder | B | GPIO 33 |
| Bottom encoder | A | GPIO 14 |
| Bottom encoder | B | GPIO 27 |

Each signal line uses an external `10 kΩ` pull-up resistor connected to `3.3 V`.

See the complete schematic:

[`electronics/eletronics.md`](./electronics/eletronics_en.md)

## Firmware

The MicroPython firmware:

1. detects transitions on channels A and B;
2. performs quadrature decoding;
3. counts encoder pulses;
4. calculates rotational speed in RPM;
5. sends the measurements through USB serial.

See:

[`firmware/firmware.md`](./firmware/firmware_en.md)

## Physical model

Angular velocity is calculated from RPM:

```text
ω = RPM × π / 30
```

The approximate tangential velocity is:

```text
v = ωr
```

Pressure difference is estimated using Bernoulli's equation and the average airflow speeds measured above and below the wing.

The model includes simplifications and represents an experimental approximation. The anemometers must be calibrated to correctly relate RPM to real airflow velocity.

## Report

The complete school report contains:

- introduction;
- objectives;
- materials;
- experimental methodology;
- Bernoulli's principle;
- RPM calculation;
- pressure difference;
- lift estimation;
- encoder operation;
- experimental limitations;
- results;
- conclusion.

See:

[`report/report.md`](./report/report_en.md)

## Authors

- Diego Trigo Araujo
- Luis Felipe Nascimento de Freitas

School physics project developed at Instituto Alpha Lumen.

## License

Source code inside the `firmware/` and `software/` directories is licensed under the [MIT License](./LICENSE).

The report, CAD models, diagrams, and images are licensed under the [Creative Commons Attribution 4.0 International](./LICENSE-DOCUMENTATION).

Appropriate credit must be given to the authors when reusing the material.