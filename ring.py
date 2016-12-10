import pygame

import colours, destination

class Ring:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

        rect = pygame.Rect((0, 0), (self.radius * 2, self.radius * 2))
        self.ring_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.ring_surf.fill((255, 255, 255, 0))
        pygame.draw.circle(self.ring_surf, colours.BLUE, (self.radius, self.radius), self.radius, 1)
        self.ring_rect = self.ring_surf.get_rect()
        self.ring_rect.centerx = self.pos[0]
        self.ring_rect.centery = self.pos[1]

        self.exit = destination.Destination((pos[0] + radius, pos[1]))

    def draw(self, surface):
        surface.blit(self.ring_surf, self.ring_rect)
        self.exit.draw(surface)