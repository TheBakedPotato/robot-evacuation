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

class REMain(object):
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
        self.robotSpeed = 100.0

    def setupScenarioButtons(self):
        self.scenarioButtons.append(button.Button("images/button1.png", (500, 100), self.setupScenario1))
        self.scenarioButtons.append(button.Button("images/button2.png", (500, 200), self.setupScenario2))
        self.scenarioButtons.append(button.Button("images/button3.png", (500, 300), self.setupScenario3))
    
    def setupScenario1(self):
        start = (self.ring.rect.centerx, self.ring.rect.centery)
        dest = self.ring.pointOnRing()

        self.robots.append(robot.Robot(self.robotSpeed, start, 1, colours.BLUE))
        self.robots.append(robot.Robot(self.robotSpeed, start, -1, colours.GREEN))

        self.ring.draw(self.screen)
        for bot in self.robots:
            bot.drawRobot(self.screen)

        return dest

    def setupScenario2(self):
        angle = (2 * math.pi) * random.random()
        start1 = (self.ring.rect.centerx, self.ring.rect.centery)
        start2 = self.ring.pointInRingAngle(angle)
        dest = self.ring.pointOnRingAngle(angle)

        self.robots.append(robot.Robot(self.robotSpeed, start1, 1, colours.BLUE))
        self.robots.append(robot.Robot(self.robotSpeed, start2, -1, colours.GREEN))

        self.ring.draw(self.screen)
        for bot in self.robots:
            bot.drawRobot(self.screen)

        return dest

    def setupScenario3(self):
        start1 = self.ring.pointInRing()
        start2 = self.ring.pointInRing()

        robotLine = line.Line.fromPoints(start1, start2)
        if not robotLine.slope:
            perpSlope = 0
        else:
            perpSlope = (-1) * ( 1 / robotLine.slope)

        midPoint = ((start1[0] + start2[0]) / 2, (start1[1] + start2[1]) / 2)
        bisector = line.Line.fromSlopeAndPoint(perpSlope, midPoint)

        dest = None
        points = self.ring.intersectionWithLine(bisector)
        minDist = self.ring.radius
        for point in points:
            dist = math.sqrt((point[0] - midPoint[0]) ** 2 + (point[1] - midPoint[1]) ** 2)
            if dist < minDist:
                minDist = dist
                dest = point

        self.robots.append(robot.Robot(self.robotSpeed, start1, 1, colours.BLUE))
        self.robots.append(robot.Robot(self.robotSpeed, start2, -1, colours.GREEN))

        self.ring.draw(self.screen)
        for bot in self.robots:
            bot.drawRobot(self.screen)

        return dest

    def setUpRing(self, scenario):
        self.robots = []
        self.ring = ring.Ring((200, self.height / 2), 150)
        return scenario()

    def moveRobots(self, point, timeDelta):
        evacuated = True
        exitFound = False
        for bot in self.robots:
            if bot.evacuated:
                exitFound = True
                break

        for bot in self.robots:
            if not bot.evacuated:
                if exitFound:
                    bot.evacuated = bot.onPerimeter = bot.findPoint((self.ring.exit.rect.centerx, self.ring.exit.rect.centery), timeDelta)
                elif not bot.onPerimeter:
                    bot.onPerimeter = bot.findPoint(point, timeDelta)
                else:
                    bot.evacuated = bot.findExitOnRing(self.ring, timeDelta)

        for bot in self.robots:
            evacuated = evacuated and bot.evacuated

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
        running = True

        scenario = None
        run = True
        evacuated = False

        runCount = 1

        point = self.setUpRing(self.setupScenario3)
        clock = pygame.time.Clock()
        delay = 0

        while running:
            event  = pygame.event.poll()
            if event:
                for btn in self.scenarioButtons:
                    tempScenario = btn.eventHandler(event)
                    if tempScenario:
                        scenario = tempScenario

            if event.type in (QUIT, KEYDOWN):
                running = False

            self.screen.blit(self.bgSurf, self.bgRect)         # TODO: Check if It is possible to just redraw a portion of the background.

            for btn in self.scenarioButtons:
                btn.draw(self.screen)

            timeDelta = clock.tick_busy_loop()
            timeDelta /= 1000.0

            self.ring.draw(self.screen)

            for bot in self.robots:
                bot.drawTravelledLine(self.screen)

            for bot in self.robots:
                bot.drawRobot(self.screen)

            if run:
                if delay >= 1:
                    evacuated = self.moveRobots(point, timeDelta)
                    if evacuated:
                        run = False
                else:
                    delay += timeDelta
            else:
                point = self.setUpRing(self.setupScenario1)
                run = True

            pygame.display.update()


if __name__ == "__main__":
    app = REMain()
    app.main_loop()