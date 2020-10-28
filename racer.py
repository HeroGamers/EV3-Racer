#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
import os, sys
from time import sleep

# Variables
black = (9, 13, 12)
red = (170, 25, 40)
yellow = (100, 45, 22)


# The motors, sensors and other things on the robot
buttons = Button()  # Any buton on the robot
motorRight = LargeMotor(address=OUTPUT_A)  # Motor on output port A
motorLeft = LargeMotor(address=OUTPUT_D)  # Motor on output port D
sensor = ColorSensor(address=INPUT_1)  # Color sensor on input port 1

def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

def setup():
    os.system('setfont Lat15-TerminusBold14')  # Sets the console font
    print('\x1Bc', end='')  # Resets the console
    print("Hello, World!")

def doRace():
    print("Starting racer...")

    while buttons.any() is False:
        print(sensor.rgb)


if __name__ == '__main__':
    setup()
    sleep(10)
    doRace()
