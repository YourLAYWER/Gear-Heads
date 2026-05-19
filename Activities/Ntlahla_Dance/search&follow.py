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

    if 250 < distance < SEARCH_LIMIT:

        robot.drive(MOVE_SPEED, 0)

    # -------------------------
    # TARGET REACHED
    # -------------------------

    elif distance <= 250 and distance > 0:

        robot.stop()

        # small wait prevents shaking/searching
        wait(300)

    # -------------------------
    # SEARCH MODE
    # -------------------------

    else:

        robot.stop()

        # look left
        robot.turn(-30)
        wait(300)

        distance = ultrasonic.distance()

        if distance < SEARCH_LIMIT:
            continue

        # look right
        robot.turn(60)
        wait(300)

        distance = ultrasonic.distance()

        if distance < SEARCH_LIMIT:
            continue

        # center again
        robot.turn(-30)

    wait(50)