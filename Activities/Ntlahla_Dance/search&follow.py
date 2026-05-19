#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, 56, 121)

touch_sensor = TouchSensor(Port.S2)
ultrasonic = UltrasonicSensor(Port.S4)
gyro_sensor = GyroSensor(Port.S1)

TARGET_DISTANCE = 250
MAX_DISTANCE = 600
MOVE_SPEED = 80

press_count = 0
follow_mode = False
return_mode = False


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


def return_to_base():
    global return_mode

    ev3.speaker.say("Returning")
    gyro_turn(180)
    return_mode = True


ev3.speaker.say("Press")


while True:

    if touch_sensor.pressed():

        press_count += 1

        if press_count == 1:
            follow_mode = True
            return_mode = False
            ev3.speaker.say("Follow mode")

        elif press_count == 2:
            follow_mode = False
            return_to_base()

        elif press_count == 3:
            follow_mode = False
            return_mode = False
            robot.stop()
            ev3.speaker.say("Stopped")
            press_count = 0

        while touch_sensor.pressed():
            wait(10)

        wait(500)

    if follow_mode:
        follow_target()

    elif return_mode:
        follow_target()

    else:
        robot.stop()

    wait(200)