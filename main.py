#!/usr/bin/python

# Pygame and external libraries
import pygame, sys, math

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

    robot = robot.Robot()
    
    robot.rect = robot.rect.move(screen_width / 2 - robot.rect.width / 2, screen_height / 2 - robot.rect.height / 2)

    screen.blit(robot.surf, robot.rect)
    pygame.display.update()

    clock = pygame.time.Clock()
    moveX = 0;
    moveY = 0;
    collided = False
    ringRadius = 150
    ringPos = (screen_width / 2, screen_height / 2)
    angle = 32

    x = round(ringRadius * math.cos(math.radians(angle)) + screen_width / 2)
    y = round(ringRadius * math.sin(math.radians(angle)) + screen_height / 2)
    print (x, y)

    pps = (round(100 * math.cos(math.radians(angle))), round(100 * math.sin(math.radians(angle))))

    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()

        screen.blit(bgSurf, bgRect)         # TODO: Check if It is possible to just redraw a portion of the background.
        circleRect = pygame.draw.circle(screen, colours.BLUE, ringPos, ringRadius, 1)
        
        timeDelta = clock.tick_busy_loop()
        timeDelta /= 1000.0

        moveX += pps[0] * timeDelta
        moveY += pps[1] * timeDelta
        
        if (moveX >= 1):
            robot.rect = robot.rect.move(1, 0)
            moveX = 0
        elif (moveX <= -1):
            robot.rect = robot.rect.move(-1, 0)
            moveX = 0

        if (moveY >= 1):
            robot.rect = robot.rect.move(0, 1)
            moveY = 0
        elif (moveY <= -1):
            robot.rect = robot.rect.move(0, -1)
            moveY = 0

        if not collided:
            screen.blit(robot.surf, robot.rect)
            collided = math.sqrt((robot.rect.centerx - ringPos[0]) ** 2 + (robot.rect.centery - ringPos[1]) ** 2) >= ringRadius
            pygame.display.update()
            if collided:
                print (robot.rect.centerx, robot.rect.centery)

        else:
            