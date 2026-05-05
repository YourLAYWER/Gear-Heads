#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

# MOTOR SETUP
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor = Motor(Port.A)  

robot = DriveBase(left_motor, right_motor, 56, 121)

# SENSOR SETUP
line_sensor = ColorSensor(Port.S3)
ultrasonic = UltrasonicSensor(Port.S4)
gyro_sensor = GyroSensor(Port.S1)


# -------------------------
# LIFT FUNCTIONS
# -------------------------

def lower_lever():
    lift_motor.run_angle(200, -90)

def raise_lever():
    lift_motor.run_angle(200, 90)

# -------------------------
# OBJECT DETECTION
# -------------------------

def object_in_front():
    distance = ultrasonic.distance() 

    if distance < 150:
        return True
    else:
        return False

# -------------------------
# MAIN PROGRAM
# -------------------------

raise_lever()
ev3.speaker.beep()

while True:

    robot.drive(100, 0)

    if object_in_front():
        robot.stop()
        ev3.speaker.beep()

        robot.straight(40)

        lower_lever()
        wait(500)

        robot.straight(-500)   

        robot.stop()
        ev3.speaker.beep()

        raise_lever()

        break

    wait(50)
