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
    angle = (2 * math.pi) * random.random()
    start = (ring.rect.centerx, ring.rect.centery)
    dest = (ringRadius * math.cos(angle) + ringPos[0], ringRadius * math.sin(angle) + ringPos[1])

    robots.append(robot.Robot(100, start, 1))
    robots.append(robot.Robot(100, start, -1))

    return dest

def setupCase2(robots, ring):
    angle = (2 * math.pi) * random.random()
    factor = random.random()
    start1 = (ring.rect.centerx, ring.rect.centery)
    start2 = (ringRadius * math.cos(angle) * factor + ringPos[0], ringRadius * math.sin(angle) * factor + ringPos[1])
    dest = (ringRadius * math.cos(angle) + ringPos[0], ringRadius * math.sin(angle) + ringPos[1])

    robots.append(robot.Robot(100, start1, 1))
    robots.append(robot.Robot(100, start2, -1))

    return dest

def setupCase3(robots, ring):
    return

def moveRobots(ring, robots, timeDelta):
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
            robot.evacuated = robot.findExit(ringPos, ringRadius * 1.0, timeDelta, ring.exit)
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
    point = setupCase2(robots, ring)

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
            evacuated = moveRobots(ring, robots, timeDelta)
        else:
            delay += timeDelta

        if not evacuated:
            pygame.display.update()
