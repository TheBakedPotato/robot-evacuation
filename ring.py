import pygame

import colours

class Ring:
    def __init__(self, radius, pos):
        self.radius = radius
        self.pos = pos

    def draw(self, surface):
        pygame.draw.circle(surface, colours.BLACK, self.pos, self.radius, 4)