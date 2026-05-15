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

# Distance limit (mm)
STOP_DISTANCE = 200

ev3.speaker.say("Press to start")

# Wait for button
while not touch_sensor.pressed():
    wait(10)

wait(500)

ev3.speaker.say("Moving")

# Start moving
robot.drive(150, 0)

while True:

    distance = ultrasonic.distance()

    print(distance)

    # Object detected close
    if distance < STOP_DISTANCE:

        robot.stop()

        ev3.speaker.say("Object")

        break

    wait(50)