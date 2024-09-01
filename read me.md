# Snake Game

This is a modern take on the classic Snake Game, implemented using Python and Pygame. This version features smooth controls, dynamic obstacles, power-ups, and a scoring system that adds a new layer of challenge and fun to the traditional gameplay.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Controls](#game-controls)
- [Power-Ups](#power-ups)
- [Obstacles](#obstacles)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Snake Game is a simple arcade game where you control a snake with the goal of eating apples to grow longer. As you progress, the game becomes increasingly challenging with the introduction of dynamic obstacles and various power-ups that can either aid or hinder your progress.

## Features

- **Classic Snake Gameplay**: Enjoy the nostalgia of the traditional snake game with modern enhancements.
- **Power-Ups**: Collect various power-ups to gain temporary abilities such as invincibility, score multipliers, speed reduction, and snake shrinking.
- **Dynamic Obstacles**: Navigate through randomly appearing obstacles that increase the challenge as your snake grows longer.
- **Smooth Motion and Controls**: Experience fluid snake movement with responsive controls.
- **Scoring System**: Track your score and aim for the highest possible.

## Requirements

- **Python**: Version 3.x is required.
- **Pygame**: The Pygame library is necessary to run the game.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/snakegame.git
   cd snakegame
Install the required packages:
bash
Copy code
pip install pygame
Run the game:

bash
Copy code
python main.py
How to Play
The objective is to control the snake and eat as many apples as possible to grow longer.
Avoid colliding with the snake's own body or the obstacles that appear on the screen.
Collect power-ups to gain temporary advantages, but be mindful of their timers.
The game ends if the snake collides with itself or an obstacle.
Game Controls
Arrow Keys: Control the direction of the snake.
P: Pause/Unpause the game.
Q: Quit the game after a game-over.
R: Restart the game after a game-over.
Power-Ups
Throughout the game, various power-ups will appear on the screen. Each power-up offers a unique temporary advantage:

Slow Down (Blue): Slows down the snake's speed for 5 seconds, making it easier to navigate tight spaces.
Shrink (Purple): Reduces the length of the snake by 3 segments, giving you more room to maneuver.
Score Multiplier (Green): Doubles the points you earn for eating apples for 5 seconds.
Invincibility (Star): Grants the snake invincibility for 5 seconds, allowing it to pass through obstacles and itself without dying.
Power-Up Timers
Disappearance Timer: Power-ups will disappear 3 seconds after they appear if not collected.
Effect Timer: Once collected, the power-up effect will last for 5 seconds.
Obstacles
Dynamic Obstacles: As the snake grows longer, obstacles will randomly appear on the screen.
Challenge: The player must navigate around these obstacles to avoid a game-over.
Obstacle Timing: Obstacles appear after the snake reaches a certain length and disappear after a while.
Known Issues
Simultaneous Collision: If the snake eats both an apple and a power-up at the exact same time, unexpected behavior may occur. Sequential collision handling has been implemented to mitigate this, but further testing is encouraged.
Power-Up Overlap: Occasionally, power-ups may spawn too close to obstacles, making them hard to reach. Future updates may address this by refining the spawn logic.