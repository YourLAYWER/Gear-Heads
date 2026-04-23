#!/usr/bin/env pybricks-micropython
"""
Demonstrates interactive Color Sensor calibration and implements a basic 
Proportional (P) control loop to follow the edge of a line.
"""

# =============================================================================
# IMPORTS AND SETUP
# =============================================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# The ColorSensor outputs a reflection value between 0 (dark) and 100 (light).
line_sensor = ColorSensor(Port.S3)

robot = DriveBase(left_motor, right_motor, 56, 121)

ultrasonic = UltrasonicSensor(Post.S4)

gyro_sensor= GyroSensor(Port.S1)

motorC = Motor(Port.C) # Magnet

####################### Here is where my code starts ############################
DRIVE_SPEED = 60
TARGET_DISTANCE = 5
COLOR_GAIN = 2
SPEED_GAIN = 1.1
THRESHOLD = 50
Width = 400
Length = 500

def arc_search(max_angle=180,speed=120):
    gyro_sensor.reset_angle(0)
    robot.drive(0, speed)
    
    while color_sensor.reflection() > THRESHOLD and abs(gyro_sensor.angle()) < max_angle:
        wait(5)
        
    robot.stop()
    
    if color_sensor.reflection() <= THRESHOLD:
        return True
    else:
        return False


def avoid_obsticle(width, length):
    robot.turn(90)
    #robot.wait(1000)
    robot.straight(width)
    #robot.wait(1000)
    robot.turn(-90)
    robot.straight(length)
    #robot.wait(1000)
    robot.turn(-90)
    robot.straight(width-(width*0.3))
    #robot.wait(1000)
    robot.turn(90)
    
def drive_robot(width,length):

    while True:
        current_distance = obstacle_sensor.distance()
        error = current_distance - TARGET_DISTANCE
        drive_speed = error * SPEED_GAIN
        
        current_reflection = color_sensor.reflection()
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
