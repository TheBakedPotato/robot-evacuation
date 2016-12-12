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
import logger

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
        self.countButtons = []
        self.robotSpeed = 400.0

    def setupCountButtons(self):
        def returnCount1():
            return 1

        def returnCount50():
            return 15

        self.countButtons.append(button.Button("images/count-btn-1.png", (610, 150), returnCount1))
        self.countButtons.append(button.Button("images/count-btn-50.png", (610, 250), returnCount50))

    def setupScenarioButtons(self):
        self.scenarioButtons.append(button.Button("images/button1.png", (465, 100), self.setupScenario1))
        self.scenarioButtons.append(button.Button("images/button2.png", (465, 200), self.setupScenario2))
        self.scenarioButtons.append(button.Button("images/button3.png", (465, 300), self.setupScenario3))
    
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
        self.setupCountButtons()

    def main_loop(self):
        """This is the Main Loop of the Game"""
        self.on_init()
        running = True

        scenario = None
        evacuated = True
        runCount = 0
        point = 0

        logStr = ""
        startTime = 0
        clock = pygame.time.Clock()
        while running:
            event  = pygame.event.poll()
            if event:
                for btn in self.scenarioButtons:
                    tempScenario = btn.eventHandler(event)
                    if tempScenario:
                        scenario = tempScenario

                for btn in self.countButtons:
                    tempCount = btn.eventHandler(event)
                    if tempCount:
                        runCount = tempCount()

                if event.type == QUIT:
                    running = False

            self.screen.blit(self.bgSurf, self.bgRect)

            for btn in self.scenarioButtons:
                btn.draw(self.screen)

            for btn in self.countButtons:
                btn.draw(self.screen)

            timeDelta = clock.tick_busy_loop()
            timeDelta /= 1000.0

            if self.ring:
                self.ring.draw(self.screen)

            if self.robots:
                for bot in self.robots:
                    bot.drawTravelledLine(self.screen)

                for bot in self.robots:
                    bot.drawRobot(self.screen)

            if evacuated:
                if runCount > 0:
                    evacuated = False
                    point = self.setUpRing(scenario)

                    logStr += str((self.ring.rect.centerx, self.ring.rect.centery)) + ","
                    for bot in self.robots:
                        logStr += str((int(bot.centerx), int(bot.centery))) + ","
                    logStr += str((self.ring.exit.rect.centerx, self.ring.exit.rect.centery)) + ","

                    startTime = time()

            elif runCount and scenario:
                evacuated = self.moveRobots(point, timeDelta)
                if evacuated:
                    endTime = time() - startTime
                    logStr += str(endTime) + "\n"
                    logger.Logger.write(logStr)
                    logStr = ""
                    runCount -= 1

            pygame.display.update()

if __name__ == "__main__":
    logger.Logger.init("log-" + str(time()) + ".log")
    
    app = REMain()
    app.main_loop()

    logger.Logger.close()