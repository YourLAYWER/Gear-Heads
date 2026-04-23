#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Initialisation
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
# Connect the Ultrasonic Sensor to Port 4
ultrasonic = UltrasonicSensor(Port.S4)

# Setup DriveBase (wheel_diameter=56mm, axle_track=121mm)
robot = DriveBase(left_motor, right_motor, 56, 121)

# ==========================================================
# CONFIGURATION
# ==========================================================
TARGET_DISTANCE = 200  # Target distance from object in mm (20cm)
GAIN = 1.5             # How fast the robot reacts to distance changes

ev3.speaker.beep()

while True:
    # 1. Read the current distance to the object in front
    current_distance = ultrasonic.distance()

    # 2. Calculate the "Error" (How far we are from our 200mm goal)
    # If distance is 300, error is 100 (Move forward)
    # If distance is 100, error is -100 (Move backward)
    error = current_distance - TARGET_DISTANCE

    # 3. Calculate speed based on the error
    drive_speed = error * GAIN

    # 4. Apply the movement
    # We keep steering at 0 to stay in a straight line
    robot.drive(drive_speed, 0)

    # Debugging to the EV3 screen
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Dist: " + str(current_distance))
    
    wait(10)