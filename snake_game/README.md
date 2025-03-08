# Enhanced Snake Game

A feature-rich Snake game created with Python and Pygame.

## Features

- **Interactive Menu System** - Configure game settings before playing
- **Multiple Difficulty Levels** - Easy, Medium, and Hard modes
- **Special Food Types**:
  - Regular Food (Red) - Adds 1 point and increases snake length
  - Bonus Food (Gold) - Adds 3 points and increases snake length by 3
  - Speed Up Food (Blue) - Temporarily increases snake speed
  - Slow Down Food (Purple) - Temporarily decreases snake speed
  - Shrink Food (Yellow) - Decreases snake length by 3
- **Wall Modes** - Play with walls that end the game on collision, or wrap-around mode
- **Dark Mode** - Play with a dark-themed interface
- **High Score System** - Your high score is saved between game sessions
- **Visual Indicators** - See active power-ups on screen
- **Pause Functionality** - Pause the game anytime with 'P' key

## Requirements

- Python 3.x
- Pygame library

## Installation

To run this game, you need to have Python and Pygame installed:

1. If you don't have Python installed, download and install it from [python.org](https://www.python.org/downloads/)
2. Install Pygame by running:
   ```
   pip install pygame
   ```

## How to Play

1. Run the game by executing:
   ```
   python snake_game.py
   ```
2. Use the menu to configure your game settings
3. Control the snake using the arrow keys:
   - Up arrow: Move up
   - Down arrow: Move down
   - Left arrow: Move left
   - Right arrow: Move right
4. Press 'P' to pause the game anytime
5. Collect different food types to score points and trigger special effects
6. Avoid hitting the walls (if wall mode is enabled) and your own snake body

## Game Controls

- **Arrow Keys**: Control snake direction
- **P Key**: Pause/resume game
- **Enter/Return**: Select menu option or restart after game over
- **M Key**: Return to menu after game over
- **Q Key**: Quit the game

## Game Mechanics

- The snake grows longer as it eats food
- Different food types have different effects
- The game gets progressively harder as your snake grows
- Special effects are temporary and will expire after a few seconds
- Your high score is automatically saved and displayed

Enjoy playing!
