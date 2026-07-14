# Firmware

MicroPython firmware used in a school physics project designed to demonstrate how an aircraft wing generates lift.

The firmware runs on an ESP32 and measures the rotational speed of two custom anemometers positioned above and below a 3D-printed wing.

## Overview

Each anemometer uses a through-bore incremental encoder with two quadrature channels, named **A** and **B**.

The ESP32 detects the transitions of both channels, calculates the rotational speed in revolutions per minute, and sends the measurements to a computer through the USB serial connection.

The two anemometers are positioned as follows:

* **Bottom encoder:** measures airflow below the wing.
* **Top encoder:** measures airflow above the wing.

The computer-side software can use these measurements to calculate:

* airflow velocity;
* pressure difference;
* estimated lift force;
* real-time experimental graphs.

## Hardware

The firmware was designed for the following components:

* ESP32-WROOM-32D;
* two through-bore incremental encoders;
* two custom cup anemometers;
* four `10 kΩ` pull-up resistors;
* USB cable for power and serial communication.

## Default pin mapping

| Component      | Signal    | ESP32 GPIO |
| -------------- | --------- | ---------: |
| Bottom encoder | Channel A |    GPIO 14 |
| Bottom encoder | Channel B |    GPIO 27 |
| Top encoder    | Channel A |    GPIO 32 |
| Top encoder    | Channel B |    GPIO 33 |

The pin mapping can be changed in `config.py`.

```python
ENCODER_BOTTOM_A = 14
ENCODER_BOTTOM_B = 27

ENCODER_TOP_A = 32
ENCODER_TOP_B = 33
```

## Quadrature decoding

The encoders generate two square-wave signals with a phase difference of approximately 90 degrees.

By comparing channels A and B, the firmware can determine:

* the number of encoder transitions;
* the rotation speed;
* the rotation direction.

The firmware counts both rising and falling edges of channels A and B. This is known as quadrature **×4 decoding**.

The number of counts per revolution is calculated as:

```text
CPR = PPR × 4
```

Where:

* `PPR` is the number of pulses per revolution on one channel;
* `CPR` is the total number of detected transitions per revolution.

## RPM calculation

The rotational speed is calculated using:

```text
RPM = (N × 60) / (CPR × Δt)
```

Where:

* `N` is the number of encoder counts;
* `CPR` is the number of counts per revolution;
* `Δt` is the measurement interval in seconds.

Since the firmware uses quadrature ×4 decoding:

```text
RPM = (N × 60) / (4 × PPR × Δt)
```

## Configuration

The main settings are located in `config.py`.

```python
PPR = 1000
QUADRATURE_MULTIPLIER = 4
SAMPLE_INTERVAL_MS = 500
DECIMAL_PLACES = 2
MAX_VALID_RPM = 20000.0
```

### Encoder PPR

The default configuration uses:

```python
PPR = 1000
```

This value must be replaced with the real PPR specified in the encoder datasheet.

An incorrect PPR value will produce incorrect RPM measurements.

### Measurement interval

The default measurement interval is:

```python
SAMPLE_INTERVAL_MS = 500
```

This means that the firmware sends a new measurement every `0.5` seconds.

A shorter interval produces faster updates but may increase measurement variation at low speeds.

A longer interval produces more stable measurements but reduces the update frequency.

## Serial output

The firmware sends measurements using a simple comma-separated format:

```text
rpm_bottom,rpm_top
```

Example:

```text
320.45,391.27
```

In this example:

* the bottom anemometer is rotating at `320.45 RPM`;
* the top anemometer is rotating at `391.27 RPM`.

Lines beginning with `#` contain startup or status information:

```text
# Airfoil Lift Experiment
# format: rpm_bottom,rpm_top
320.45,391.27
325.12,397.84
```

The computer-side program should ignore lines beginning with `#`.

## Viewing the measurements

Using `mpremote`:

```bash
mpremote repl
```

Using a serial terminal:

```bash
python -m serial.tools.miniterm COM3 115200
```

On Linux, the serial port may look like:

```text
/dev/ttyUSB0
```

On Windows, it may look like:

```text
COM3
```

The exact port depends on the computer.

## Rotation direction

Because quadrature decoding determines the rotation direction, RPM values may be positive or negative.

If an anemometer produces negative RPM during normal airflow, either:

* swap channels A and B in the wiring;
* swap the channel pin definitions in `config.py`;
* invert the value in the computer-side software.

The measurement magnitude remains valid as long as the encoder is decoded correctly.

## Experimental limitations

The firmware calculates rotational speed from encoder pulses, but RPM is not automatically equal to the real airflow velocity.

The relationship between anemometer RPM and airflow velocity depends on:

* cup geometry;
* anemometer radius;
* friction;
* encoder resistance;
* air turbulence;
* mechanical losses;
* calibration.

For more accurate measurements, the anemometers should be calibrated using a known airflow velocity.

The current physics model uses representative average velocities measured at fixed positions above and below the wing.

## Authors

* Diego Trigo Araujo
* Luis Felipe Nascimento de Freitas

School physics project developed at Instituto Alpha Lumen.
