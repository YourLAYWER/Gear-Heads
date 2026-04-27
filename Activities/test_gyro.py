#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor, Motor
from pybricks.parameters import Port, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Initialize the brick, motors, and sensor
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
gyro = GyroSensor(Port.S1)

# Initialize DriveBase (wheel_diameter, axle_track)
robot = DriveBase(left_motor, right_motor, 56, 121)

# Reset the gyro while still
ev3.speaker.beep()
gyro.reset_angle(0)

print("Manual Control Mode Active.")
print("Use Brick Buttons to move.")

while True:
    # 1. Update the Screen with Gyro Data
    angle = gyro.angle()
    ev3.screen.clear()
    ev3.screen.draw_text(0, 10, "Angle: " + str(angle))
    ev3.screen.draw_text(0, 40, "UP: Fwd | DN: Back")
    ev3.screen.draw_text(0, 60, "L/R: Turn")

    # 2. Check for Button Presses
    pressed = ev3.buttons.pressed()

    if Button.UP in pressed:
        ev3.speaker.beep(1000, 50)
        robot.straight(100)  # Move forward 100mm
    
    elif Button.DOWN in pressed:
        ev3.speaker.beep(800, 50)
        robot.straight(-100) # Move backward 100mm
    
    elif Button.LEFT in pressed:
        ev3.speaker.beep(1200, 50)
        robot.turn(-90)      # Turn left 90 degrees
    
    elif Button.RIGHT in pressed:
        ev3.speaker.beep(1200, 50)
        robot.turn(90)       # Turn right 90 degrees
    
    elif Button.CENTER in pressed:
        # Reset the gyro angle to zero manually
        gyro.reset_angle(0)
        ev3.speaker.beep(400, 500)
        wait(500)

    # Small wait to keep the loop stable
    wait(10)