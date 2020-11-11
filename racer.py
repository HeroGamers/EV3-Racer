#!/usr/bin/env python3
import math

from ev3dev2.motor import MoveTank, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
import os
import sys
import json
from time import sleep


# Variables
scoreThreshold = 10

# The motors, sensors and other things on the robot
buttons = Button()  # Any buton on the robot
backMotors = MoveTank(left_motor_port=OUTPUT_A, right_motor_port=OUTPUT_D)  # Motor on output port A and D
driveMotor = MediumMotor(address=OUTPUT_B)  # Motor on output port B
sensor = ColorSensor(address=INPUT_1)  # Color sensor on input port 1


def debug(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


class Color:
    color = None
    RGB_values = []

    def __init__(self, color, rgb_values=None):
        self.color = color
        if rgb_values is None:
            self.load()
        else:
            self.RGB_values = rgb_values

    def save(self):
        colors = None
        with open("colors.json", "r") as colorFile:
            colors = json.load(colorFile)

        with open("colors.json", "w") as colorFile:
            rgb_push = []
            for value in self.RGB_values:
                rgb_push.append({"R": value[0], "G": value[1], "B": value[2]})
            colors[self.color] = rgb_push

            json.dump(colors, colorFile, indent=4)

    def load(self):
        with open("colors.json", "r") as colorFile:
            colors = json.load(colorFile)
            self.RGB_values = []
            for value in colors[self.color]:
                self.RGB_values.append((value["R"], value["G"], value["B"]))


# Colors
black = Color("black")
red = Color("red")
yellow = Color("yellow")


def setup():
    os.system('setfont Lat15-TerminusBold14')  # Sets the console font
    print('\x1Bc', end='')  # Resets the console
    print("Hello, World!")


def getColor(rgb):
    # The lower score the better
    redScore = 0
    blackScore = 0
    yellowScore = 0

    def getScore(color, rgb):
        scores = []
        for db_rgb in color.RGB_values:
            vec_diff = (rgb[0]-db_rgb[0], rgb[1]-db_rgb[1], rgb[2]-db_rgb[2])
            vec_length = math.sqrt(vec_diff[0]**2+vec_diff[1]**2+vec_diff[2]**2)
            scores.append(vec_length)

        return sum(scores)/len(scores)

    # Get color scores
    redScore = getScore(red, rgb)
    blackScore = getScore(black, rgb)
    yellowScore = getScore(yellow, rgb)

    # Get the smallest score
    score_dict = {"red": redScore, "black": blackScore, "yellow": yellowScore}
    lowest_score_value = min([redScore, blackScore, yellowScore])
    chosenColor = None
    if score_dict['red'] == lowest_score_value:
        chosenColor = red
    elif score_dict['black'] == lowest_score_value:
        chosenColor = black
    elif score_dict['yellow'] == lowest_score_value:
        chosenColor = yellowScore

    print(str(lowest_score_value) + "/" + str(scoreThreshold))

    if chosenColor and lowest_score_value <= scoreThreshold:
        return chosenColor
    return None


def doRace():
    print("Starting racer...")

    # while buttons.any() is False:
    #     print(sensor.rgb)

    while True:
        read_color = sensor.rgb

        color = getColor(read_color)
        if not color:
            colorName = "None"
        else:
            colorName = color.color

        print("Current color: " + colorName)

        # print(to_save)
        if buttons.right:
            red.RGB_values.append(read_color)
            print("Saved to red")
            sleep(2)
        elif buttons.up:
            black.RGB_values.append(read_color)
            print("Saved to black")
            sleep(2)
        elif buttons.left:
            yellow.RGB_values.append(read_color)
            print("Saved to yellow")
            sleep(2)
        elif buttons.enter:
            red.save()
            black.save()
            yellow.save()
            print("Saved colors to colors.json")
            sleep(2)


if __name__ == '__main__':
    setup()
    sleep(5)
    doRace()
