import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from hud import HUD
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    # HUD
    font = pygame.font.Font(None, 28)
    hud = HUD(font, ["Score", "Lives", "Fire", "Bullets"])

    # Score & lives
    score = 0
    lives = PLAYER_START_LIVES

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Containers
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)   # not drawable; just spawns
    Player.containers = (updatable, drawable)

    # Spawner + player
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Scaling state
    fire_rate_tier = 0               # every 1,000 points → -5% delay
    player.set_fire_rate_tier(fire_rate_tier)

    bullet_life_tier = 0            # every 10,000 points → +1 bullet life
    player.bullet_lives = 1 + bullet_life_tier

    # Respawn / invulnerability
    invuln = 0.0
    dt = 0.0
    running = True

    while running:
        # ---- events ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ---- update world ----
        updatable.update(dt)

        if invuln > 0:
            invuln -= dt

        # Player–asteroid collisions (skip when invulnerable)
        if invuln <= 0 and player.alive():
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    lives -= 1
                    player.kill()
                    if lives > 0:
                        # Respawn fresh player; reapply upgrades
                        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.set_fire_rate_tier(fire_rate_tier)
                        player.bullet_lives = 1 + bullet_life_tier
                        invuln = 1.5
                    else:
                        print(f"Game Over!\nFinal Score: {score}")
                        running = False
                    break

        # Shot–asteroid collisions (shots can have multiple lives)
        for asteroid in list(asteroids):
            for shot in list(shots):
                if asteroid.collides_with(shot):
                    score += 100
                    asteroid.split()
                    shot.hit()  # decrements and kills only at 0

                    # Fire rate scaling: every 1,000 points
                    new_fire_tier = score // 1000
                    if new_fire_tier != fire_rate_tier:
                        fire_rate_tier = new_fire_tier
                        player.set_fire_rate_tier(fire_rate_tier)

                    # Bullet lives scaling: every 10,000 points
                    new_bullet_life_tier = score // 10000
                    if new_bullet_life_tier != bullet_life_tier:
                        bullet_life_tier = new_bullet_life_tier
                        player.bullet_lives = 1 + bullet_life_tier

        # ---- draw ----
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)

        # HUD values
        fire_mult = 1.0 / (player.shoot_cooldown / player.base_shoot_cooldown)
        hud.update_values([
            f"{score:,}",
            str(lives),
            f"x{fire_mult:.2f}",
            f"{player.bullet_lives}x",
        ])
        hud.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

    pygame.quit()

if __name__ == "__main__":
    main()
