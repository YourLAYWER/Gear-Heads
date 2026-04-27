#!/usr/bin/env pybricks-micropython
"""
Demonstrates interactive Color Sensor calibration and implements a basic 
Proportional (P) control loop to follow the edge of a line.
"""

# =============================================================================
# IMPORTS AND SETUP
# =============================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, GyroSensor, UltrasonicSensor
from pybricks.parameters import Port
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

COLOR_GAIN = 2
SPEED_GAIN = 0.3
THRESHOLD = 5
Width = 400
Length = 500

def measure_black():
    ev3.screen.clear()
    ev3.screen.draw_text(0,20, "Place on Black")
    ev3.screen.draw_text(0,50, "Press any button")
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    value = line_sensor.reflection()
    return value




def arc_search(max_angle=180,speed=5):
    gyro_sensor.reset_angle(0)
    robot.drive(0, speed)
    
    while line_sensor.reflection() > THRESHOLD and abs(gyro_sensor.angle()) < max_angle:
        wait(5)
        
    robot.stop()
    
    if line_sensor.reflection() <= THRESHOLD:
        return True
    else:
        return False


def avoid_obsticle(width, length):
    robot.turn(90)
    robot.straight(width)
    robot.turn(-90)
    robot.straight(length)
    robot.turn(-90)
    robot.straight(width-(width*0.3))
    robot.turn(90)
    
def drive_robot(width,length):

    while True:
        current_distance = ultrasonic.distance()
        error = current_distance - TARGET_DISTANCE
        drive_speed = error * SPEED_GAIN
        
        current_reflection = line_sensor.reflection()
        color_error = current_reflection - THRESHOLD
        steering = color_error*COLOR_GAIN
        
        if current_distance < TARGET_DISTANCE+2:
            avoid_obsticle(width, length)
            
            found = arc_search()
            
            if not found:
                break
            continue
        
        robot.drive(drive_speed, steering)
        wait(3)
        

THRESHOLD = measure_black()

drive_robot(Width,Length)

##This is line following code
# while True:
#     current_reflection = color_sensor.reflection()
    
#     error = current_reflection - THRESHOLD
    
#     steering = error * TURN_GAIN
    
#     robot.drive(DRIVE_SPEED, steering)
# This is the Ultrasonic sensor code that stop the robot from colliding with things


# while True:
#     current_distance = obstacle_sensor.distance()
#     error = current_distance - TARGET_DISTANCE
#     drive_speed = error * GAIN
#     robot.drive(drive_speed,0)
#     wait(10)
