import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Pre-generate a jittered polygon so the shape stays stable each frame
        self.shape_points = self._generate_shape()

    def _generate_shape(self):
        """
        Build a noisy, roughly circular polygon around the center.
        Points are stored RELATIVE to the asteroid's center.
        """
        # More vertices = smoother; fewer = chunkier
        vertex_count = random.randint(8, 14)

        # How "lumpy" the outline is (as a fraction of radius)
        jitter = self.radius * 0.35

        points = []
        for i in range(vertex_count):
            angle = (i / vertex_count) * 360
            r = self.radius + random.uniform(-jitter, jitter)
            vec = pygame.Vector2(0, -r).rotate(angle)
            points.append(vec)
        return points

    def draw(self, screen):
        # Translate relative points by the current position
        poly = [self.position + p for p in self.shape_points]
        pygame.draw.polygon(screen, "white", poly, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # Remove this asteroid
        self.kill()

        # Stop if already at the smallest size
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Randomize split angle, create two smaller asteroids with rotated velocities
        random_angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(random_angle) * 1.2
        v2 = self.velocity.rotate(-random_angle) * 1.2

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a = Asteroid(self.position.x, self.position.y, new_radius)
        a.velocity = v1

        b = Asteroid(self.position.x, self.position.y, new_radius)
        b.velocity = v2
