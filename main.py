from p5 import *
import random

class Point:
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad

    def draw(self):
        stroke_weight(0)
        fill(255, 0, 0)
        circle((self.x, self.y), self.rad)

class BlindFinder:
    def __init__(self, x, y, rad, stepX = 5, stepY = 5):
        self.x = x
        self.y = y
        self.rad = rad
        self.moves = list()
        self.stepX = stepX
        self.stepY = stepY

    def genMove(self): 
        xShift = random.uniform(-self.stepX, self.stepX)
        yShift = random.uniform(-self.stepY, self.stepY)
        self.x += xShift
        self.y += yShift

        self.moves.append((xShift, yShift))

    def draw(self):
        stroke_weight(0)
        fill(0, 255, 0)
        circle((self.x, self.y), self.rad)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BORDER_WIDTH = 20
BORDER_COLOR = Color(255,0,0)
NUM_FINDERS = 30

bFinders = list()

START = (320, 360)
END = (960, 360)
count = 0

start = Point(START[0], START[1], 30)
end = Point(END[0], END[1], 30)

def setup():
    size(SCREEN_WIDTH, SCREEN_HEIGHT)
    no_stroke()
    background(204)

    for i in range(0, NUM_FINDERS-1):
        bFinders.append(BlindFinder(START[0], START[1], 10))

def draw():
    stroke_weight(BORDER_WIDTH)
    stroke(BORDER_COLOR)
    fill(240)
    rect(0,0,SCREEN_WIDTH, SCREEN_HEIGHT)

    start.draw()
    end.draw()

    global count
    if count < 200:
        count = count + 1
        for finder in bFinders:
            finder.genMove()
            finder.draw()

run()