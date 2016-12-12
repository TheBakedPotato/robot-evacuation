import pygame

import colours

class Destination(object):
    # Constructor for the Destination object
    def __init__(self, pos):
        rect = pygame.Rect((0, 0), (10, 10))

        # Setting up the surface of the object so it can be displayed and manipulated
        self.surf  = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        pygame.draw.rect(self.surf, colours.RED, rect)
        self.rect = self.surf.get_rect()

        # Positioning the destination
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

        # Creating the mask to be used for collisions
        self.mask = pygame.mask.from_surface(self.surf)

    # Draw the destination on a Surface
    # surface: the surface to draw the destination on
    def draw(self, surface):
        surface.blit(self.surf, self.rect)
