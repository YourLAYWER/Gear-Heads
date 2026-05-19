#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, 56, 121)

touch_sensor = TouchSensor(Port.S2)
ultrasonic = UltrasonicSensor(Port.S4)

TARGET_DISTANCE = 50
MAX_DISTANCE = 600
MOVE_SPEED = 80

ev3.speaker.say("Press")

while not touch_sensor.pressed():
    wait(10)

wait(700)
ev3.speaker.say("Follow mode")

while True:
    distance = ultrasonic.distance()
    print(distance)

    if TARGET_DISTANCE < distance < MAX_DISTANCE:
        robot.drive(MOVE_SPEED, 0)

    elif 0 < distance <= TARGET_DISTANCE:
        robot.stop()

    else:
        robot.stop()

        wait(500)

        robot.urn(-20)

        distance = ultrasonic.distance()

        if TARGET_DISTANCE < distance < MAX_DISTANCE:
            continue

        robot.turn(40)

        distance = ultrasonic.distance()

        if TARGET_DISTANCE < distance < MAX_DISTANCE:
            continue

        robot.turn(-20)
        
    wait(200)