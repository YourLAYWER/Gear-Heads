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


ev3.speaker.beep()

# Move forward
robot.straight(300)
wait(500)

# Move backward
robot.straight(-300)
wait(500)

robot.stop()
ev3.speaker.beep()