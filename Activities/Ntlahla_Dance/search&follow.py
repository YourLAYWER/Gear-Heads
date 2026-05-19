#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

# -------------------------
# MOTORS
# -------------------------

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor = Motor(Port.A)

robot = DriveBase(left_motor, right_motor, 56, 121)

# -------------------------
# SENSORS
# -------------------------

touch_sensor = TouchSensor(Port.S2)
ultrasonic = UltrasonicSensor(Port.S4)
gyro_sensor = GyroSensor(Port.S1)

# -------------------------
# SETTINGS
# -------------------------

TARGET_DISTANCE = 180
MAX_DISTANCE = 600
MOVE_SPEED = 80

press_count = 0
follow_mode = False


# -------------------------
# FUNCTIONS
# -------------------------

def gyro_turn(target_angle):
    gyro_sensor.reset_angle(0)
    wait(300)

    if target_angle > 0:
        turn_speed = 40
    else:
        turn_speed = -40

    robot.drive(0, turn_speed)

    while abs(gyro_sensor.angle()) < abs(target_angle):
        wait(10)

    robot.stop()
    wait(200)


def search_left_right():
    robot.stop()
    wait(500)

    # look left
    gyro_turn(-20)

    distance = ultrasonic.distance()

    if TARGET_DISTANCE < distance < MAX_DISTANCE:
        return

    # look right
    gyro_turn(40)

    distance = ultrasonic.distance()

    if TARGET_DISTANCE < distance < MAX_DISTANCE:
        return

    # return to center
    gyro_turn(-20)


def follow_target():
    distance = ultrasonic.distance()
    print(distance)

    if TARGET_DISTANCE < distance < MAX_DISTANCE:
        robot.drive(MOVE_SPEED, 0)

    elif 0 < distance <= TARGET_DISTANCE:
        robot.stop()

    else:
        search_left_right()


def drop_lift():
    ev3.speaker.say("Drop")
    lift_motor.run_angle(150, -90)
    wait(300)


def raise_lift():
    ev3.speaker.say("Lift")
    lift_motor.run_angle(150, 90)
    wait(300)


def push_release_tool():
    robot.straight(60)
    wait(300)

    robot.straight(-70)
    wait(300)


def reverse_with_items():
    ev3.speaker.say("Reverse")
    robot.straight(-500)
    robot.stop()


def collect_items():
    ev3.speaker.say("Collect")

    drop_lift()

    for count in range(3):
        push_release_tool()

    ev3.speaker.say("Return")
    reverse_with_items()

    raise_lift()

    ev3.speaker.say("Done")


# -------------------------
# MAIN PROGRAM
# -------------------------

ev3.speaker.say("Press")

while True:

    # -------------------------
    # BUTTON CONTROL
    # -------------------------

    if touch_sensor.pressed():

        press_count += 1

        # PRESS 1: start follow mode
        if press_count == 1:
            follow_mode = True
            ev3.speaker.say("Follow")

        # PRESS 2: stop and prepare to collect
        elif press_count == 2:
            follow_mode = False
            robot.stop()
            ev3.speaker.say("Press again")

        # PRESS 3: collect items and reverse back
        elif press_count == 3:
            follow_mode = False
            robot.stop()

            collect_items()

            press_count = 0
            follow_mode = False

        while touch_sensor.pressed():
            wait(10)

        wait(500)

    # -------------------------
    # FOLLOW LOGIC
    # -------------------------

    if follow_mode:
        follow_target()
    else:
        robot.stop()

    wait(200)