#!/usr/bin/env python3
from time import sleep
from ev3dev2.motor import MoveTank, LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent

driveSpeed = SpeedPercent(100)
turnSpeed = [SpeedPercent(30), SpeedPercent(-30)]  # Right and left
turnDegrees = 90


backMotors = MoveTank(left_motor_port=OUTPUT_A, right_motor_port=OUTPUT_D, motor_class=LargeMotor)  # Motor on output port A and D
#motor1 = LargeMotor(address=OUTPUT_A)
driveMotor = MediumMotor(address=OUTPUT_B)  # Motor on output port B


if __name__ == '__main__':
    # backMotors.on(left_speed=driveSpeed, right_speed=driveSpeed)

    while True:
        driveMotor.on_for_degrees(speed=turnSpeed[1], degrees=turnDegrees)
        sleep(1)
        driveMotor.on_for_degrees(speed=turnSpeed[0], degrees=turnDegrees)
        sleep(1)
        backMotors.on_for_degrees(left_speed=driveSpeed, right_speed=driveSpeed, degrees=360)
        sleep(1)
