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

# Your specific calibrated dimensions
robot = DriveBase(left_motor, right_motor, 56, 121)
ev3.speaker.set_volume(100)

# --- 1. START MUSIC ---
try:
    # Start music immediately
    ev3.speaker.play_file('118.wav', wait=False)
except:
    # If file is missing, beep so you know the script is running
    ev3.speaker.beep()

# --- 2. TRIGGER LOGIC (Pattern-Safe) ---
ev3.screen.draw_text(0, 40, "PLACE ON WHITE")

# We use 40 as a 'Safe White' trigger. 
# It's bright enough to be white, but won't be blocked by light lines.
while line_sensor.reflection() < 40:
    wait(10)

# --- 3. DANCE (From raise.py and turn_360.py) ---
ev3.screen.clear()
ev3.screen.draw_text(0, 40, "DANCING!")
lift_motor.reset_angle(0)

# We use a loop of 5 to ensure it doesn't shut down if the music file fails
for i in range(5):
    # Raise (Target 110 from raise.py)
    # wait=False allows lifting and turning at the same time
    lift_motor.run_target(150, 110, wait=False) 
    
    # Turn 360 (From turn_360.py)
    robot.turn(360) 
    
    # Lower (Target 0 from lower.py)
    lift_motor.run_target(150, 0)
    
    # Pause for stability (From turn_360.py)
    wait(1000)

# --- 4. FINISH ---
robot.stop()
lift_motor.stop()
ev3.speaker.beep(frequency=1000, duration=500)