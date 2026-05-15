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
# SETTINGS
# -------------------------

follow_mode = False

TARGET_DISTANCE = 200   # 20 cm
MOVE_SPEED = 120

RELEASE_DISTANCE = 120  # 12 cm from release tool


# -------------------------
# FUNCTIONS
# -------------------------

def push_release_tool():
    robot.straight(60)     # push forward
    wait(300)

    robot.straight(-70)    # move back to reset
    wait(300)


def collect_items():

    ev3.speaker.say("Collecting")

    for count in range(3):
        push_release_tool()

    ev3.speaker.say("Returning")

    # turn around
    turn_around()

    # follow back forever until stopped
    while True:
        follow_target()
        wait(50)


def turn_around():
    robot.turn(180)

#-------------------------
#STILL TO ADD THE FOLLOW BACK CODE
#------------------------------------

def follow_target():
    distance = ultrasonic.distance()

    if distance > TARGET_DISTANCE:
        robot.drive(MOVE_SPEED, 0)
    else:
        robot.stop()

# -------------------------
# MAIN LOOP
# -------------------------

while True:

    # Touch sensor toggles follow mode
    if touch_sensor.pressed():

        follow_mode = not follow_mode

        if follow_mode:
            ev3.speaker.say("Follow mode")
        else:
            ev3.speaker.say("Stopped")
            robot.stop()

        while touch_sensor.pressed():
            wait(10)

    # -------------------------
    # FOLLOW LOGIC
    # -------------------------

    if follow_mode:

        distance = ultrasonic.distance()

        # Object/person is far, move forward
        if distance > TARGET_DISTANCE:
            robot.drive(MOVE_SPEED, 0)

        # Object/person is close enough
        else:
            robot.stop()

        # If robot reaches release station
        if distance < RELEASE_DISTANCE:
            robot.stop()
            follow_mode = False
            collect_items()

    wait(50)