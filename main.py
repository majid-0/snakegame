import pygame
import random
from base import Snake, Apple, COLORS, CLOCK, FONT_STYLE, WIN, draw_text
from powerups import SlowDownPowerUp, ShrinkPowerUp, ScoreMultiplierPowerUp, InvincibilityPowerUp
from obstacles import Obstacle

class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()
        self.power_up = None
        self.obstacles = []
        self.score = 0
        self.multiplier = 1
        self.paused = False
        self.game_over = False
        self.obstacle_timer = 0

        self.settings = {
            "speed": 15,
            "DEFAULT_SPEED": 15,
            "controls": {
                "UP": pygame.K_UP,
                "DOWN": pygame.K_DOWN,
                "LEFT": pygame.K_LEFT,
                "RIGHT": pygame.K_RIGHT,
                "PAUSE": pygame.K_p,
            },
        }

    def start(self):
        self.spawn_power_up()
        self.game_loop()

    def pause_game(self):
        self.paused = not self.paused

    def draw(self):
        WIN.fill(COLORS["BACKGROUND_COLOR"])
        self.apple.draw()
        if self.power_up:
            self.power_up.draw()
        for obstacle in self.obstacles:
            obstacle.draw()
        self.snake.draw()
        draw_text(f"Score: {self.score} x{self.multiplier}", COLORS["APPLE_RED"], [10, 10])
        pygame.display.update()

    def game_loop(self):
        while not self.game_over:
            while self.paused:
                draw_text("Paused. Press P to resume.", COLORS["APPLE_RED"], [WIN.get_width() / 4, WIN.get_height() / 3])
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == self.settings["controls"]["PAUSE"]:
                        self.pause_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    self.snake.handle_key_event(event, self.settings["controls"])
                elif event.type == pygame.USEREVENT + 1:
                    # Handle power-up disappearance
                    if self.power_up and not self.power_up.active:
                        self.power_up = None
                        pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the disappearance timer
                elif event.type == pygame.USEREVENT + 2:
                    # Handle power-up effect expiration
                    if self.power_up and self.power_up.active:
                        self.power_up.deactivate(self)
                        self.power_up = None  # Remove the power-up completely

            self.snake.move()

            if self.snake.has_collided():
                self.handle_game_over()

            # Check for collision with apple first
            if self.snake.head_position() == self.apple.position:
                self.snake.grow()
                self.apple = Apple()
                self.score += 10 * self.multiplier
                self.multiplier += 1
                self.spawn_power_up()

            # Check for collision with power-up separately
            if self.power_up and self.snake.head_position() == self.power_up.position:
                self.power_up.activate(self)

            self.manage_obstacles()
            self.draw()
            CLOCK.tick(self.settings["speed"])

        pygame.quit()

    def handle_game_over(self):
        self.draw()  # Final draw to show the game state at the moment of game over
        draw_text("Game Over! Press Q to quit or R to restart", COLORS["APPLE_RED"], [WIN.get_width() / 8, WIN.get_height() / 3])
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_r:
                        self.__init__()  # Reset the game
                        self.start()

    def manage_obstacles(self):
        if len(self.snake.body) > 10:  # Start generating obstacles after the snake grows to a certain length
            if self.obstacle_timer == 0:
                self.obstacles.append(Obstacle())
                self.obstacle_timer = 200
            else:
                self.obstacle_timer -= 1
                if self.obstacle_timer == 0 and random.choice([True, False]):
                    self.obstacles.pop(0)

    def spawn_power_up(self):
        if not self.power_up:
            power_up_type = random.choice([SlowDownPowerUp, ShrinkPowerUp, ScoreMultiplierPowerUp, InvincibilityPowerUp])
            self.power_up = power_up_type()

if __name__ == "__main__":
    game = SnakeGame()
    game.start()
