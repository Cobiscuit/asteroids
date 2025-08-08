# player.py
import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.base_shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.shoot_cooldown = self.base_shoot_cooldown  # mutable
        self.fire_rate_tier = 0  # how many 1000-pt thresholds hit
        self.bullet_lives = 1  # how many asteroids a bullet can destroy

    def set_fire_rate_tier(self, tier: int):
        """Tier 0 = 100%, Tier 1 = 95%, Tier 2 = 90.25%, etc."""
        self.fire_rate_tier = max(0, tier)
        self.shoot_cooldown = self.base_shoot_cooldown * (0.95 ** self.fire_rate_tier)

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.move(dt)
        if keys[pygame.K_s]: self.move(-dt)
        if keys[pygame.K_a]: self.rotate(-dt)
        if keys[pygame.K_d]: self.rotate(dt)
        if keys[pygame.K_SPACE]: self.shoot()

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = self.shoot_cooldown  # <-- use current cooldown
        shot = Shot(self.position.x, self.position.y, lives=self.bullet_lives)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
