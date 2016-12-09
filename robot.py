import colours

import pygame

class Robot:
    def __init__(self):
        rect = pygame.Rect((20, 20), (20, 20))
        self.surf = pygame.Surface(rect.size)
        self.rect = pygame.draw.rect(self.surf, colours.BLACK, rect)