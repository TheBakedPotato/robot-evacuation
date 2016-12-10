import pygame

import colours

class Ring:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

        rect = pygame.Rect((0, 0), (self.radius * 2, self.radius * 2))

        self.surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        self.rect = pygame.draw.circle(self.surf, colours.BLUE, (self.radius, self.radius), self.radius, 1)
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]

    def draw(self, surface):
        surface.blit(self.surf, self.rect)