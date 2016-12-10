import colours

import pygame, math

class Robot:
    def __init__(self, speed, startPos, angle=0):
        rect = pygame.Rect((0, 0), (20, 20))

        self.moving = False

        self.speed = 100
        self.surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        self.rect = pygame.draw.rect(self.surf, colours.BLACK, rect)
        self.rect.centerx = self.centerx = startPos[0]
        self.rect.centery = self.centery = startPos[1]
        self.angle = angle
        self.mask = pygame.mask.from_surface(self.surf)

    def findPoint(self, start, distance, timeDelta):
        if not self.moving:
            self.moving = True

        self.centerx += self.speed * timeDelta * math.cos(self.angle)
        self.centery += self.speed * timeDelta * math.sin(self.angle)

        self.rect.centerx = self.centerx;
        self.rect.centery = self.centery

        return math.sqrt((self.rect.centerx - start[0]) ** 2 + (self.rect.centery - start[1]) ** 2) >= distance

    def collision(self, destination):
        dx = self.rect.centerx - destination.rect.centerx
        dy = self.rect.centery - destination.rect.centery

        area1 = self.mask.scale((10,10)).overlap_area(destination.mask,(dx, dy))
        area2 = self.mask.scale((10,10)).overlap_area(destination.mask,(-dx, -dy))
        area3 = self.mask.scale((10,10)).overlap_area(destination.mask,(-dx, dy))
        area4 = self.mask.scale((10,10)).overlap_area(destination.mask,(dx, -dy))
        
        return max([ area1, area2, area3, area4 ])

    def findExit(self, center, radius, timeDelta, exit, direction):
        if not self.moving:
            self.moving = True

        currMaxArea = newMaxArea = 0

        collided = self.rect.colliderect(exit.rect)
        if collided:
            currMaxArea = self.collision(exit)
        
        self.angle += direction * timeDelta * (self.speed / radius)
        self.rect.centerx = self.centerx = radius * math.cos(self.angle) + center[0]
        self.rect.centery = self.centery = radius * math.sin(self.angle) + center[1]

        if collided:
            newMaxArea = self.collision(exit)

        return currMaxArea > newMaxArea and not currMaxArea == 0