import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Snake Game")

# Define default colors
# Define default colors
COLORS = {
    "BLACK": (0, 0, 0),
    "APPLE_RED": (233, 30, 99),
    "DARK_GREEN": (0, 153, 76),
    "LIGHT_GREEN": (102, 204, 102),
    "EYE_WHITE": (255, 255, 255),
    "EYE_BLACK": (0, 0, 0),
    "BROWN": (139, 69, 19),
    "BACKGROUND_COLOR": (34, 40, 49),
    "POWER_UP_BLUE": (0, 0, 255),  # Color for SlowDownPowerUp
    "POWER_UP_PURPLE": (128, 0, 128),  # Color for ShrinkPowerUp
    "POWER_UP_GREEN": (0, 255, 0),  # Color for ScoreMultiplierPowerUp
    "POWER_UP_STAR": (255, 255, 0),  # Color for InvincibilityPowerUp
}


# Define snake properties
SNAKE_BLOCK = 20
DEFAULT_SPEED = 15

# Initialize clock and font
CLOCK = pygame.time.Clock()
FONT_STYLE = pygame.font.SysFont(None, 50)

class Snake:
    def __init__(self):
        self.body = [[WIDTH / 2, HEIGHT / 2]]
        self.direction = "RIGHT"
        self.length = 1
        self.speed_boosted = False
        self.invincible = False

    def head_position(self):
        return self.body[-1]

    def draw(self):
        for i, pos in enumerate(self.body):
            color = COLORS["DARK_GREEN"] if i % 2 == 0 else COLORS["LIGHT_GREEN"]
            pygame.draw.rect(WIN, color, pygame.Rect(pos[0], pos[1], SNAKE_BLOCK, SNAKE_BLOCK))
            if not self.is_head(pos):
                draw_random_red_circle(pos)
        if self.is_head(self.head_position()):
            draw_eyes_and_tongue(self.head_position(), self.direction)

    def is_head(self, position):
        return position == self.head_position()

    def move(self):
        x, y = self.head_position()
        x_change, y_change = 0, 0

        if self.direction == "UP":
            y_change = -SNAKE_BLOCK
        elif self.direction == "DOWN":
            y_change = SNAKE_BLOCK
        elif self.direction == "LEFT":
            x_change = -SNAKE_BLOCK
        elif self.direction == "RIGHT":
            x_change = SNAKE_BLOCK

        # Update the snake's head position with wrapping
        new_head = [(x + x_change) % WIDTH, (y + y_change) % HEIGHT]
        self.body.append(new_head)

        if len(self.body) > self.length:
            del self.body[0]

    def grow(self):
        self.length += 1

    def handle_key_event(self, event, keys):
        if event.key == keys["UP"] and self.direction != "DOWN":
            self.direction = "UP"
        elif event.key == keys["DOWN"] and self.direction != "UP":
            self.direction = "DOWN"
        elif event.key == keys["LEFT"] and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif event.key == keys["RIGHT"] and self.direction != "LEFT":
            self.direction = "RIGHT"

    def has_collided(self):
        head = self.head_position()
        if head in self.body[:-1] and not self.invincible:
            return True
        return False

class Apple:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        return [
            round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0,
            round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0,
        ]

    def draw(self):
        draw_apple(self.position[0], self.position[1])

# Helper functions
def draw_text(msg, color, position):
    mesg = FONT_STYLE.render(msg, True, color)
    WIN.blit(mesg, position)

def draw_apple(x, y):
    pygame.draw.circle(WIN, COLORS["APPLE_RED"], (x + SNAKE_BLOCK // 2, y + SNAKE_BLOCK // 2), SNAKE_BLOCK // 2)
    pygame.draw.rect(WIN, COLORS["BROWN"], [x + SNAKE_BLOCK // 2 - 2, y - 5, 4, 8])

def draw_eyes_and_tongue(position, direction):
    offsets = {
        "UP": [(6, 6), (SNAKE_BLOCK - 6, 6), (SNAKE_BLOCK // 2, -5), (SNAKE_BLOCK // 2, -15)],
        "DOWN": [(6, SNAKE_BLOCK - 6), (SNAKE_BLOCK - 6, SNAKE_BLOCK - 6), (SNAKE_BLOCK // 2, SNAKE_BLOCK + 5), (SNAKE_BLOCK // 2, SNAKE_BLOCK + 15)],
        "LEFT": [(6, 6), (6, SNAKE_BLOCK - 6), (-5, SNAKE_BLOCK // 2), (-15, SNAKE_BLOCK // 2)],
        "RIGHT": [(SNAKE_BLOCK - 6, 6), (SNAKE_BLOCK - 6, SNAKE_BLOCK - 6), (SNAKE_BLOCK + 5, SNAKE_BLOCK // 2), (SNAKE_BLOCK + 15, SNAKE_BLOCK // 2)],
    }

    eye_pos = [(position[0] + x, position[1] + y) for x, y in offsets[direction][:2]]
    tongue_pos = [
        (position[0] + offsets[direction][2][0], position[1] + offsets[direction][2][1]),
        (position[0] + offsets[direction][3][0], position[1] + offsets[direction][3][1]),
    ]

    for pos in eye_pos:
        pygame.draw.circle(WIN, COLORS["EYE_WHITE"], pos, 4)
        pygame.draw.circle(WIN, COLORS["EYE_BLACK"], pos, 2)

    if random.choice([True, False]):  # Randomly decide to extend or retract the tongue
        pygame.draw.line(WIN, COLORS["APPLE_RED"], tongue_pos[0], tongue_pos[1], 2)

def draw_random_red_circle(position):
    radius = random.randint(3, 8)
    center = (position[0] + random.randint(4, SNAKE_BLOCK - 4), position[1] + random.randint(4, SNAKE_BLOCK - 4))
    pygame.draw.circle(WIN, COLORS["APPLE_RED"], center, radius)

