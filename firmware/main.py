# main.py
"""
Airfoil Lift Experiment
-----------------------

Reads two incremental quadrature encoders connected to an ESP32 and
calculates their rotational speeds in RPM.

Encoder positions:
    - bottom: below the wing
    - top: above the wing

Serial output:
    rpm_bottom,rpm_top

Example:
    320.45,391.27

The computer can read this CSV-like stream through the ESP32 USB serial
connection and convert RPM into airflow velocity, pressure difference,
and lift force.
"""

from machine import Pin
from micropython import const
import time

from config import (
    ENCODER_BOTTOM_A,
    ENCODER_BOTTOM_B,
    ENCODER_TOP_A,
    ENCODER_TOP_B,
    PPR,
    QUADRATURE_MULTIPLIER,
    SAMPLE_INTERVAL_MS,
    DECIMAL_PLACES,
    MAX_VALID_RPM,
)


# Valid transitions for quadrature decoding.
# Index: previous_state << 2 | current_state
# Values: +1, -1 or 0.
_TRANSITION_TABLE = (
    0, -1, 1, 0,
    1, 0, 0, -1,
    -1, 0, 0, 1,
    0, 1, -1, 0,
)


class QuadratureEncoder:
    def __init__(self, pin_a, pin_b, name):
        self.name = name

        # External 10 kOhm pull-up resistors are recommended for
        # open-collector encoder outputs.
        self.pin_a = Pin(pin_a, Pin.IN)
        self.pin_b = Pin(pin_b, Pin.IN)

        self._count = 0
        self._previous_state = self._read_state()

        trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING
        self.pin_a.irq(trigger=trigger, handler=self._handle_edge)
        self.pin_b.irq(trigger=trigger, handler=self._handle_edge)

    def _read_state(self):
        return (self.pin_a.value() << 1) | self.pin_b.value()

    def _handle_edge(self, _pin):
        current_state = self._read_state()
        transition = (self._previous_state << 2) | current_state
        self._count += _TRANSITION_TABLE[transition]
        self._previous_state = current_state

    def read_and_reset(self):
        """
        Atomically returns the accumulated count and resets it.

        Disabling interrupts briefly prevents an encoder edge from being
        lost while the counter is copied and cleared.
        """
        irq_state = __import__("machine").disable_irq()
        count = self._count
        self._count = 0
        __import__("machine").enable_irq(irq_state)
        return count


def counts_to_rpm(counts, elapsed_ms):
    """Convert quadrature counts measured during elapsed_ms into RPM."""
    if elapsed_ms <= 0:
        return 0.0

    counts_per_revolution = PPR * QUADRATURE_MULTIPLIER
    elapsed_seconds = elapsed_ms / 1000.0

    rpm = (counts * 60.0) / (counts_per_revolution * elapsed_seconds)

    # Reject physically implausible values caused by electrical noise.
    if abs(rpm) > MAX_VALID_RPM:
        return 0.0

    return rpm


def format_measurement(rpm_bottom, rpm_top):
    """Return the serial line expected by the computer software."""
    return (
        "{bottom:.{places}f},{top:.{places}f}".format(
            bottom=rpm_bottom,
            top=rpm_top,
            places=DECIMAL_PLACES,
        )
    )


def main():
    encoder_bottom = QuadratureEncoder(
        ENCODER_BOTTOM_A,
        ENCODER_BOTTOM_B,
        "bottom",
    )

    encoder_top = QuadratureEncoder(
        ENCODER_TOP_A,
        ENCODER_TOP_B,
        "top",
    )

    last_measurement = time.ticks_ms()

    # Small startup message. Lines beginning with "#" may be ignored by
    # the computer-side parser.
    print("# Airfoil Lift Experiment")
    print("# format: rpm_bottom,rpm_top")

    while True:
        time.sleep_ms(10)

        now = time.ticks_ms()
        elapsed_ms = time.ticks_diff(now, last_measurement)

        if elapsed_ms < SAMPLE_INTERVAL_MS:
            continue

        bottom_counts = encoder_bottom.read_and_reset()
        top_counts = encoder_top.read_and_reset()

        rpm_bottom = counts_to_rpm(bottom_counts, elapsed_ms)
        rpm_top = counts_to_rpm(top_counts, elapsed_ms)

        print(format_measurement(rpm_bottom, rpm_top))

        last_measurement = now


try:
    main()
except KeyboardInterrupt:
    print("# measurement stopped")
