#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

# -------------------------
# MOTORS
# -------------------------

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, 56, 121)

# -------------------------
# SENSORS
# -------------------------

ultrasonic = UltrasonicSensor(Port.S4)
touch_sensor = TouchSensor(Port.S2)

# -------------------------
# MODE SETTINGS
# -------------------------

follow_mode = False
return_mode = False

TARGET_DISTANCE = 200
MOVE_SPEED = 120
RELEASE_DISTANCE = 120


# -------------------------
# FUNCTIONS
# -------------------------

def push_release_tool():
    robot.straight(60)
    wait(300)

    robot.straight(-70)
    wait(300)


def turn_around():
    robot.turn(180)


def follow_target():
    distance = ultrasonic.distance()

    if distance > TARGET_DISTANCE:
        robot.drive(MOVE_SPEED, 0)
    else:
        robot.stop()


def collect_items():
    global return_mode

    ev3.speaker.say("Collecting")

    for count in range(3):
        push_release_tool()

    ev3.speaker.say("Returning")

    turn_around()

    return_mode = True


# -------------------------
# MAIN LOOP
# -------------------------

while True:

    # Touch sensor stops everything
    if touch_sensor.pressed():

        follow_mode = not follow_mode

        if follow_mode:
            return_mode = False
            ev3.speaker.say("Follow mode")
        else:
            return_mode = False
            ev3.speaker.say("Stopped")
            robot.stop()

        while touch_sensor.pressed():
            wait(10)

    # -------------------------
    # FOLLOW TO COLLECTION POINT
    # -------------------------

    if follow_mode:

        distance = ultrasonic.distance()

        if distance > TARGET_DISTANCE:
            robot.drive(MOVE_SPEED, 0)
        else:
            robot.stop()

        if distance < RELEASE_DISTANCE:
            robot.stop()
            follow_mode = False
            collect_items()

    # -------------------------
    # FOLLOW BACK TO BASE
    # -------------------------

    if return_mode:
        follow_target()

    wait(50)