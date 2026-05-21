#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.ev3devices import Motor, TouchSensor
from pybricks.ev3devices import ColorSensor
from pybricks.robotics import DriveBase

#Constants First
DRIVE_SPEED = 80  #Measured in mm/s   
PROPORTIONAL_GAIN = 0.8 #Determines wobbliness/sluggishness of the bot.
LIFT_UP_ANGLE = 90     # The absolute angle representing the "up" position
LIFT_DOWN_ANGLE = 0    # The absolute angle representing the "down" position

#Variables
ev3 = EV3Brick()
#gyro = GyroSensor(Port.S1)
touch = TouchSensor(Port.S2)
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

###Method Definitions
def move_and_wait(distance, pause=2000):
    # Move the robot straight for the given distance.
    robot.straight(distance)
    # Pause after the movement.
    wait(pause)


def turn_and_wait(angle, pause=2000):
    # Turn the robot by the given angle.
    robot.turn(angle)
    # Pause after the turn.
    wait(pause)


def celebrate():
    ev3.speaker.beep()
    wait(300)
    ev3.speaker.beep()

def move(distance):
    """
    Drives the robot straight forward or backward.
    
    distance: The distance to travel in millimeters. 
              Positive values move forward, negative values reverse.
    """
    robot.straight(distance)
    # Pause for 1 second after moving to let momentum settle
    wait(1000)

def turn(angle):
    """
    Turns the robot in place.
    
    angle: The target angle to turn in degrees.
           Positive values turn right (clockwise), negative turn left.
    """
    robot.turn(angle)
    wait(1000)

def lift_up():
    """
    Moves the attachment to the predefined UP position.
    """
    # run_target moves the motor to an absolute angle (90 degrees), 
    # regardless of where it currently is, at a speed of 200 deg/s.
    lift_motor.run_target(200, LIFT_UP_ANGLE)
    wait(500)

def lift_down():
    """
    Moves the attachment to the predefined DOWN position.
    """
    # run_target returns the motor to the absolute 0 degree mark.
    lift_motor.run_target(200, LIFT_DOWN_ANGLE)
    wait(500)

def color_move(distance_covered):    
    while True:
        if(distance_covered == 1105):
            break
        ev3.screen.clear()
        ev3.screen.draw_text(0, 50, "Following Line...")
        current_reflection = line_sensor.reflection()
        error = current_reflection - TARGET_THRESHOLD
        steering = error * PROPORTIONAL_GAIN
        robot.drive(DRIVE_SPEED, steering)
        wait(50)
        distance_covered += 1

def touch_move():
     # Command the robot to drive forward indefinitely at 200 mm/s with 0 steering.
    # Because this is inside a while loop, it keeps refreshing the command.
    robot.drive(200, 0)

    # Poll the touch sensor. The .pressed() method returns a boolean (True/False).
    if touch.pressed():
        
        # Immediate reaction: Stop the motors to prevent pushing into the obstacle.
        robot.stop()

        # Output to the console for debugging purposes.
        print("Touch pressed! Obstacle detected.")

        # ---------------------------------
        # EXCEPTION HANDLING
        # ---------------------------------
        # Attempt to play a specific audio file. If the file "oopsy.wav" is missing 
        # from the EV3's file system, the program would normally crash. 
        # The try/except block catches this FileNotFoundError and safely defaults 
        # to a standard beep, keeping the robot operational.
        try:
             ev3.speaker.play_file("oopsy.wav")
        except:
            ev3.speaker.beep()

        # Wait 1.5 seconds (1500 ms) to let the sound finish playing
        wait(1500)

        # ---------------------------------
        # EVASIVE MANEUVER
        # ---------------------------------
        # Move backwards by 100 millimeters to clear the obstacle
        robot.straight(-100)

        # Brief pause to allow momentum to settle after turning
        wait(500)

        # ---------------------------------
        # STATE MANAGEMENT (DEBOUNCING)
        # ---------------------------------
        # 🔥 CRITICAL: If the robot backed up but the sensor is somehow STILL pressed 
        # (e.g., it got snagged, or a user is holding it), the loop would immediately 
        # trigger again. This nested while loop acts as a block, pausing the main 
        # program flow until the physical button is explicitly released.
        while touch.pressed():
            wait(10) # Check every 10ms, do nothing until False.

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
ev3.screen.clear()
ev3.screen.draw_text(0, 30, "Lowering the bar")
lift_motor.reset_angle(0)
lift_down()

#Move toward the car
move(780)
distance_covered += 900

#Raise the bar 100%
ev3.screen.draw_text(0, 30, "Raising The bar")
lift_up()

#Turn Towards the road
turn(-65)
distance_covered += 90
# Brief pause to allow momentum to settle after turning
wait(500)

#Next block follows the line forward until the end.(Using color sensor)
ev3.screen.clear()
move(900) 
wait(500)

#Lower the bar 100% (Car drop off)
ev3.screen.draw_text(0, 30, "Lowering the bar")
lift_down()

#Move back (Out of the way of the car)
move(-100)
wait(500)
#Turn Left (45 Degrees)
turn(-45)

#Follow the line to the end corner
trip_two_distance = 0 #To be used as the new distance_covered variable
move(200)

#Beep to indicate the end of the road
celebrate()




