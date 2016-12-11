#!/usr/bin/python

# Pygame and external libraries
import pygame, sys, math, random

from time import time

from pygame.locals import *

# Custom modules
import ring
import robot
import colours
import button
import line

class REMain:
    """The Main Robot Evacuation Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=700,height=400):
        self.running = False
        """Set the window Size"""
        self.size = self.width, self.height = width, height
        self.screen = None
        self.ring = None
        self.scenario = None
        self.robots = []
        self.scenarioButtons = []

    def setupScenarioButtons(self):
        self.scenarioButtons.append(button.Button((100,100), (600, 200), self.setupScenario3))

    def setupScenario1(self):
        start = (self.ring.rect.centerx, self.ring.rect.centery)
        dest = self.ring.pointOnRing()

        self.robots.append(robot.Robot(100, start, 1))
        self.robots.append(robot.Robot(100, start, -1))

        self.ring.draw(self.screen)
        for bot in self.robots:
            bot.draw(self.screen)

        return dest

    def setupScenario2(self):
        angle = (2 * math.pi) * random.random()
        start1 = (self.ring.rect.centerx, self.ring.rect.centery)
        start2 = self.ring.pointInRingAngle(angle)
        dest = self.ring.pointOnRingAngle(angle)

        self.robots.append(robot.Robot(100, start1, 1))
        self.robots.append(robot.Robot(100, start2, -1))

        self.ring.draw(self.screen)
        for bot in self.robots:
            bot.draw(self.screen)

        return dest

    def setupScenario3(self):
        start1 = self.ring.pointInRing()
        start2 = self.ring.pointInRing()

        slope = calcSlope(start1, start2)
        if not slope:
            perpSlope = 0
        else:
            perpSlope = (-1) * (1 / slope)

        midPoint = ((start1[0] + start2[0]) / 2, (start1[1] + start2[1]) / 2)
        yInt = calcIntercept(perpSlope, midPoint)

        dest = None
        points = self.ring.intersectionWithLine((perpSlope, yInt))
        minDist = self.ring.radius
        for point in points:
            dist = math.sqrt((point[0] - midPoint[0]) ** 2 + (point[1] - midPoint[1]) ** 2)
            if dist < minDist:
                minDist = dist
                dest = point

        self.robots.append(robot.Robot(100, start1, 1))
        self.robots.append(robot.Robot(100, start2, -1))

        self.ring.draw(self.screen)
        for bot in self.robots:
            bot.draw(self.screen)

        return dest

    def setUpRing(self):
        self.robots = []
        self.ring = ring.Ring((200, self.height / 2), 150)

    def moveRobots(self, point, timeDelta):
        evacuated = False
        exitFound = False
        for bot in self.robots:
            if bot.evacuated:
                exitFound = True
                break

        for bot in self.robots:
            if exitFound and not bot.evacuated:
                if not bot.evacuated:
                    bot.onPerimeter = bot.evacuated = bot.findPoint((self.ring.exit.rect.centerx, self.ring.exit.rect.centery), timeDelta)
                evacuated = evacuated and bot.evacuated
            elif not bot.onPerimeter:
                bot.onPerimeter = bot.findPoint(point, timeDelta)
            elif not bot.evacuated:
                bot.evacuated = bot.findExitOnRing(self.ring, timeDelta)
                if bot.evacuated:
                    exitFound = True

        return evacuated

    def on_init(self):
        pygame.init()

        self.screen = pygame.display.set_mode([self.width,self.height])
        self.bgRect = Rect((0, 0), (self.width, self.height))
        self.bgSurf = pygame.Surface(self.bgRect.size)
        pygame.draw.rect(self.bgSurf, colours.WHITE, self.bgRect)
        self.screen.blit(self.bgSurf, self.bgRect)

        self.setupScenarioButtons()

    def main_loop(self):
        """This is the Main Loop of the Game"""
        self.on_init()

        point = None
        scenario = None
        run = False
        evacuated = False

        clock = pygame.time.Clock()
        delay = 0

        while True:
            event  = pygame.event.poll()
            if event:
                for btn in self.scenarioButtons:
                    tempScenario = btn.eventHandler(event)
                    if tempScenario:
                        scenario = tempScenario

            if event.type in (QUIT, KEYDOWN):
                sys.exit()

            self.screen.blit(self.bgSurf, self.bgRect)         # TODO: Check if It is possible to just redraw a portion of the background.

            for btn in self.scenarioButtons:
                btn.draw(self.screen)

            timeDelta = clock.tick_busy_loop()
            timeDelta /= 1000.0

            if run:
                self.ring.draw(self.screen)

                for bot in self.robots:
                    bot.draw(self.screen)

                if delay >= 1:
                    evacuated = self.moveRobots(point, timeDelta)
                else:
                    delay += timeDelta

            elif scenario:
                self.setUpRing()
                point = scenario()
                scenario = None
                run = True

            if not evacuated:
                pygame.display.update()



####################################################################################################3
def setupCase1(robots, robotRing, surface):
    start = (robotRing.rect.centerx, robotRing.rect.centery)
    dest = robotRing.pointOnRing()

    robots.append(robot.Robot(100, start, 1))
    robots.append(robot.Robot(100, start, -1))

    robotRing.draw(surface)
    for bot in robots:
        bot.draw(surface)

    return dest

def setupCase2(robots, robotRing, surface):
    angle = (2 * math.pi) * random.random()
    start1 = (robotRing.rect.centerx, robotRing.rect.centery)
    start2 = robotRing.pointInRingAngle(angle)
    dest = robotRing.pointOnRingAngle(angle)

    robots.append(robot.Robot(100, start1, 1))
    robots.append(robot.Robot(100, start2, -1))

    robotRing.draw(surface)
    for bot in robots:
        bot.draw(surface)

    return dest

def setupCase3(robots, robotRing, surface):
    start1 = robotRing.pointInRing()
    start2 = robotRing.pointInRing()

    slope = calcSlope(start1, start2)
    if not slope:
        perpSlope = 0
    else:
        perpSlope = (-1) * (1 / slope)

    midPoint = ((start1[0] + start2[0]) / 2, (start1[1] + start2[1]) / 2)
    yInt = calcIntercept(perpSlope, midPoint)

    dest = None
    points = robotRing.intersectionWithLine((perpSlope, yInt))
    minDist = robotRing.radius
    for point in points:
        dist = math.sqrt((point[0] - midPoint[0]) ** 2 + (point[1] - midPoint[1]) ** 2)
        if dist < minDist:
            minDist = dist
            dest = point

    robots.append(robot.Robot(100, start1, 1))
    robots.append(robot.Robot(100, start2, -1))

    robotRing.draw(surface)
    for bot in robots:
        bot.draw(surface)

    return dest

def calcSlope(pos1, pos2):

    if pos1[0] == pos2[0]:
        slope = None
    else:
        slope = (float(pos2[1]) - pos1[1]) / (float(pos2[0]) - pos1[0])
    
    return slope

def calcIntercept(slope, point):
    return point[1] - point[0] * slope

def moveRobots(point, robotRing, robots, timeDelta):
    evacuated = False
    exitFound = False
    for bot in robots:
        if bot.evacuated:
            exitFound = True
            break

    for bot in robots:
        if exitFound and not bot.evacuated:
            if not bot.evacuated:
                bot.onPerimeter = bot.evacuated = bot.findPoint((robotRing.exit.rect.centerx, robotRing.exit.rect.centery), timeDelta)
            evacuated = evacuated and bot.evacuated
        elif not bot.onPerimeter:
            bot.onPerimeter = bot.findPoint(point, timeDelta)
        elif not bot.evacuated:
            bot.evacuated = bot.findExitOnRing(robotRing, timeDelta)
            if bot.evacuated:
                exitFound = True

    return evacuated

def setUp(robots):
    robots = []
    return ring.Ring((200, screen_height / 2), 150)

if __name__ == "__main__":
    app = REMain()
    app.main_loop()
    
    # pygame.init()
    
    # screen_width = 700
    # screen_height = 400

    # screen = pygame.display.set_mode([screen_width,screen_height])
    # bgRect = Rect((0, 0), (screen_width, screen_height))
    # bgSurf = pygame.Surface(bgRect.size)
    # pygame.draw.rect(bgSurf, colours.WHITE, bgRect)
    # screen.blit(bgSurf, bgRect)

    # ##################################################################

    # # ringPos = (200, screen_height / 2)
    # # ringRadius = 150
    # # ring = ring.Ring(ringPos, ringRadius)


    # # point = setupCase3(robots, ring)

    # button = button.Button((100,100), (600, 200), setupCase3)


    # robots = []
    # point = None
    # robotRing = None
    # scenario = None
    # run = False
    # evacuated = False

    # clock = pygame.time.Clock()
    # delay = 0

    # while True:
    #     event  = pygame.event.poll()
    #     if event:
    #         scenario = button.eventHandler(event)
    #     if event.type in (QUIT, KEYDOWN):
    #         sys.exit()

    #     screen.blit(bgSurf, bgRect)         # TODO: Check if It is possible to just redraw a portion of the background.
    #     button.draw(screen)

    #     timeDelta = clock.tick_busy_loop()
    #     timeDelta /= 1000.0

    #     if run:
    #         robotRing.draw(screen)

    #         for robot in robots:
    #             robot.draw(screen)
            

    #         if delay >= 1:
    #             evacuated = moveRobots(point, robotRing, robots, timeDelta)
    #         else:
    #             delay += timeDelta

    #     elif scenario:
    #         robotRing = setUp(robots)
    #         point = scenario(robots, robotRing, screen)
    #         scenario = None
    #         run = True

    #     if not evacuated:
    #         pygame.display.update()