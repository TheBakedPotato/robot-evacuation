import pygame, random, math

import colours, destination

class Ring:
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

        if not exitPos:
            angle = (2 * math.pi) * random.random()
            exitX = self.pos[0] + radius * math.cos(angle)
            exitY = self.pos[1] + radius * math.sin(angle)
            exitPos = (exitX, exitY)

        self.exit = destination.Destination(exitPos)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)
        self.exit.draw(surface)