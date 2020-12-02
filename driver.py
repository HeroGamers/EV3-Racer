from time import sleep
from ev3dev2.motor import MoveTank, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent

driveSpeed = SpeedPercent(100)
turnSpeed = [SpeedPercent(30), SpeedPercent(-30)]  # Right and left
turnDegrees = 90


backMotors = MoveTank(left_motor_port=OUTPUT_A, right_motor_port=OUTPUT_D)  # Motor on output port A and D
driveMotor = MediumMotor(address=OUTPUT_B)  # Motor on output port B

backMotors.on(left_speed=driveSpeed, right_speed=driveSpeed)

while True:
    driveMotor.on_for_degrees(speed=turnSpeed[1], degrees=turnDegrees)
    sleep(1)
    driveMotor.on_for_degrees(speed=turnSpeed[0], degrees=turnDegrees)
    sleep(1)