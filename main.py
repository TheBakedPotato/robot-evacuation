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
    # Constructor
    # Setting up the screen size
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

    # Initializing the count buttons
    def setupCountButtons(self):
        def returnCount1():
            return 1

        def returnCount50():
            return 50

        self.countButtons.append(button.Button("images/count-btn-1.png", (610, 150), returnCount1))
        self.countButtons.append(button.Button("images/count-btn-50.png", (610, 250), returnCount50))

    # Initializing the scenario buttons
    # They're used to select which scenario should be executed
    def setupScenarioButtons(self):
        self.scenarioButtons.append(button.Button("images/button1.png", (465, 100), self.setupScenario1))
        self.scenarioButtons.append(button.Button("images/button2.png", (465, 200), self.setupScenario2))
        self.scenarioButtons.append(button.Button("images/button3.png", (465, 300), self.setupScenario3))
    
    # Setup the positions of the robots for scenario 1 where both robots are in the center
    # Returns the position they are headed to on the perimeter from the center
    def setupScenario1(self):
        start = (self.ring.rect.centerx, self.ring.rect.centery)
        dest = self.ring.pointOnRing()

        self.robots.append(robot.Robot(self.robotSpeed, start, 1, colours.BLUE))
        self.robots.append(robot.Robot(self.robotSpeed, start, -1, colours.GREEN))

        self.ring.draw(self.screen)
        for bot in self.robots:
            bot.drawRobot(self.screen)

        return dest

    # Setup the positions of the robots for scenario 2 where only one robot is in the center
    # Returns the position they are headed to on the perimeter from the center
    def setupScenario2(self):
        angle = (2 * math.pi) * random.random()
        start1 = (self.ring.rect.centerx, self.ring.rect.centery)

        # Grabbing a random point in the ring at a given angle from the center
        start2 = self.ring.pointInRingAngle(angle)
        # Their destination point will be at the same angle so they go in the same direction
        dest = self.ring.pointOnRingAngle(angle)

        self.robots.append(robot.Robot(self.robotSpeed, start1, 1, colours.BLUE))
        self.robots.append(robot.Robot(self.robotSpeed, start2, -1, colours.GREEN))

        self.ring.draw(self.screen)
        for bot in self.robots:
            bot.drawRobot(self.screen)

        return dest

    # Setup the positions of the robots for scenario 3 where both robots are in ring
    # Returns the position they are headed to on the perimeter from the center
    def setupScenario3(self):
        start1 = self.ring.pointInRing()
        start2 = self.ring.pointInRing()

        # Creating the line between the two robots
        robotLine = line.Line.fromPoints(start1, start2)
        
        # Calculating the perpendicular slope to robotLine
        if not robotLine.slope:
            perpSlope = 0
        else:
            perpSlope = (-1) * ( 1 / robotLine.slope)

        # Finding the mid point between the two robots
        midPoint = ((start1[0] + start2[0]) / 2, (start1[1] + start2[1]) / 2)
        # Bisector for robotLine using the mid point of the robots
        bisector = line.Line.fromSlopeAndPoint(perpSlope, midPoint)

        dest = None
        # Retrieving where the bisector intersects with the ring`
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

    # Setting up the ring
    def setUpRing(self, scenario):
        self.robots = []
        self.ring = ring.Ring((200, self.height / 2), 150)
        return scenario()

    # Moves the robots an amount based on timeDelta
    # point: (x,y) coordinate on the perimeter the robots have to reach
    # timeDelta: time since last frame in seconds
    def moveRobots(self, point, timeDelta):
        evacuated = True
        exitFound = False

        # Determining if one of the robots has found the exit
        for bot in self.robots:
            if bot.evacuated:
                exitFound = True
                break

        for bot in self.robots:
            if not bot.evacuated:
                if exitFound:
                    # Robots head straight to the exit if another robot has found the exit
                    # The onPerimeter flag is set if they have not made to the perimeter yet
                    bot.evacuated = bot.onPerimeter = bot.findPoint((self.ring.exit.rect.centerx, self.ring.exit.rect.centery), timeDelta)
                elif not bot.onPerimeter:
                    # Head to the perimeter until they are on the perimeter
                    bot.onPerimeter = bot.findPoint(point, timeDelta)
                else:
                    # Search ring for the exit
                    bot.evacuated = bot.findExitOnRing(self.ring, timeDelta)

        # setting evacuated based on if robots have evacuated
        for bot in self.robots:
            evacuated = evacuated and bot.evacuated

        return evacuated

    # Setting up main application window
    def on_init(self):
        pygame.init()

        self.screen = pygame.display.set_mode([self.width,self.height])
        self.bgRect = Rect((0, 0), (self.width, self.height))
        self.bgSurf = pygame.Surface(self.bgRect.size)
        pygame.draw.rect(self.bgSurf, colours.WHITE, self.bgRect)
        self.screen.blit(self.bgSurf, self.bgRect)

        self.setupScenarioButtons()
        self.setupCountButtons()

    # Main application loop
    # Controllers moving the robots and handling events, such as mouse events, for the buttons
    def main_loop(self):
        """This is the Main Loop of the Game"""
        self.on_init()
        running = True

        scenario = None         # Scenario function based on which button is pressed
        runCount = 0            # How many runs are left for a given scenario before a new scenario can be selected
        evacuated = True
        point = 0

        logStr = ""
        startTime = 0
        clock = pygame.time.Clock()
        while running:
            event  = pygame.event.poll()
            if event:
                # Getting the scenario to execute if a scenario button was clicked
                for btn in self.scenarioButtons:
                    tempScenario = btn.eventHandler(event)
                    if tempScenario:
                        scenario = tempScenario

                # Getting the run count to execute if a run count button was clicked
                for btn in self.countButtons:
                    tempCount = btn.eventHandler(event)
                    if tempCount:
                        runCount = tempCount()

                if event.type == QUIT:
                    running = False

            # Redraws the background to clean the slate for drawing all the objects, such as robots
            self.screen.blit(self.bgSurf, self.bgRect)

            for btn in self.scenarioButtons:
                btn.draw(self.screen)

            for btn in self.countButtons:
                btn.draw(self.screen)

            # Calculating time since last frame
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

                    # logStr += str((self.ring.rect.centerx, self.ring.rect.centery)) + ","
                    # for bot in self.robots:
                    #     logStr += str((int(bot.centerx), int(bot.centery))) + ","
                    # logStr += str((self.ring.exit.rect.centerx, self.ring.exit.rect.centery)) + ","

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