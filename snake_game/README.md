# Ultimate Snake Game

A feature-rich Snake game created with Python and Pygame, featuring modern graphics, special effects, and extensive customization options. Now playable both on desktop and in web browsers!

## Features

### Gameplay Features
- **Multiple Difficulty Levels** - Choose from Easy, Medium, and Hard modes
- **Progressive Difficulty** - Game gets harder as you level up
- **Level System** - Advance through levels by collecting food
- **Statistics Tracking** - Track your gameplay stats across multiple sessions
- **High Score System** - Beat your previous best scores

### Special Foods and Power-ups
- **Regular Food (Red Apple)** - +1 point and length
- **Bonus Food (Gold Star)** - +3 points and increases length by 3
- **Speed Up Food (Blue Lightning)** - Temporarily increases snake speed
- **Slow Down Food (Purple Clock)** - Temporarily decreases snake speed
- **Shrink Food (Yellow Arrow)** - Decreases snake length by 3
- **Ghost Food (Cyan)** - Pass through walls and your own body temporarily
- **Double Score Food (Orange)** - Score twice as many points for a limited time
- **Rainbow Food (Magenta)** - Changes snake to rainbow pattern
- **Freeze Food (Gray Snowflake)** - Temporarily stops snake movement

### Visual Features
- **Dark Mode** - Play with a dark-themed interface
- **Particle Effects** - Visual effects when collecting food or game over
- **Snake Styles** - Multiple visual styles for the snake (Classic, Gradient, Patterned)
- **Food Animations** - Animated food with special effects
- **Background Options** - Grid, Gradient, or Plain backgrounds
- **Direction-Aware Snake Eyes** - Snake eyes follow its direction of movement

### Interface
- **Comprehensive Menu System** - Configure all aspects of the game
- **Game Statistics** - View detailed stats about your gameplay
- **Enhanced Pause Menu** - Pause anytime with multiple options
- **Game Over Screen** - Detailed game over screen with final stats
- **Visual Effect Timers** - See how long power-ups will last

### Other Features
- **Alternative Control Schemes** - Choose between Arrow keys or WASD
- **Sound Effects** - Optional sound effects for game actions
- **Extensive Customization** - Personalize your gameplay experience
- **Time Tracking** - Keep track of your total play time

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
3. Control the snake using the arrow keys or WASD (depending on your settings):
   - Arrow Keys/WASD: Move snake in the corresponding direction
   - P: Pause/resume game
   - M: Return to menu (during pause)
   - ESC: Quit the game
4. Collect different food types to score points and trigger special effects
5. Avoid hitting the walls (if wall mode is enabled) and your own snake body
6. Level up by collecting enough food to reach the target score

## Game Mechanics

- The snake grows longer as it eats food
- Different food types have different effects
- Special effects are temporary and will expire after a few seconds
- The game gets progressively harder as you level up
- Your high score and stats are automatically saved between sessions
- Food will disappear after a while and respawn in a new location

## Customization Options

- **Difficulty**: Easy, Medium, Hard
- **Wall Mode**: On/Off
- **Special Foods**: On/Off
- **Sound**: On/Off
- **Particles**: On/Off
- **Background Style**: Grid, None, Gradient
- **Snake Style**: Classic, Gradient, Patterned
- **Food Style**: Simple, Animated, Realistic
- **Control Scheme**: Arrow keys, WASD

## Web Deployment

This game can now be played directly in web browsers! No installation required for players.

### For Players
- Just visit the game's web page in a modern browser (Chrome, Firefox, Edge, Safari)
- No downloads or plugins needed
- Enjoy the full game experience online

### For Developers
- Deploy the game to itch.io, GitHub Pages, or any web server
- Share with anyone via a simple URL
- See the included `WEB_DEPLOYMENT_GUIDE.md` for detailed instructions

Enjoy playing the Ultimate Snake Game!
