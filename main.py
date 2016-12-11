#!/usr/bin/python

# Pygame and external libraries
import pygame, sys, math, random

from time import time

from pygame.locals import *

# Custom modules
import ring
import robot
import colours

class REMain:
    """The Main Robot Evacuation Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=700,height=400):
        self._running = False
        """Set the window Size"""
        self.size = self.width, self.height = width, height
        self.ring = ring.Ring(self.height / 2, (self.width / 2, self.height / 2))
        
    def _on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.display_surf.fill(colours.WHITE)
        self._running = True

    def _on_cleanup(self):
        self._running = False

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            self._on_cleanup()

    def main_loop(self):
        """This is the Main Loop of the Game"""
        if self._on_init() == False:
            self._running = False

        self._running = True
        self.ring.draw(self.display_surf)
        while self._running:
            for event in pygame.event.get():
                self._on_event(event)
            pygame.display.update()

        pygame.quit()
        sys.exit()

def setupCase1(robots, ring):
    start = (ring.rect.centerx, ring.rect.centery)
    dest = ring.pointOnRing()

    robots.append(robot.Robot(100, start, 1))
    robots.append(robot.Robot(100, start, -1))

    return dest

def setupCase2(robots, ring):
    angle = (2 * math.pi) * random.random()
    start1 = (ring.rect.centerx, ring.rect.centery)
    start2 = ring.pointInRingAngle(angle)
    dest = ring.pointOnRingAngle(angle)

    robots.append(robot.Robot(100, start1, 1))
    robots.append(robot.Robot(100, start2, -1))

    return dest

def setupCase3(robots, ring):
    start1 = ring.pointInRing()
    start2 = ring.pointInRing()

    slope = calcSlope(start1, start2)
    if not slope:
        perpSlope = 0
    else:
        perpSlope = (-1) * (1 / slope)

    midPoint = ((start1[0] + start2[0]) / 2, (start1[1] + start2[1]) / 2)
    yInt = calcIntercept(perpSlope, midPoint)

    dest = None
    points = ring.intersectionWithLine((perpSlope, yInt))
    minDist = ring.radius
    for point in points:
        dist = math.sqrt((point[0] - midPoint[0]) ** 2 + (point[1] - midPoint[1]) ** 2)
        if dist < minDist:
            minDist = dist
            dest = point

    robots.append(robot.Robot(100, start1, 1))
    robots.append(robot.Robot(100, start2, -1))

    return dest

def calcSlope(pos1, pos2):

    if pos1[0] == pos2[0]:
        slope = None
    else:
        slope = (float(pos2[1]) - pos1[1]) / (float(pos2[0]) - pos1[0])
    
    return slope

def calcIntercept(slope, point):
    return point[1] - point[0] * slope


def moveRobots(point, ring, robots, timeDelta):
    evacuated = False
    exitFound = False
    for robot in robots:
        if robot.evacuated:
            exitFound = True
            break

    for robot in robots:
        if exitFound and not robot.evacuated:
            if not robot.evacuated:
                robot.onPerimeter = robot.evacuated = robot.findPoint((ring.exit.rect.centerx, ring.exit.rect.centery), timeDelta)
            evacuated = evacuated and robot.evacuated
        elif not robot.onPerimeter:
            robot.onPerimeter = robot.findPoint(point, timeDelta)
        elif not robot.evacuated:
            robot.evacuated = robot.findExit(ring, timeDelta)
            if robot.evacuated:
                exitFound = True

    return evacuated

if __name__ == "__main__":
    # app = REMain()
    # app.main_loop()
    
    pygame.init()
    
    screen_width = 700
    screen_height = 400

    screen = pygame.display.set_mode([screen_width,screen_height])
    bgRect = Rect((0, 0), (screen_width, screen_height))
    bgSurf = pygame.Surface(bgRect.size)
    pygame.draw.rect(bgSurf, colours.WHITE, bgRect)

    screen.blit(bgSurf, bgRect)

    ringPos = (screen_width / 2, screen_height / 2)
    ringRadius = 150
    ring = ring.Ring(ringPos, ringRadius)

    clock = pygame.time.Clock()
    evacuated = False

    robots = []
    point = setupCase3(robots, ring)

    delay = 0
    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()

        screen.blit(bgSurf, bgRect)         # TODO: Check if It is possible to just redraw a portion of the background.
        ring.draw(screen)

        for robot in robots:
            robot.draw(screen)
        
        timeDelta = clock.tick_busy_loop()
        timeDelta /= 1000.0

        if delay >= 1:
            evacuated = moveRobots(point, ring, robots, timeDelta)
        else:
            delay += timeDelta

        if not evacuated:
            pygame.display.update()
