#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor, Motor
from pybricks.parameters import Port, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# The ColorSensor outputs a reflection value between 0 (dark) and 100 (light).
line_sensor = ColorSensor(Port.S3)

robot = DriveBase(left_motor, right_motor, 56, 121)

ultrasonic = UltrasonicSensor(Port.S4)

gyro_sensor= GyroSensor(Port.S1)


####################### Here is where my code starts ############################
DRIVE_SPEED = 2
TARGET_DISTANCE = 15
SPEED_GAIN = 2

COLOR_GAIN = 1.6
THRESHOLD = 5
WIDTH = 400
LENGTH = 500

def arc_search(max_angle=180,speed=20):
    ev3.speaker.beep()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Searching for line...")
    gyro_sensor.reset_angle(0)
    robot.drive(0, speed)
    
    while line_sensor.reflection() > THRESHOLD and abs(gyro_sensor.angle()) < max_angle:
        wait(5)
        
    robot.stop()
    if line_sensor.reflection() <= THRESHOLD:
        wait(5)
        return True
    else:
        return False


ev3.screen.clear()
ev3.screen.draw_text(0,20, "Place on Black")
ev3.screen.draw_text(0,50, "Press any button")
while len(ev3.buttons.pressed()) == 0:
    wait(10)
    
black_value = line_sensor.reflection()

ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on WHITE")
ev3.screen.draw_text(0, 50, "Press any btn")
while len(ev3.buttons.pressed()) == 0:
    wait(10)

white_value = line_sensor.reflection()

while len(ev3.buttons.pressed()) > 0:
    wait(10)

THRESHOLD = (black_value + white_value) / 2

ev3.speaker.beep(1000, 200)

value = arc_search()
if value:
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Line FOUND")
    robot.stop()
else:
    ev3.screen.draw_text(0, 50, "Line not found")
    robot.stop()

