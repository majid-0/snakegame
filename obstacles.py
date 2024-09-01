import pygame
import random
from base import SNAKE_BLOCK, COLORS, WIN

class Obstacle:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        return [
            round(random.randrange(0, WIN.get_width() - SNAKE_BLOCK) / 20.0) * 20.0,
            round(random.randrange(0, WIN.get_height() - SNAKE_BLOCK) / 20.0) * 20.0,
        ]

    def draw(self):
        pygame.draw.rect(WIN, COLORS["OBSTACLE_COLOR"], pygame.Rect(self.position[0], self.position[1], SNAKE_BLOCK, SNAKE_BLOCK))
