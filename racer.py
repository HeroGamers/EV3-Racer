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
driveSpeed = SpeedPercent(100)
turnDriveSpeed = SpeedPercent(50)
turnSpeed = [SpeedPercent(30), SpeedPercent(-30)]  # Right and left
turnDegrees = 90
backMotorsState = "off"
seenColorsTolerancePercent = 90
seenColors = collections.deque(maxlen=5)
driveDelay = 0.5  # Delay between each loop of driving

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
    print("drive() is running")
    global backMotorsState
    if not color:
        print("no color, should be driving")
        print("backmotorstate: " + backMotorsState)
        if (backMotorsState == "off") or (backMotorsState == "turning"):
            print("driving")
            backMotors.on(left_speed=driveSpeed, right_speed=driveSpeed)
            backMotorsState = "on"
    elif (color == colorAPI.red) or (color == colorAPI.black):
        print("turning")
        # Set down the speed to our turn drive speed
        if backMotorsState != "turning":
            backMotors.on(left_speed=turnDriveSpeed, right_speed=turnDriveSpeed)
            backMotorsState = "turning"

        # Turn depending on color
        if color == colorAPI.red:
            print("red registered, turning right")
            driveMotor.on_for_degrees(speed=turnSpeed[1], degrees=turnDegrees)
        elif color == colorAPI.black:
            print("black registered, turning left")
            driveMotor.on_for_degrees(speed=turnSpeed[0], degrees=turnDegrees)
    elif color == colorAPI.yellow:
        print("yellow registered, turning off")
        backMotors.off()
        backMotorsState = "off"
        driveMotor.off()


def doRace():
    print("Starting racer...")

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
            print(str(seenColors))

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
