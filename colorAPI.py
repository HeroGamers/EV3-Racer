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
        chosenColor = yellow

    print(str(lowest_score_value) + "/" + str(scoreThreshold))

    if chosenColor and lowest_score_value <= scoreThreshold:
        return chosenColor
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