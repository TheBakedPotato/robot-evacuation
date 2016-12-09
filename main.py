#!/usr/bin/python

# Pygame and external libraries
import pygame, sys

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
    screen.fill(colours.BLUE)

    robot = pygame.image.load('images/robot.png').convert()
    robotPos = robot.get_rect(center=(robot.get_width() / 2, robot.get_height() / 2))
    robotPos.x = screen_width / 2
    robotPos.y = screen_height / 2

    print "X: " + str(robotPos.x) + " Center X: " + str(robotPos.centerx)

    screen.blit(robot, robotPos)
    pygame.display.update()

    pps = (100, 0)

    clock = pygame.time.Clock()
    moveX = 0;
    moveY = 0;
    while 1:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()

        screen.blit(screen, robotPos, robotPos)
        robotPos = robotPos.move(1,0)
        screen.blit(robot, robotPos)
        pygame.display.update()
        pygame.time.delay(20)
        
        # screen.blit(screen, robotPos, robotPos)

        # timeDelta = clock.tick_busy_loop()
        # timeDelta /= 1000.0

        # moveX += pps[0] * timeDelta
        # moveY += pps[1] * timeDelta
        # if (moveX >= 1):
        #     robotPos = robotPos.move(moveX, 0)
        #     moveX = 0

        # if (moveY >= 1):
        #     robotPos = robotPos.move(0, moveY)
        #     moveY = 0

        # screen.blit(robot, robotPos)
        # pygame.display.update()