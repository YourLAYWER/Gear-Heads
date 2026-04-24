#!/usr/bin/env pybricks-micropython

# =========================================================
# HUMANOID EV3 DANCE
# =========================================================

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

ev3 = EV3Brick()

# ---------------------------------------------------------
# MOTOR SETUP 
# ---------------------------------------------------------
left_leg = Motor(Port.B)
right_leg = Motor(Port.C)
arm_motor = Motor(Port.A)  

# ---------------------------------------------------------
# COUNTDOWN
# ---------------------------------------------------------
def countdown():
    for _ in range(3):
        ev3.speaker.beep()
        wait(500)

# ---------------------------------------------------------
# DANCE MOVES
# ---------------------------------------------------------

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

# Arm swing
def arm_swing():
    arm_motor.run_angle(400, 180)
    arm_motor.run_angle(400, -180)

# ---------------------------------------------------------
# START
# ---------------------------------------------------------

ev3.screen.clear()
ev3.screen.draw_text(20, 50, "Ready!")

wait(2000)
countdown()

ev3.screen.clear()
ev3.screen.draw_text(20, 50, "Dancing!")

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
while True:

    step_left()
    wait(300)

    step_right()
    wait(300)

    bounce()
    wait(200)

    arm_swing()
    wait(200)