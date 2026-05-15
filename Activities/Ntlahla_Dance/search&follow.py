#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()
#----------------------------------
# Motors
#-----------------------------
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, 56, 121)

touch_sensor = TouchSensor(Port.S2)

ev3.speaker.say("Press to start")

# Wait for first press
while not touch_sensor.pressed():
    wait(10)

# Small delay so one press is not counted twice
wait(500)

ev3.speaker.say("Moving")

# Start driving forever
robot.drive(150, 0)

# Wait until button pressed again
while not touch_sensor.pressed():
    wait(10)

# Stop robot
robot.stop()

ev3.speaker.say("Stopped")