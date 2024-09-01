import pygame
import random
from base import SNAKE_BLOCK, COLORS, WIN

class PowerUp:
    def __init__(self, color, effect, effect_duration=5000, disappear_time=3000):
        self.position = self.generate_position()
        self.color = color
        self.effect = effect
        self.effect_duration = effect_duration
        self.disappear_time = disappear_time
        self.active = False

        # Set timer for power-up disappearance after 3 seconds
        pygame.time.set_timer(pygame.USEREVENT + 1, self.disappear_time)

    def generate_position(self):
        return [
            round(random.randrange(0, WIN.get_width() - SNAKE_BLOCK) / 20.0) * 20.0,
            round(random.randrange(0, WIN.get_height() - SNAKE_BLOCK) / 20.0) * 20.0,
        ]

    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.position[0] + SNAKE_BLOCK // 2, self.position[1] + SNAKE_BLOCK // 2), SNAKE_BLOCK // 2)

    def activate(self, game):
        if not self.active:
            self.effect(game)
            self.active = True
            # Set timer for power-up effect duration
            pygame.time.set_timer(pygame.USEREVENT + 2, self.effect_duration)
            # Remove the power-up from the game visually
            game.power_up = None
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the disappearance timer

    def deactivate(self, game):
        # Reset game state after power-up expires
        game.settings["speed"] = game.settings["DEFAULT_SPEED"]
        game.snake.invincible = False
        game.multiplier = 1
        self.active = False
        pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Stop the effect timer

class SlowDownPowerUp(PowerUp):
    def __init__(self):
        super().__init__(COLORS["POWER_UP_BLUE"], self.slow_down)

    def slow_down(self, game):
        game.settings["speed"] = game.settings["DEFAULT_SPEED"] // 2

class ShrinkPowerUp(PowerUp):
    def __init__(self):
        super().__init__(COLORS["POWER_UP_PURPLE"], self.shrink)

    def shrink(self, game):
        if game.snake.length > 3:
            game.snake.body = game.snake.body[:-3]
            game.snake.length -= 3

class ScoreMultiplierPowerUp(PowerUp):
    def __init__(self):
        super().__init__(COLORS["POWER_UP_GREEN"], self.multiply_score)

    def multiply_score(self, game):
        game.multiplier = 2

class InvincibilityPowerUp(PowerUp):
    def __init__(self):
        super().__init__(COLORS["POWER_UP_STAR"], self.invincible)

    def invincible(self, game):
        game.snake.invincible = True
