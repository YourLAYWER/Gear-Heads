#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.ev3devices import Motor
from pybricks.ev3devices import ColorSensor
from pybricks.robotics import DriveBase

#Constants First
DRIVE_SPEED = 30  #Measured in mm/s   
PROPORTIONAL_GAIN = 1.8 #Determines wobbliness/sluggishness of the bot.
LIFT_UP_ANGLE = 90     # The absolute angle representing the "up" position
LIFT_DOWN_ANGLE = 0    # The absolute angle representing the "down" position

#Variables
ev3 = EV3Brick()
gyro = GyroSensor(Port.S1)
line_sensor = ColorSensor(Port.S3)
lift_motor = Motor(Port.A)
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
robot = DriveBase(left_motor, right_motor, 56, 121)
wheel_diameter = 56      
axle_track = 121
distance_covered = 0 #Initialize distance(To be used as a measurement at multiple points during operation)
robot.settings(straight_speed=200, turn_rate=90)

#First block of code is intended to reset the gyro sensor.
#Commented out gyro lines because I'm not sure of their necessity at the moment.
'''
gyro.reset_angle(0)
print(gyro.angle())
wait(1000)
'''

##INITIALISATION STARTS
#Set Black
ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on BLACK")
ev3.screen.draw_text(0, 50, "Press any btn") 
while len(ev3.buttons.pressed()) == 0:
wait(10)
black_value = line_sensor.reflection()
ev3.speaker.beep(500, 200)

#Debounce command follows, ensures that the user isn't pressing anything
while len(ev3.buttons.pressed()) > 0:  
wait(10)

#Set White
ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on WHITE")
ev3.screen.draw_text(0, 50, "Press any btn")
while len(ev3.buttons.pressed()) == 0:
wait(10)
white_value = line_sensor.reflection()
ev3.speaker.beep(1000, 200)

#Debounce again
while len(ev3.buttons.pressed()) > 0:
wait(10)
return black_value, white_value

#Calculations for initialization
TARGET_THRESHOLD = (black_value + white_value) / 2

# Display results
ev3.screen.clear()
ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
ev3.screen.draw_text(0, 60, "Thr: " + str(TARGET_THRESHOLD)) 
print("Calibration Complete. Threshold:", TARGET_THRESHOLD)
wait(3000)
##INITIALISATION DONE

#Lower the bar 100% 
ev3.screen.draw_text(0, 30, "Lowering the bar")
lift_motor.reset_angle(0)
lift_down()

#Move toward the car
move(1000)
distance_covered += 1000

#Raise the bar 100%
ev3.screen.draw_text(0, 30, "Raising The bar")
lift_up()

#Turn Towards the road
turn(-90)
distance_covered +- 90

#Next block follows the line forward until the end.(Using color sensor)
def color_move(distance_covered):    
    while True:
        if(distance_covered == 1500):
            break      
        ev3.speaker.beep()
        ev3.screen.clear()
        ev3.screen.draw_text(0, 50, "Following Line...")
        current_reflection = line_sensor.reflection()
        error = current_reflection - TARGET_THRESHOLD
        steering = error * PROPORTIONAL_GAIN
        robot.drive(DRIVE_SPEED, steering)
        wait(50)
        distance_covered += 1

color_move(distance_covered)

#Lower the bar 100% (Car drop off)
ev3.screen.draw_text(0, 30, "Lowering the bar")
lift_down()

#Move back (Out of the way fo the car)
move(-400)
#Turn Around (180 Degrees)
turn(180)

#Follow the line back (To the pick up point)
trip_two_distance = 0 #To be used as the new distance_covered variable
color_move(trip_two_distance)

#Beep to indicate the end of the road


#Implementation of victory sound will follow. Still yet to find a sound to use.




