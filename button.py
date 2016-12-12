import pygame

from pygame.locals import *

import colours

class Button(object):
    # Constructor for the Button class
    def __init__(self, imageFile, position, action=None):

        # Setting up the Surface so the button can be displayed and moved/positioned
        self.surf = pygame.image.load(imageFile).convert()
        self.rect = self.surf.get_rect()

        # Positioning the button
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

        # The action to return if the event was triggered
        self.action = action

    # Returns the action to execute if the event was triggered
    # event: the Event that occurred
    def eventHandler(self, event):
        # Only triggeres if it was a MOUSEBUTTONUP action and the mousepoint collides with the button
        if event.type == MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mousePos):
                return self.action

    # Draws the button on a Surface
    # surface: the Surface to draw the button on
    def draw(self, surface):
        surface.blit(self.surf, self.rect)
