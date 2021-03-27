from p5 import *
import random
import math

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
    def __init__(self, x, y, rad, stepX = 5, stepY = 5, moves = list()):
        self.x = x
        self.y = y
        self.rad = rad
        self.moves = moves
        self.stepX = stepX
        self.stepY = stepY
        self.moveToDo = 0

    def genMove(self): 
        xShift = random.randint(-self.stepX, self.stepX)
        yShift = random.randint(-self.stepY, self.stepY)
        self.x += xShift
        self.y += yShift

        self.moves.append((-1, 2))
        print("Add: " + str((xShift, yShift)) + " in " + str(self))

    def move(self):
        self.x = self.x + self.moves[self.moveToDo][0]
        self.y = self.y + self.moves[self.moveToDo][1]
        self.moveToDo += 1

    def draw(self):
        stroke_weight(0)
        fill(0, 255, 0)
        circle((self.x, self.y), self.rad)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BORDER_WIDTH = 20
BORDER_COLOR = Color(255,0,0)
NUM_FINDERS = 10
MOVES_PER_GEN = 5
K_BEST = 5

numMoves = 0
bFinders = list()
compute = True

START = (320, 360)
END = (960, 360)
count = 0

start = Point(START[0], START[1], 30)
end = Point(END[0], END[1], 30)

def setup():
    size(SCREEN_WIDTH, SCREEN_HEIGHT)
    no_stroke()
    background(204)

    global bFinders
    bFinders = [BlindFinder(START[0], START[1], 10) for _ in range(0, NUM_FINDERS)]

def draw():
    stroke_weight(BORDER_WIDTH)
    stroke(BORDER_COLOR)
    fill(240)
    rect(0,0,SCREEN_WIDTH, SCREEN_HEIGHT)

    start.draw()
    end.draw()

    global count
    global compute
    global bFinders
    global numMoves
    if count < MOVES_PER_GEN:
        # Gen 1
        count = count + 1
        genMoveAllFinders()
        if count == MOVES_PER_GEN:
            compute = True
    else:
        if compute:
            # Gen k
            # Valutare Finders della generazione precedente
            bestAll = fitnessFunction(bFinders)
            # Seleziono i k migliori
            best = bestAll[:K_BEST]
            # Farli accoppiare e mutare
            bFinders = crossover(best)
            compute = False
            numMoves = 0
        else:
            moveAllFinders()
            numMoves = numMoves + 1
            if(numMoves == MOVES_PER_GEN - 1):
                numMoves = 0
                compute = True

def genMoveAllFinders():
    global bFinders
#    for f in bFinders:
#        print(str(f) + ": " + str(len(f.moves)))
    for finder in bFinders:
        finder.genMove()
        finder.draw()
    print(" ")

def moveAllFinders():
    for finder in bFinders:
        #print(finder.moves[finder.moveToDo])
        finder.move()
        finder.draw()


def crossover(bestFinders):
    listNewFinders = list()
    for i in range(0, NUM_FINDERS):
        firstIndex = 0
        secondIndex = 0
        while firstIndex == secondIndex:
            firstIndex = random.randint(0, len(bestFinders)-1)
            secondIndex = random.randint(0, len(bestFinders)-1)
        finderA = bestFinders[firstIndex].get("finder")
        finderB = bestFinders[secondIndex].get("finder")
        listNewFinders.append(BlindFinder(START[0], START[1], 10))
        for i in range(0, len(finderA.moves)):
            ch = random.randint(0,1)
            if ch == 0:
                listNewFinders[len(listNewFinders)-1].moves.append(finderA.moves[i])
            else:
                listNewFinders[len(listNewFinders)-1].moves.append(finderB.moves[i])
    return listNewFinders

def fitnessFunction(finders):
    evalFinders = list()
    for finder in finders:
        dist = evalDist(finder)
        evalFinders.append({"finder": finder, "dist": dist})
    evalFinders.sort(key=takeFit)
    return evalFinders

def takeFit(elem):
    return elem.get("dist")

def evalDist(finder):
    return math.sqrt( math.pow((finder.x - end.x), 2) + math.pow((finder.y - end.y), 2) )

run()