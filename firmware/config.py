# config.py
# Configuration for the Airfoil Lift Experiment

# Encoder 1: lower surface of the wing
ENCODER_BOTTOM_A = 14
ENCODER_BOTTOM_B = 27

# Encoder 2: upper surface of the wing
ENCODER_TOP_A = 32
ENCODER_TOP_B = 33

# Encoder resolution informed by the manufacturer.
# PPR = pulses per revolution for a single channel.
PPR = 1000

# Quadrature decoding mode.
# This firmware counts every rising and falling edge on channels A and B.
QUADRATURE_MULTIPLIER = 4

# Measurement interval in milliseconds.
SAMPLE_INTERVAL_MS = 500

# Serial output settings.
# USB serial on the ESP32 uses the default REPL serial connection.
DECIMAL_PLACES = 2

# Ignore RPM values above this limit as probable electrical noise.
MAX_VALID_RPM = 20000.0
