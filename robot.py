import colours

import pygame, math

class Robot:
    def __init__(self, speed, startPos, angle=0):
        rect = pygame.Rect((0, 0), (20, 20))

        self.moving = False

        self.speed = 100
        self.surf = pygame.Surface(rect.size)
        self.rect = pygame.draw.rect(self.surf, colours.BLACK, rect)
        self.rect.centerx = self.centerx = startPos[0]
        self.rect.centery = self.centery = startPos[1]
        self.angle = angle

    def findPoint(self, start, distance, timeDelta):
        if not self.moving:
            self.moving = True

        self.centerx += self.speed * timeDelta * math.cos(self.angle)
        self.centery += self.speed * timeDelta * math.sin(self.angle)

        self.rect.centerx = self.centerx;
        self.rect.centery = self.centery

        return math.sqrt((self.rect.centerx - start[0]) ** 2 + (self.rect.centery - start[1]) ** 2) >= distance

    def findExit(self, center, radius, timeDelta, exit, direction):
        if not self.moving:
            self.moving = True

        self.angle += direction * timeDelta * (self.speed / radius)
        self.rect.centerx = radius * math.cos(self.angle) + center[0]
        self.rect.centery = radius * math.sin(self.angle) + center[1]

