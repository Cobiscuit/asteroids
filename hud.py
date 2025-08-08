import pygame
from constants import SCREEN_WIDTH

HUD_H = 40
HUD_PAD_Y = 6

class HUD:
    def __init__(self, font, columns):
        """
        columns: list of label strings, in order.
                 e.g. ["Score", "Lives", "Fire", "Bullets"]
        """
        self.font = font
        self.labels = columns
        self.values = [""] * len(columns)  # start blank
        self.bar_color = (40, 40, 40)
        self.label_color = (180, 180, 180)
        self.value_color = (255, 255, 255)

    def update_values(self, values):
        """Pass in list of strings (same length as labels)."""
        self.values = values

    def draw(self, screen):
        # Draw bar background
        pygame.draw.rect(screen, self.bar_color, (0, 0, SCREEN_WIDTH, HUD_H))

        col_w = SCREEN_WIDTH / max(1, len(self.labels))
        for i, (label, value) in enumerate(zip(self.labels, self.values)):
            label_surf = self.font.render(label.upper(), True, self.label_color)
            value_surf = self.font.render(value, True, self.value_color)

            cx = int((i + 0.5) * col_w)
            label_rect = label_surf.get_rect(midtop=(cx, HUD_PAD_Y))
            value_rect = value_surf.get_rect(midtop=(cx, HUD_PAD_Y + label_rect.height - 2))

            screen.blit(label_surf, label_rect)
            screen.blit(value_surf, value_rect)
