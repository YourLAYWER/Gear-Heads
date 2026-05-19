#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

# Motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, 56, 121)

# Sensors
touch_sensor = TouchSensor(Port.S2)
ultrasonic = UltrasonicSensor(Port.S4)

# Settings
TARGET_DISTANCE = 200   # 20 cm
MOVE_SPEED = 120

ev3.speaker.say("Press to start")

# Wait for button
while not touch_sensor.pressed():
    wait(10)

wait(500)

ev3.speaker.say("Follow mode")

while True:

    distance = ultrasonic.distance()

    print(distance)

    # -------------------------
    # FOLLOW TARGET
    # -------------------------

    if TARGET_DISTANCE < distance < 600:

        robot.drive(MOVE_SPEED, 0)

    # -------------------------
    # TARGET CLOSE
    # -------------------------

    elif distance <= TARGET_DISTANCE:

        robot.stop()

    # -------------------------
    # SEARCH MODE
    # -------------------------

    else:

        robot.stop()

        # Look left
        robot.turn(-30)
        wait(300)

        distance = ultrasonic.distance()

        if TARGET_DISTANCE < distance < 600:
            continue

        # Look right
        robot.turn(60)
        wait(300)

        distance = ultrasonic.distance()

        if TARGET_DISTANCE < distance < 600:
            continue

        # Return to center
        robot.turn(-30)

    wait(50)