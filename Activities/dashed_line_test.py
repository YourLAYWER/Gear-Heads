#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch

# Initialize hardware
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
line_sensor = ColorSensor(Port.S3)
timer = StopWatch()

# Constants
THRESHOLD = 40  # Midpoint between black and white
GAIN = 1.5      # How sharply it turns
BASE_SPEED = 150

while True:
    intensity = line_sensor.reflection()
    error = intensity - THRESHOLD
    
    if intensity < 80:  # We see a line or a shadow
        timer.reset()
        steering = error * GAIN
        left_motor.run(BASE_SPEED + steering)
        right_motor.run(BASE_SPEED - steering)
    else:
        # We are in a gap (White)
        if timer.time() < 500: # 0.5 seconds of "grace period"
            # Drive straight to bridge the gap
            left_motor.run(BASE_SPEED)
            right_motor.run(BASE_SPEED)
        else:
            # We are actually lost; slow down and look
            left_motor.run(BASE_SPEED / 2)
            right_motor.run(BASE_SPEED / 2)