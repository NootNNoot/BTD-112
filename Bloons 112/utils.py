import math 
from cmu_graphics import *
import towerStats
import Classes


def createUIMonkeys():
    x = 847
    y = 92
    dx = 0
    dy = 0
    i = 0
    for monkeys in towerStats.tStats:
        match i:
            case 0:
                dx = 0
            case 1:
                dx = 100
        monkey = Classes.UITower(x + dx, y + dy, monkeys)
        i += 1
        if i % 2 == 0:
            i = 0
            dy += 200

def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def exists(bloon):
    if bloon in Classes.Balloon.registry:
        return True
    return False

def resetBloons():
    for bloon in Classes.Balloon.registry:
        bloon.justHit = False

def spawnNewBloons(L):
    i = 1
    for child, x, y, direction in L:
        dir = direction
        dx = dy = 0
        match dir: 
            case 'right':
                dx = 5
            case 'left':
                dx = -5
            case 'up':
                dy = -5
            case 'down':
                dy = 5
            case 'up-right':
                dx = 5
                dy = -5
            case 'up-left':
                dx = -5
                dy = -5
            case 'down-left':
                dx = -5
                dy = 5
            case 'down-right':
                dx = 5
                dy = 5
        newB = Classes.Balloon(x + (dx*i), y + (dy*i), child, direction)
        i *= -1


#Equations for an increasingly expanding spiral
#(Parametric equations of a spiral)
def xEquation(s, t):
    return s*t*math.cos(t)

def yEquation(s, t):
    return s*t*math.sin(t)