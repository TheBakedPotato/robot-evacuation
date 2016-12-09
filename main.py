#!/usr/bin/python

# Pygame and external libraries
import pygame, sys

from pygame.locals import *

# Custom modules
import ring
import robot
import colours

class REMain:
    """The Main Robot Evacuation Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=480):
        self._running = False
        """Set the window Size"""
        self.size = self.width, self.height = width, height
        self.display_surf = None
        self.ring = ring.Ring(self.height / 2, (self.width / 2, self.height / 2))
        
    def _on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.display_surf.fill(colours.WHITE)
        self._running = True

    def _on_cleanup(self):
        self._running = False

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            self._on_cleanup()

    def main_loop(self):
        """This is the Main Loop of the Game"""
        if self._on_init() == False:
            self._running = False

        self._running = True
        while self._running:
            for event in pygame.event.get():
                self._on_event(event)
            self.ring.draw(self.display_surf)
            pygame.display.update()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = REMain()
    app.main_loop()
