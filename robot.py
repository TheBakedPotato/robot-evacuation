import colours

import pygame, math

class Robot:
    def __init__(self, speed, startPos, angle=0):
        rect = pygame.Rect((0, 0), (20, 20))

        self._moving = False
        self._moveX = 0
        self._moveY = 0

        self.speed = 100
        self.surf = pygame.Surface(rect.size)
        self.rect = pygame.draw.rect(self.surf, colours.BLACK, rect)
        self.rect.centerx = startPos[0]
        self.rect.centery = startPos[1]
        self.angle = angle

    def findPerimeter(self, start, radius, timeDelta):
        if not self._moving:
            self._moving = True
            self._moveX = 0
            self._moveY = 0

        self._moveX += self.speed * timeDelta * math.cos(self.angle)
        self._moveY += self.speed * timeDelta * math.sin(self.angle)

        if (self._moveX >= 1) or (self._moveX <= -1):  
            self.rect = self.rect.move(self._moveX, 0)
            self._moveX = 0

        if (self._moveY >= 1) or (self._moveY <= -1):
            self.rect = self.rect.move(0, self._moveY)
            self._moveY = 0

        return math.sqrt((self.rect.centerx - start[0]) ** 2 + (self.rect.centery - start[1]) ** 2) >= radius

    def findExit(self, center, radius, timeDelta, direction):
        self.angle += direction * timeDelta * (self.speed / radius)
        self.rect.centerx = radius * math.cos(self.angle) + center[0]
        self.rect.centery = radius * math.sin(self.angle) + center[1]

