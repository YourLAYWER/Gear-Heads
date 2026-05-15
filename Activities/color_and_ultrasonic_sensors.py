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
from pybricks.parameters import Port, Color
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
TARGET_DISTANCE = 150
SPEED_GAIN = 1.8

COLOR_GAIN = 1.3
THRESHOLD = 5
WIDTH = 400
LENGTH = 500

def measure_grey():
    ev3.screen.clear()
    ev3.screen.draw_text(0,20, "Place on Black")
    ev3.screen.draw_text(0,50, "Press any button")
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    black = line_sensor.reflection()

    ev3.screen.clear()
    ev3.screen.draw_text(0,20, "Place on White")
    ev3.screen.draw_text(0,50, "Press any button")
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    white = line_sensor.reflection()

    #Calculating the grey area/ THRESHOLD
    value = (black+white)/2

    # Display results
    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "Blk: " + str(black))
    ev3.screen.draw_text(0, 30, "Wht: " + str(white))
    ev3.screen.draw_text(0, 60, "Thr: " + str(value))

    return value

def arc_search(max_angle=180,speed=50):
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


def avoid_obstacle(width=200, length=300):
    ev3.speaker.beep()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Avoiding Obsticle...")
    robot.turn(90)
    robot.straight(width)
    robot.turn(-90)
    robot.straight(length)
    robot.turn(-90)
    robot.straight(width+(width*0.15))
    robot.turn(90)
    wait(2000)
    
def drive_robot(max_speed=65,red_value):
    ev3.speaker.beep()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Following Line...")
    ev3.speaker.say("starting self driving procedure")
    while True:

        # if line_sensor.distance() == Color.RED:
        #     robot.stop()
        #     ev3.speaker.say("Mission complete")
        #     break


        current_distance = ultrasonic.distance()
        error = current_distance - TARGET_DISTANCE
        drive_speed = error * SPEED_GAIN
        

        current_reflection = line_sensor.reflection()
        color_error = current_reflection - THRESHOLD
        steering = color_error * COLOR_GAIN
        
        if current_distance < TARGET_DISTANCE+10:

            robot.stop()
            ev3.speaker.say("Obsticle Detected")
            wait(1000)
            current_distance = ultrasonic.distance()
            if current_distance < TARGET_DISTANCE+10:

                ev3.speaker.say("Initiating Obsticle avoidance procedure")
                avoid_obstacle()
                wait(2000)
                found = arc_search()
            
                if not found:
                    robot.stop()
                    break
                else:
                    continue
            
        
        if drive_speed > max_speed:
            drive_speed = max_speed
        
        robot.drive(drive_speed, steering)
        wait(10)

####################### this code is for calculating the THRESHOLD ##########################      
ev3.screen.clear()
ev3.screen.draw_text(0,20, "Place on Black")
ev3.screen.draw_text(0,50, "Press any button")
while len(ev3.buttons.pressed()) == 0:
    wait(5)
    
black_value = line_sensor.reflection()

while len(ev3.buttons.pressed()) > 0:
    wait(10)
ev3.speaker.beep()


# measure white
ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on WHITE")
ev3.screen.draw_text(0, 50, "Press any btn")
while len(ev3.buttons.pressed()) == 0:
    wait(5)

white_value = line_sensor.reflection()

while len(ev3.buttons.pressed()) > 0:
    wait(10)
ev3.speaker.beep()

ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on Red")
ev3.screen.draw_text(0, 50, "Press any btn")
while len(ev3.buttons.pressed()) == 0:
    wait(5)

red_value = line_sensor.reflection()

while len(ev3.buttons.pressed()) > 0:
    wait(10)
ev3.speaker.beep()

THRESHOLD = (black_value + white_value) / 2  

# Display results
ev3.screen.clear()
ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
ev3.screen.draw_text(0, 30, "Red: " + str(red_value))
ev3.screen.draw_text(0, 60, "Thr: " + str(THRESHOLD))

ev3.speaker.beep(1000, 200)  # end of THRESHOLD calculation
print("calibration complete")
wait(5)
drive_robot(red_value)
