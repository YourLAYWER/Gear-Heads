#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, GyroSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait,StopWatch

# =============================================================================
# 1. SETUP & INITIALIZATION
# =============================================================================
ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor = Motor(Port.A) 

# Sensors
line_sensor = ColorSensor(Port.S3)
gyro = GyroSensor(Port.S1)

# Robot Dimensions (Wheel Diameter: 56mm, Axle Track: 121mm)
robot = DriveBase(left_motor, right_motor, 56, 121)

# =============================================================================
# 2. CALIBRATION LOGIC
# =============================================================================
ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on BLACK")
ev3.screen.draw_text(0, 50, "Press any btn")

# Wait for Black reading
while len(ev3.buttons.pressed()) == 0:
    wait(10)
black_value = line_sensor.reflection()
ev3.speaker.beep(500, 200)
while len(ev3.buttons.pressed()) > 0: wait(10) # Debounce

ev3.screen.clear()
ev3.screen.draw_text(0, 20, "Place on WHITE")
ev3.screen.draw_text(0, 50, "Press any btn")

# Wait for White reading
while len(ev3.buttons.pressed()) == 0:
    wait(10)
white_value = line_sensor.reflection()
ev3.speaker.beep(1000, 200)
while len(ev3.buttons.pressed()) > 0: wait(10) # Debounce

# Calculate the Target Threshold (The edge of the line)
TARGET_THRESHOLD = (black_value + white_value) / 2

# 3. PRE-START LIFT (Lifting after calibration)
ev3.speaker.beep()
ev3.screen.draw_text(0, 50,"Lifting object...")
lift_motor.reset_angle(0)       #current position is 0
lift_motor.run_target(200, 110) # Raise to 110 degrees before moving(speed=200)

# Display calibration results
ev3.screen.clear()
ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
ev3.screen.draw_text(0, 60, "Thr: " + str(TARGET_THRESHOLD))

print("Calibration Complete. Threshold:", TARGET_THRESHOLD)
wait(2000) 

# =============================================================================
# 4. INTEGRATED P-CONTROL LOOP
# =============================================================================
DRIVE_SPEED = 60       
PROPORTIONAL_GAIN = 1.2#steering sensitivity
RUN_TIME_MS = 17220
ev3.speaker.beep()
ev3.screen.clear()
ev3.screen.draw_text(0, 50, "Following Line...")
timer = StopWatch()
while True:
    # Get current sensor reading
    if timer.time() > RUN_TIME_MS:
        break
    current_reflection = line_sensor.reflection()

    # Standard behavior: Move forward or search for line
    # (Insert your line-following logic here, for example:)
    robot.drive(60, 0) 

    #Calculate Error
    error = current_reflection - TARGET_THRESHOLD
    
    #Calculate Steering
    steering = error * PROPORTIONAL_GAIN
    
    #Apply drive
    robot.drive(DRIVE_SPEED, steering)
    
    wait(10)

# =============================================================================
# 5. FINAL DROP
# =============================================================================
robot.stop()#robot stops after 17.22 seconds
# This runs only after the robot sees white and breaks the loop
lift_motor.run_target(150, 0) # Go back to 0 degrees (the floor),speed=150
# Move back a set distance (e.g., 100mm)
robot.straight(-100) 

# --- TURN right ---
robot.turn(90)
while line_sensor.reflection() > TARGET_THRESHOLD:
    robot.drive(0, 20) # Slow, precise rotation (speed 20)
    wait(5)

robot.stop()
ev3.speaker.beep(600, 100)

# --- SECOND LINE FOLLOW (Same time as before) ---
print("Final 17.22 second stretch...")
timer.reset() # Reset the timer to start from 0 for the new move

while timer.time() < RUN_TIME_MS:
    current_reflection = line_sensor.reflection()
    error = current_reflection - TARGET_THRESHOLD
    steering = error * PROPORTIONAL_GAIN
    robot.drive(DRIVE_SPEED, steering) # Use line following again
    wait(10)

# CRITICAL: Stop immediately after the second 17.22 seconds
robot.stop()
ev3.speaker.say("Mission complete")
print("Mission complete")