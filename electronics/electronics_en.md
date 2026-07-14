# Eletronics

This directory contains the **electronic schematic diagram** of the project.

The circuit was designed to measure airflow **above** and **below** a wing using **two incremental encoders**, connected to an **ESP32-WROOM-32D**, with quadrature signal reading and USB serial data output.

## Schematic diagram

<p align="center">
  <img src="./schematic.svg" alt="Project electronics schematic diagram" width="100%">
</p>

## Circuit overview

The electronic system is composed of:

* **1 ESP32-WROOM-32D**
* **2 incremental encoders**

  * top encoder
  * bottom encoder
* **4 pull-up resistors of 10 kΩ**
* **3.3 V supply**
* **common ground**
* **USB serial connection to the computer**

The purpose of the circuit is to read the rotation of two anemometers:

* one positioned **above the wing**
* one positioned **below the wing**

These rotations are converted into **RPM** values by the MicroPython firmware running on the ESP32.

## Connections

### Top encoder (`J1`)

| Encoder pin | Function  | ESP32 connection |
| ----------- | --------- | ---------------- |
| VCC         | Power     | `+3V3`           |
| GND         | Ground    | `GND`            |
| A           | Channel A | `GPIO32`         |
| B           | Channel B | `GPIO33`         |

### Bottom encoder (`J2`)

| Encoder pin | Function  | ESP32 connection |
| ----------- | --------- | ---------------- |
| VCC         | Power     | `+3V3`           |
| GND         | Ground    | `GND`            |
| A           | Channel A | `GPIO14`         |
| B           | Channel B | `GPIO27`         |

## Pull-up resistors

The circuit uses **four 10 kΩ resistors**:

* `R1` and `R2` for the top encoder
* `R3` and `R4` for the bottom encoder

These resistors pull the **A** and **B** signal lines up to `3.3 V`.

This is especially important when the encoders use:

* **open-collector**
* **open-drain**

outputs.

## Power supply

The whole logic system must operate at **3.3 V**.

* the ESP32 `3V3` pin powers the encoders;
* all grounds must be connected together;
* signals applied to the ESP32 **must not exceed 3.3 V**.

> **Important:** do not connect `5 V` signals directly to ESP32 GPIO pins.

## Serial output

The ESP32 sends data to the computer through **USB serial**.

Expected output format:

```text
rpm_bottom,rpm_top
```

Example:

```text
312.45,389.21
```

Where:

* `rpm_bottom` represents the bottom anemometer;
* `rpm_top` represents the top anemometer.

## Important notes

* All **grounds must be common**.
* The encoders must be compatible with ESP32 logic levels.
* If the encoder has open outputs, pull-up resistors are required.
* The schematic represents the main electronics of the system, focused on sensor reading and communication with the computer.