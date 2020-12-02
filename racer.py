#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
import os
import sys
import collections
from time import sleep
import colorAPI


# Variables
driveSpeed = 100  # Speed in percent
turnDriveSpeed = 50  # Speed in percent
turnSpeed = 30  # Speed in percent
maxTurnDegrees = 90
backMotorsState = "off"
turning_direction = "none"
seenColorsTolerancePercent = 90
seenColors = collections.deque(maxlen=5)
driveDelay = 5.5  # Delay between each loop of driving

# The motors, sensors and other things on the robot
buttons = Button()  # Any buton on the robot
backMotors = MoveTank(left_motor_port=OUTPUT_A, right_motor_port=OUTPUT_D)  # Motor on output port A and D
driveMotor = MediumMotor(address=OUTPUT_B)  # Motor on output port B
sensor = ColorSensor(address=INPUT_1)  # Color sensor on input port 1


def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def setup():
    os.system('setfont Lat15-TerminusBold14')  # Sets the console font
    print('\x1Bc', end='')  # Resets the console
    print("Hello, World!")


def drive(color=None):
    global backMotorsState
    global turning_direction
    if not color:
        if (backMotorsState == "off") or (backMotorsState == "turning"):
            print("driving")
            backMotors.on(left_speed=SpeedPercent(driveSpeed), right_speed=SpeedPercent(-driveSpeed))
            backMotorsState = "on"

            if driveMotor.position != 0:
                turning_direction = "none"
                if driveMotor.position > 0:
                    driveMotor.on_to_position(speed=SpeedPercent(-turnSpeed), position=0)
                elif driveMotor.position < 0:
                    driveMotor.on_to_position(speed=SpeedPercent(turnSpeed), position=0)
    elif (color == colorAPI.red) or (color == colorAPI.black):
        print("turning")
        # Set down the speed to our turn drive speed
        if backMotorsState != "turning":
            backMotors.on(left_speed=SpeedPercent(turnDriveSpeed), right_speed=SpeedPercent(-turnDriveSpeed))
            backMotorsState = "turning"

        # Turn depending on color
        if color == colorAPI.red:
            print("red registered, turning right")
            print("direction: " + turning_direction)
            print("position: " + str(driveMotor.position) + "/" + str(-((driveMotor.count_per_rot/360)*turnDegrees)))
            if turning_direction != "right":
                turning_direction = "right"
                driveMotor.on_to_position(speed=SpeedPercent(-turnSpeed), position=-((driveMotor.count_per_rot/360)*turnDegrees))
                # driveMotor.on(speed=SpeedPercent(-turnSpeed))
            # driveMotor.on_for_degrees(speed=SpeedPercent(-turnSpeed), degrees=turnDegrees)
        elif color == colorAPI.black:
            print("black registered, turning left")
            print("direction: " + turning_direction)
            print("position: " + str(driveMotor.position) + "/" + str(((driveMotor.count_per_rot/360)*turnDegrees)))
            if turning_direction != "left":
                turning_direction = "left"
                driveMotor.on_to_position(speed=SpeedPercent(turnSpeed), position=((driveMotor.count_per_rot/360)*turnDegrees))
                # driveMotor.on(speed=SpeedPercent(turnSpeed))
            # driveMotor.on_for_degrees(speed=SpeedPercent(turnSpeed), degrees=turnDegrees)
    elif color == colorAPI.yellow:
        print("yellow registered, turning off")
        backMotors.off()
        backMotorsState = "off"
        driveMotor.off()


def doRace():
    print("Starting racer...")

    driveMotor.position = 0

    # while buttons.any() is False:
    #     print(sensor.rgb)

    while True:
        try:
            # Get the color from the sensor
            # color = colorAPI.getColor(sensor.rgb)  # The custom color recognizer
            color = colorAPI.getColorBuiltIn(sensor.color)  # The built-in color from the API, categorized by 0, 1, 2 etc.
            if not color:
                colorName = "None"
            else:
                colorName = color.color

            print("Current color: " + colorName)

            # Save the color to the list of seen colors
            seenColors.append(color)

            # Drive, depending on the seen colors
            if len(seenColors) < 5:
                drive(color)
            else:
                count = len([x for x in seenColors if x == color])
                percent = count/len(seenColors)*100

                if percent >= seenColorsTolerancePercent:
                    drive(color)
                    sleep(driveDelay)

            # # print(to_save)
            # if buttons.right:
            #     red.RGB_values.append(read_color)
            #     print("Saved to red")
            #     sleep(2)
            # elif buttons.up:
            #     black.RGB_values.append(read_color)
            #     print("Saved to black")
            #     sleep(2)
            # elif buttons.left:
            #     yellow.RGB_values.append(read_color)
            #     print("Saved to yellow")
            #     sleep(2)
            # elif buttons.enter:
            #     red.save()
            #     black.save()
            #     yellow.save()
            #     print("Saved colors to colors.json")
            #     sleep(2)
        except Exception as e:
            print("uh oh... - " + str(e))


if __name__ == '__main__':
    setup()
    sleep(5)
    doRace()
