import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, lives=1):
        super().__init__(x, y, SHOT_RADIUS)
        self.lives = lives

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.kill()
