#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

#Constants First
DRIVE_SPEED = 30     
PROPORTIONAL_GAIN = 1.8 #Determines wobbliness/sluggishness of the bot.

#First block of code is intended to reset and initialise the bot itself.

ev3 = EV3Brick()
'''
gyro = GyroSensor(Port.S1)
gyro.reset_angle(0)
print(gyro.angle())
wait(1000)
'''

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

print("Start")

##INITIALISATION STARTS

#Prep & initialise the color sensor.
line_sensor = ColorSensor(Port.S3)
robot = DriveBase(left_motor, right_motor, 56, 121) 

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

#Calculations for initialization
TARGET_THRESHOLD = (black_value + white_value) / 2

# Display results
ev3.screen.clear()
ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
ev3.screen.draw_text(0, 60, "Thr: " + str(TARGET_THRESHOLD))
ev3.screen.clear()
ev3.screen.draw_text("Calibration Complete. Threshold: ", TARGET_THRESHOLD)
wait(3000) 

ev3.screen.clear()
ev3.screen.draw_text("Got here lol")

##INITIALISATION DONE

ev3.screen.draw_text("Lowering the bar")

#Lower the bar 100% 
lift_motor = Motor(Port.A)
lift_motor.run_target(100, -1)

#Next block follows the line forward until the end.(Using color sensor)
ev3.speaker.beep()
ev3.screen.clear()
ev3.screen.draw_text(0, 50, "Following Line...")
current_reflection = line_sensor.reflection()
error = current_reflection - TARGET_THRESHOLD
steering = error * PROPORTIONAL_GAIN
robot.drive(DRIVE_SPEED, steering)
wait(50)
ev3.screen.draw_text("Time to TOW!")

#Raise the bar 100%
lift_motor = Motor(Port.A)
lift_motor.reset_angle(0)
lift_motor.run_target(100, 110)

#Turn Around (180 Degrees)
#Kinematic setup for accuracy first.
wheel_diameter = 56      
axle_track = 121      
robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

#Actual movement
ev3.speaker.beep()
sequence_count = 2 #Changed sequence count from 3 to 1 to turn once, monitor this effect
#Chaned to 2 to see if it has any effect on functioning
for i in range(sequence_count):
    print("Sequence " + str(i + 1) + ": Turning 180 degrees Right (Clockwise)")
    robot.turn(180)
    wait(1000)
ev3.speaker.beep(frequency=1000, duration=500) #Higher pitched beep indicates completion.

#Follow the line back (To the drop off point)
ev3.speaker.beep()
ev3.screen.clear()
ev3.screen.draw_text(0, 50, "Following Line...")
current_reflection = line_sensor.reflection()
error = current_reflection - TARGET_THRESHOLD
steering = error * PROPORTIONAL_GAIN
robot.drive(DRIVE_SPEED, steering)
wait(50)
ev3.screen.draw_text("Drop off time.")

#Lower the bar 100%
lift_motor = Motor(Port.A)
lift_motor.run_target(100, -1)

#Implementation of victory sound will follow. Still yet to find a sound to use.




