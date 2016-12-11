import pygame

import colours

class Destination(object):
    def __init__(self, pos):
        rect = pygame.Rect((0, 0), (10, 10))

        self.surf  = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        pygame.draw.rect(self.surf, colours.RED, rect)
        self.rect = self.surf.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.mask = pygame.mask.from_surface(self.surf)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)
