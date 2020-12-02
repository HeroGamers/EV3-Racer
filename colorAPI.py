import json
import math

# Variables
scoreThreshold = 30


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


def getColor(rgb):
    # https://stackoverflow.com/questions/36439384/classifying-rgb-values-in-python
    manhattan = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
    colorList = []
    for rgb in black.RGB_values:
        colorList.append((black, rgb))
    for rgb in yellow.RGB_values:
        colorList.append((yellow, rgb))
    for rgb in red.RGB_values:
        colorList.append((red, rgb))
    distances = [(color, manhattan(color_rgb, rgb)) for color, color_rgb in colorList]
    distanceNumbers = [distance[1] for distance in distances]

    minDistance = min(distanceNumbers)

    # print(colorFound)
    # print(colorFound[0].color)


    return None


# Get color from sensor built-in
def getColorBuiltIn(sensorColor):
    # Color codes from https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/sensors.html?highlight=colorsensor#ev3dev2.sensor.lego.ColorSensor.color
    if sensorColor == 1:
        return black
    elif sensorColor == 4:
        return yellow
    elif sensorColor == 5:
        return red
    return None
