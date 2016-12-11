import pygame

from pygame.locals import *

import colours

class Button:
    def __init__(self, size, position, action):
        rect = pygame.Rect((0, 0), size)

        self.surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        self.rect = pygame.draw.rect(self.surf, colours.RED, rect)
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.action = action

    def eventHandler(self, event):
        if event.type == MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mousePos):
                return self.action

    def draw(self, surface):
        surface.blit(self.surf, self.rect)
