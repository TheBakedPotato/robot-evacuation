import colours

import pygame, math

class Robot(object):
    def __init__(self, speed, startPos, direction=1, colour):
        rect = pygame.Rect((0, 0), (20, 20))

        self.colour = colour
        self.surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))
        self.rect = pygame.draw.rect(self.surf, colour, rect)
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect.centerx = self.centerx = float(startPos[0])
        self.rect.centery = self.centery = float(startPos[1])

        self.moving = False
        self.speed = 100.0
        self.dest = None
        self.angle = None
        self.direction = direction
        self.onPerimeter = False
        self.evacuated = False
        self.ringPos = None
        self.travelled = []

    def findPoint(self, pos, timeDelta):
        if not self.dest == pos:
            self.dest = (float(pos[0]), float(pos[1]))
            dx = self.dest[0] - self.centerx
            dy = self.dest[1] - self.centery

            self.angle = math.atan2(dy, dx)
            if self.angle < 0:
                self.angle += 2 * math.pi

        currDistance = math.sqrt((self.centerx - self.dest[0]) ** 2 + (self.centery - self.dest[1]) ** 2)
        
        if len(self.travelled) > 0:
            lastPos = self.travelled[-1]
            if not (lastPos[0] == self.rect.centerx and lastPos[1] == self.travelled[-1]):
                self.travelled.append((self.rect.centerx, self.rect.centery))
        else:
            self.travelled.append((self.rect.centerx, self.rect.centery))

        self.centerx += self.speed * timeDelta * math.cos(self.angle)
        self.centery += self.speed * timeDelta * math.sin(self.angle)

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        newDistance = math.sqrt((self.centerx - self.dest[0]) ** 2 + (self.centery - self.dest[1]) ** 2)

        return (currDistance - newDistance) < 0

    def collision(self, destination):
        dx = self.rect.centerx - destination.rect.centerx
        dy = self.rect.centery - destination.rect.centery

        area1 = self.mask.scale(destination.rect.size).overlap_area(destination.mask,(dx, dy))
        area2 = self.mask.scale(destination.rect.size).overlap_area(destination.mask,(-dx, -dy))
        area3 = self.mask.scale(destination.rect.size).overlap_area(destination.mask,(-dx, dy))
        area4 = self.mask.scale(destination.rect.size).overlap_area(destination.mask,(dx, -dy))
        
        return max([ area1, area2, area3, area4 ])

    def findExitOnRing(self, ring, timeDelta):
        if not self.ringPos == (ring.rect.centerx, ring.rect.centery):
            self.ringPos = (float(ring.rect.centerx), float(ring.rect.centery))
            dx = self.centerx - self.ringPos[0]
            dy = self.centery - self.ringPos[1]

            self.angle = math.atan2(dy, dx)
            if self.angle < 0:
                self.angle += 2 * math.pi

        currMaxArea = newMaxArea = 0

        if len(self.travelled) > 0:
            lastPos = self.travelled[-1]
            if not (lastPos[0] == self.rect.centerx and lastPos[1] == self.travelled[-1]):
                self.travelled.append((self.rect.centerx, self.rect.centery))
        else:
            self.travelled.append((self.rect.centerx, self.rect.centery))

        collided = self.rect.colliderect(ring.exit.rect)
        if collided:
            currMaxArea = self.collision(ring.exit)
        
        self.angle += self.direction * timeDelta * (self.speed / ring.radius)
        self.rect.centerx = self.centerx = ring.radius * math.cos(self.angle) + self.ringPos[0]
        self.rect.centery = self.centery = ring.radius * math.sin(self.angle) + self.ringPos[1]

        if collided:
            newMaxArea = self.collision(ring.exit)

        return currMaxArea > newMaxArea and not currMaxArea == 0

    def drawRobot(self, surface):
        surface.blit(self.surf, self.rect)

    def drawTravelledLine(self, surface):
        if len(self.travelled) > 1:
            pygame.draw.lines(surface, self.colour, False, self.travelled, 3)