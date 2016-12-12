import pygame

from pygame.locals import *

import colours

class Button(object):
    def __init__(self, imageFile, position, action=None):
        self.surf = pygame.image.load(imageFile).convert()
        self.rect = self.surf.get_rect()
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
