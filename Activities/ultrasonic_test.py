#!/usr/bin/env pybricks-micropython
"""
Demonstrates interactive Color Sensor calibration and implements a basic 
Proportional (P) control loop to follow the edge of a line.
"""

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
gyro_sensor = GyroSensor(Port.S1)

####################### Constants ############################
TARGET_DISTANCE = 80
SPEED_GAIN = 1.8
COLOR_GAIN = 1.2

def measure_threshold():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on Black")
    ev3.screen.draw_text(0, 50, "Press any button")
    
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    black_value = line_sensor.reflection()

    while len(ev3.buttons.pressed()) > 0:
        wait(10)
    ev3.speaker.beep()

    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on White")
    ev3.screen.draw_text(0, 50, "Press any button")
    
    while len(ev3.buttons.pressed()) == 0:
        wait(10)
    
    white_value = line_sensor.reflection()

    while len(ev3.buttons.pressed()) > 0:
        wait(10)
    ev3.speaker.beep()

    # Calculating the grey area / THRESHOLD
    threshold_value = (black_value + white_value) / 2

    # Display results
    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "Blk: " + str(black_value))
    ev3.screen.draw_text(0, 30, "Wht: " + str(white_value))
    ev3.screen.draw_text(0, 60, "Thr: " + str(threshold_value))

    return threshold_value


def arc_search(threshold_val, max_angle=180, speed=45):
    ev3.speaker.beep()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Searching for line...")
    gyro_sensor.reset_angle(0)
    robot.drive(0, speed)
    
    while line_sensor.reflection() > threshold_val and abs(gyro_sensor.angle()) < max_angle:
        wait(5)
        
    robot.stop()
    
    if line_sensor.reflection() <= threshold_val:
        wait(5)
        return True
    else:
        return False


def avoid_obstacle(width=200, length=300):
    ev3.speaker.beep()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Avoiding Obstacle...")
    robot.turn(90)
    wait(100)
    robot.straight(width)
    wait(100)
    robot.turn(-90)
    wait(100)
    robot.straight(length)
    wait(100)
    robot.turn(-90)
    wait(100)
    robot.straight(width + (width * 0.15))
    wait(100)
    robot.turn(90)
    wait(1000)
    
    
def drive_robot(threshold_val, target_distance, color_gain, speed_gain, max_speed=80):
    ev3.speaker.beep()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Following Line...")
    ev3.speaker.say("starting self driving procedure")
    
    while True:
        current_distance = ultrasonic.distance()
        error = current_distance - target_distance
        drive_speed = error * speed_gain
        
        current_reflection = line_sensor.reflection()
        color_error = current_reflection - threshold_val
        steering = color_error * color_gain
        
        if current_distance < target_distance + 10:
            robot.stop()
            ev3.speaker.say("Obstacle Detected")
            wait(1000)
            current_distance = ultrasonic.distance()
            
            if current_distance < target_distance + 10:
                ev3.speaker.say("Initiating Obstacle avoidance procedure")
                avoid_obstacle()
                wait(1000)
                found = arc_search(threshold_val)
            
                if not found:
                    robot.stop()
                    break
                else:
                    continue
            
        if drive_speed > max_speed:
            drive_speed = max_speed
        
        robot.drive(drive_speed, steering)
        wait(10)

####################### Execution ##########################      

THRESHOLD = measure_threshold()

ev3.speaker.beep(1000, 200)  # end of THRESHOLD calculation
print("Calibration complete. Threshold:", THRESHOLD)
wait(5)

# Note: max_speed defaults to 150 now instead of 65.
drive_robot(THRESHOLD, TARGET_DISTANCE, COLOR_GAIN, SPEED_GAIN)