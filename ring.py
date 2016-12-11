import pygame, random, math

import colours, destination

class Ring(object):
    def __init__(self, pos, radius, exitPos=None):
        self.pos = pos
        self.radius = radius

        rect = pygame.Rect((0, 0), (self.radius * 2, self.radius * 2))
        self.surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        pygame.draw.circle(self.surf, colours.BLUE, (self.radius, self.radius), self.radius, 1)
        self.rect = self.surf.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

        self.exit = destination.Destination(self.pointOnRing())

    def draw(self, surface):
        surface.blit(self.surf, self.rect)
        self.exit.draw(surface)

    def pointOnRingAngle(self, angle):
        x = self.pos[0] + self.radius * math.cos(angle)
        y = self.pos[1] + self.radius * math.sin(angle)
        return (x, y)

    def pointOnRing(self):
        angle = (2 * math.pi) * random.random()
        return self.pointOnRingAngle(angle)

    def pointInRingAngle(self, angle):
        tempRadius = self.radius * random.random()
        x = self.pos[0] + tempRadius * math.cos(angle)
        y = self.pos[1] + tempRadius * math.sin(angle)
        return (x, y)

    def pointInRing(self):
        angle = (2 * math.pi) * random.random()
        return self.pointInRingAngle(angle)

    def intersectionWithLine(self, line):
        a = line.slope ** 2 + 1
        b = 2 * (line.slope * line.yInt - line.slope * self.pos[1] - self.pos[0])
        c = (self.pos[1] ** 2) - (self.radius ** 2) + (self.pos[0] ** 2) - (2 * line.yInt * self.pos[1]) + (line.yInt ** 2)

        radical = (b ** 2) - (4 * a * c)
        if radical < 0:
            return []

        x1 = ((-b) + math.sqrt(radical)) / (2 * a)
        x2 = ((-b) - math.sqrt(radical)) / (2 * a)

        y1 = line.slope * x1 + line.yInt
        y2 = line.slope * x2 + line.yInt

        return [(x1, y1), (x2, y2)]