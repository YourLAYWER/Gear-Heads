#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --- INITIALIZATION (From turn_360.py) ---
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor = Motor(Port.A)
line_sensor = ColorSensor(Port.S3)

# calibrated dimensions
robot = DriveBase(left_motor, right_motor, 56, 121)
ev3.speaker.set_volume(100)

# --- 1. START MUSIC ---
try:
    # Start music immediately
    ev3.speaker.play_file("118.wav")
except:
    # If file is missing, beep so you know the script is running
    ev3.screen.draw_text(20, 50, "Eish")

ev3.screen.draw_text(0, 40, "PLACE ON WHITE")

# 
while line_sensor.reflection() < 30:
    wait(10)

# (From raise.py and turn_360.py)
ev3.screen.clear()
ev3.screen.draw_text(0, 40, "DANCING!")
lift_motor.reset_angle(0)#You are standing at angle 0. 

# We use a loop of 5 to ensure it doesn't shut down if the music file fails
for i in range(5):#Repeat process 5 times
    # (Target 110 from raise.py)
    # wait=False allows lifting and turning at the same time
    lift_motor.run_target(150, 110, wait=False)#Raise to 110 at 150 speed.
    
    #(From turn_360.py)
    robot.turn(360) 
    
    #(Target 0 from lower.py)
    lift_motor.run_target(150, 0)#Lower at 150 speed
    
    # Pause for stability (From turn_360.py)
    wait(1000)

# --- 4. FINISH ---
robot.stop()
lift_motor.stop()
ev3.speaker.beep(frequency=1000, duration=500)