#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor,GyroSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# --- INITIALIZATION ---
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
lift_motor = Motor(Port.A)
line_sensor = ColorSensor(Port.S3)
ultrasonic = UltrasonicSensor(Port.S4)
gyro = GyroSensor(Port.S1)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=121)

def main():
    # =========================================================================
    # 1. LIFT FIRST (Before Calibration)
    # =========================================================================
    ev3.speaker.beep()
    print("Lifting object...")
    lift_motor.reset_angle(0)
    lift_motor.run_target(200, 110) # Lift to your 110 degree target

    # =========================================================================
    # 2. CALIBRATION (Teaching the robot your Black and White)
    # =========================================================================
    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on BLACK") # This is your Black line
    while len(ev3.buttons.pressed()) == 0: wait(10)
    black_value = line_sensor.reflection() 
    ev3.speaker.beep(500, 200)
    while len(ev3.buttons.pressed()) > 0: wait(10)

    ev3.screen.clear()
    ev3.screen.draw_text(0, 20, "Place on WHITE") # This is your white Floor
    while len(ev3.buttons.pressed()) == 0: wait(10)
    white_value = line_sensor.reflection()
    ev3.speaker.beep(1000, 200)
    while len(ev3.buttons.pressed()) > 0: wait(10)

    # Calculate the Threshold Edge
    TARGET_THRESHOLD = (black_value + white_value) / 2

    # =========================================================================
    # 3. SETTINGS & LINE FOLLOWING
    # =========================================================================
    DRIVE_SPEED = 100 
    PROPORTIONAL_GAIN = 1.4#Steering wheel sensitivity

    # ev3.screen.clear()
    ev3.screen.draw_text(0, 40, "PLACE ON EDGE")
    # ev3.speaker.beep(1500, 500)
    # wait(2000) # Give you 2 seconds to place it on the edge before it moves
    

    while True:
        current_reflection = line_sensor.reflection()
        # Check for 90-Degree Turn (Detecting the crossing line)
        if current_reflection < (black_value + 5):#If see anything darker
            robot.stop()
            ev3.speaker.beep()
            gyro.reset_angle(0)
            robot.drive(0, 40) # rotation speed of 40
            while abs(gyro.angle()) < 90:#while less than 90 always check during turning
                wait(1)
            robot.stop()
            continue 

        # Check for End of Line (Dropping off onto pure white floor)
        if current_reflection > (white_value - 2):#If it is pure white stop
            robot.stop()
            break 
        
        # C. Proportional Steering(Ensures that it stays on the line instead of woobling)
        error = current_reflection - TARGET_THRESHOLD
        steering = error * PROPORTIONAL_GAIN
        robot.drive(DRIVE_SPEED, steering)#Drive at 100 while doing steering calc.
        wait(10)

    # =========================================================================
    # 4. FINAL DROP
    # =========================================================================
    lift_motor.run_target(200, 0)
    ev3.speaker.say("Mission complete")

if __name__ == "__main__":
    main()