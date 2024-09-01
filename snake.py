import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 960,720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
APPLE_RED = (233, 30, 99)
DARK_GREEN = (0, 153, 76)
LIGHT_GREEN = (102, 204, 102)
EYE_WHITE = (255, 255, 255)
EYE_BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
BACKGROUND_COLOR = (34, 40, 49)
CIRCLE_RED = (255, 0, 0)

# Define snake properties
SNAKE_BLOCK = 20
SNAKE_SPEED = 15

# Initialize clock and font
CLOCK = pygame.time.Clock()
FONT_STYLE = pygame.font.SysFont(None, 50)
BITE_SOUND = pygame.mixer.Sound("bite.wav")  # Load the sound effect

def draw_text(msg, color, position):
    mesg = FONT_STYLE.render(msg, True, color)
    WIN.blit(mesg, position)

def draw_apple(x, y):
    pygame.draw.circle(WIN, APPLE_RED, (x + SNAKE_BLOCK // 2, y + SNAKE_BLOCK // 2), SNAKE_BLOCK // 2)
    pygame.draw.rect(WIN, BROWN, [x + SNAKE_BLOCK // 2 - 2, y - 5, 4, 8])

def draw_snake(snake_list, direction):
    for i, pos in enumerate(snake_list):
        is_head = (i == len(snake_list) - 1)
        color = DARK_GREEN if i % 2 == 0 else LIGHT_GREEN
        draw_snake_segment(pos, direction if is_head else None, color, is_head)

        # Draw random red circles within the snake's body
        if not is_head and random.choice([True, False]):
            draw_random_red_circle(pos)

def draw_snake_segment(position, direction=None, color=None, is_head=False):
    rect = pygame.Rect(position[0], position[1], SNAKE_BLOCK, SNAKE_BLOCK)
    pygame.draw.rect(WIN, color or DARK_GREEN, rect, border_radius=5)

    if is_head:
        draw_eyes_and_tongue(position, direction)

def draw_eyes_and_tongue(position, direction):
    offsets = {
        "UP": [(6, 6), (SNAKE_BLOCK - 6, 6), (SNAKE_BLOCK // 2, -5), (SNAKE_BLOCK // 2, -15)],
        "DOWN": [(6, SNAKE_BLOCK - 6), (SNAKE_BLOCK - 6, SNAKE_BLOCK - 6), (SNAKE_BLOCK // 2, SNAKE_BLOCK + 5), (SNAKE_BLOCK // 2, SNAKE_BLOCK + 15)],
        "LEFT": [(6, 6), (6, SNAKE_BLOCK - 6), (-5, SNAKE_BLOCK // 2), (-15, SNAKE_BLOCK // 2)],
        "RIGHT": [(SNAKE_BLOCK - 6, 6), (SNAKE_BLOCK - 6, SNAKE_BLOCK - 6), (SNAKE_BLOCK + 5, SNAKE_BLOCK // 2), (SNAKE_BLOCK + 15, SNAKE_BLOCK // 2)],
    }

    eye_pos = [(position[0] + x, position[1] + y) for x, y in offsets[direction][:2]]
    tongue_pos = [(position[0] + offsets[direction][2][0], position[1] + offsets[direction][2][1]), 
                  (position[0] + offsets[direction][3][0], position[1] + offsets[direction][3][1])]

    for pos in eye_pos:
        pygame.draw.circle(WIN, EYE_WHITE, pos, 4)
        pygame.draw.circle(WIN, EYE_BLACK, pos, 2)

    if random.choice([True, False]):  # Randomly decide to extend or retract the tongue
        pygame.draw.line(WIN, APPLE_RED, tongue_pos[0], tongue_pos[1], 2)

def draw_random_red_circle(position):
    radius = random.randint(3, 8)
    center = (position[0] + random.randint(4, SNAKE_BLOCK-4), position[1] + random.randint(4, SNAKE_BLOCK-4))
    pygame.draw.circle(WIN, CIRCLE_RED, center, radius)

def generate_food_position():
    return round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0, round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

def game_loop():
    game_over = False
    game_close = False

    x, y = WIDTH / 2, HEIGHT / 2
    x_change, y_change = 0, 0
    direction = "RIGHT"

    snake_list = []
    length_of_snake = 1

    foodx, foody = generate_food_position()

    while not game_over:

        while game_close:
            WIN.fill(BLACK)
            draw_text("Game Over! Press Q-Quit or C-Play Again", APPLE_RED, [WIDTH / 6, HEIGHT / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                x_change, y_change, direction = handle_key_event(event, direction, x_change, y_change)

        x = (x + x_change) % WIDTH
        y = (y + y_change) % HEIGHT

        WIN.fill(BACKGROUND_COLOR)
        draw_apple(foodx, foody)

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        if snake_head in snake_list[:-1]:
            game_close = True

        draw_snake(snake_list, direction)
        pygame.display.update()

        if [x, y] == [foodx, foody]:
            foodx, foody = generate_food_position()
            length_of_snake += 1

            # Open mouth and play sound
            draw_open_mouth(snake_head, direction)
            BITE_SOUND.play()
            pygame.display.update()
            pygame.time.delay(100)  # Delay for effect

        CLOCK.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

def draw_open_mouth(position, direction):
    offsets = {
        "UP": [(SNAKE_BLOCK // 2, -10), (SNAKE_BLOCK // 2, SNAKE_BLOCK // 2)],
        "DOWN": [(SNAKE_BLOCK // 2, SNAKE_BLOCK + 10), (SNAKE_BLOCK // 2, SNAKE_BLOCK // 2)],
        "LEFT": [(-10, SNAKE_BLOCK // 2), (SNAKE_BLOCK // 2, SNAKE_BLOCK // 2)],
        "RIGHT": [(SNAKE_BLOCK + 10, SNAKE_BLOCK // 2), (SNAKE_BLOCK // 2, SNAKE_BLOCK // 2)],
    }
    
    mouth_pos = [(position[0] + x, position[1] + y) for x, y in offsets[direction]]
    pygame.draw.line(WIN, EYE_BLACK, mouth_pos[0], mouth_pos[1], 4)

def handle_key_event(event, current_direction, x_change, y_change):
    directions = {
        pygame.K_LEFT: ("LEFT", -SNAKE_BLOCK, 0),
        pygame.K_RIGHT: ("RIGHT", SNAKE_BLOCK, 0),
        pygame.K_UP: ("UP", 0, -SNAKE_BLOCK),
        pygame.K_DOWN: ("DOWN", 0, SNAKE_BLOCK),
    }

    if event.key in directions:
        new_direction, new_x_change, new_y_change = directions[event.key]
        if current_direction in ("LEFT", "RIGHT") and new_direction in ("UP", "DOWN"):
            return new_x_change, new_y_change, new_direction
        if current_direction in ("UP", "DOWN") and new_direction in ("LEFT", "RIGHT"):
            return new_x_change, new_y_change, new_direction

    return x_change, y_change, current_direction

game_loop()
