import pygame

import colours

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

        rect = pygame.Rect((0, 0), (10, 10))
        self.exit_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.exit_surf.fill((255, 255, 255, 0))
        pygame.draw.rect(self.exit_surf, colours.RED, pygame.Rect((0, 0,), (10, 10)))
        self.exit_rect = self.exit_surf.get_rect()
        self.exit_rect.centerx = self.pos[0] + radius
        self.exit_rect.centery = self.pos[1]

    def draw(self, surface):
        surface.blit(self.ring_surf, self.ring_rect)
        surface.blit(self.exit_surf, self.exit_rect)