#!/usr/bin/env pybricks-micropython

# =========================================================
# HUMANOID EV3 DANCE
# =========================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

ev3 = EV3Brick()

#--------------------
# MUSIC SETUP
#--------------------

# try: 
#     ev3.speaker.play_file("music.mp3, wait=False")
# except:
#     ev3.speaker.beep()

# MOTOR SETUP 
left_leg = Motor(Port.B)
right_leg = Motor(Port.C)
right_arm = Motor(Port.A)  
# left_arm = Motor(Port.D)

#------------
# COUNTDOWN
#---------------

def countdown():
    for _ in range(3):
        ev3.speaker.beep()
        wait(500)

#-------------------
# DANCE MOVES
#----------------------

# Stretch
# def stretch():
#     left_leg.run_angle(200, 120, wait=False)
#     right_leg.run_angle(200, -120)

# Step left
def step_left():
    left_leg.run_angle(300, 90, wait=False)
    right_leg.run_angle(300, -90)

# Step right
def step_right():
    left_leg.run_angle(300, -90, wait=False)
    right_leg.run_angle(300, 90)

# Bounce (small up/down motion)
def bounce():
    left_leg.run_angle(400, 45, wait=False)
    right_leg.run_angle(400, 45)
    left_leg.run_angle(400, -45, wait=False)
    right_leg.run_angle(400, -45)

# Right arm swing
def right_arm_swing():
    right_arm.run_angle(400, 180)
    right_arm.run_angle(400, -180)

# Left arm swing
# def left_arm_swing():
#     left_arm.run_angle(400, 180)
#     left_arm.run_angle(400, -180)

# Move back to initial position
# def reset_initial_position():
#     left_leg.run_back(300,0, wait=False)
#     right_leg.run_back(300,0,wait=False)

# ---------------------------------------------------------
# START
# ---------------------------------------------------------

ev3.screen.clear()
ev3.screen.draw_text(20, 50, "Ready!")

wait(400)
countdown()

# Eyes
ev3.screen.clear()
ev3.screen.draw_circle(40, 50, 10)
ev3.screen.draw_circle(90, 50, 10)

# Eyes pupils
ev3.screen.draw_circle(40, 50, 5, fill=True)
ev3.screen.draw_circle(90, 50, 5, fill= True)

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
while True:

    # stretch()
    # wait(300)
    
    # reset_initial_position()
    # wait(300)

    step_left()
    wait(300)

    step_right()
    wait(300)

    bounce()
    wait(200)

    right_arm_swing()
    wait(200)

    # left_arm_swing()
    # wait(200)