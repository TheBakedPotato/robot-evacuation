#!/usr/bin/python

# Pygame and external libraries
import pygame, sys, math

from time import time

from pygame.locals import *

# Custom modules
import ring
import robot
import colours

class REMain:
    """The Main Robot Evacuation Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=480):
        self._running = False
        """Set the window Size"""
        self.size = self.width, self.height = width, height
        self.display_surf = None
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

    angle = 37 * math.pi / 20
    ringPos = (screen_width / 2, screen_height / 2)
    exitPos = (200, 200)
    ringRadius = 150

    robot1 = robot.Robot(100, ringPos, angle)
    robot2 = robot.Robot(100, ringPos, angle)
    ring = ring.Ring(ringPos, ringRadius)

    clock = pygame.time.Clock()
    foundPerimeter = False
    evacuated = False

    startTime = time()

    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()

        screen.blit(bgSurf, bgRect)         # TODO: Check if It is possible to just redraw a portion of the background.
        ring.draw(screen)
        screen.blit(robot1.surf, robot1.rect)
        screen.blit(robot2.surf, robot2.rect)

        
        timeDelta = clock.tick_busy_loop()
        timeDelta /= 1000.0

        if not foundPerimeter:
            foundPerimeter = robot1.findPoint(ringPos, ringRadius, timeDelta)
            robot2.findPoint(ringPos, ringRadius, timeDelta)
            if foundPerimeter:
                print "Elapsed Time: " + str(time() - startTime)
                startTime = time()
        elif not evacuated:
            r1Evac = robot1.findExit(ringPos, ringRadius * 1.0, timeDelta, ring.exit, 1)
            r2Evac = robot2.findExit(ringPos, ringRadius * 1.0, timeDelta, ring.exit, -1)

            evacuated = r1Evac or r2Evac
            if evacuated:
                print "Elapsed Time: " + str(time() - startTime)

        screen.blit(robot1.surf, robot1.rect)
        screen.blit(robot2.surf, robot2.rect)
        pygame.display.update()
