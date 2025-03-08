import pygame
import time
import random
import sys
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()  # For sound effects

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)

# Set display dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
GRID_SIZE = 20

# Sound effects paths (create an empty sounds directory)
os.makedirs("C:\\Users\\toprak\\Desktop\\command-and-claude\\claudeworkspace\\snake_game\\sounds", exist_ok=True)

# Game settings
class GameSettings:
    def __init__(self):
        self.difficulty = "medium"  # "easy", "medium", "hard"
        self.snake_speed = 15
        self.walls_enabled = False
        self.special_foods = True
        self.dark_mode = False
        
    def update_speed(self):
        if self.difficulty == "easy":
            self.snake_speed = 10
        elif self.difficulty == "medium":
            self.snake_speed = 15
        elif self.difficulty == "hard":
            self.snake_speed = 25

# Food types and their properties
class FoodType:
    def __init__(self, color, points, duration=None, effect=None):
        self.color = color
        self.points = points
        self.duration = duration  # For temporary effects
        self.effect = effect      # Function to call when eaten

# Define food types
FOODS = {
    "regular": FoodType(RED, 1),
    "bonus": FoodType(GOLD, 3),
    "speed_up": FoodType(BLUE, 1),
    "slow_down": FoodType(PURPLE, 1),
    "shrink": FoodType(YELLOW, -3)  # Reduces length by 3 (min length is 1)
}

class Snake:
    def __init__(self, block_size):
        self.block_size = block_size
        # Start at center of screen
        self.x = DISPLAY_WIDTH // 2
        self.y = DISPLAY_HEIGHT // 2
        # Initial movement (no movement)
        self.dx = 0
        self.dy = 0
        # Initialize snake body
        self.body = []
        self.length = 1
        # Snake head at start
        self.head = [self.x, self.y]
        self.body.append(self.head)
        # Current effects
        self.effects = {}  # {effect_name: expiry_time}
        
    def update(self):
        # Move snake
        self.x += self.dx
        self.y += self.dy
        
        # Update head position
        self.head = [self.x, self.y]
        self.body.append(self.head)
        
        # Remove tail if snake is longer than it should be
        if len(self.body) > self.length:
            del self.body[0]
            
    def grow(self, amount=1):
        """Increase snake length"""
        self.length += amount
        if self.length < 1:  # Minimum length
            self.length = 1
            
    def check_collision_with_self(self):
        """Check if snake head collides with its body"""
        for segment in self.body[:-1]:  # All segments except head
            if segment == self.head:
                return True
        return False
    
    def check_collision_with_walls(self, wrap_around=False):
        """Check if snake hits the walls"""
        if wrap_around:
            # Wrap around the screen
            if self.x >= DISPLAY_WIDTH:
                self.x = 0
            elif self.x < 0:
                self.x = DISPLAY_WIDTH - self.block_size
            if self.y >= DISPLAY_HEIGHT:
                self.y = 0
            elif self.y < 0:
                self.y = DISPLAY_HEIGHT - self.block_size
            return False
        else:
            # Game over if snake hits wall
            if (self.x >= DISPLAY_WIDTH or self.x < 0 or 
                self.y >= DISPLAY_HEIGHT or self.y < 0):
                return True
        return False
        
    def draw(self, display, dark_mode=False):
        """Draw the snake on screen"""
        for i, segment in enumerate(self.body):
            # Head is slightly different color
            if i == len(self.body) - 1:  # Head
                color = (0, 200, 0) if not dark_mode else (0, 150, 0)
            else:
                color = GREEN if not dark_mode else DARK_GREEN
            pygame.draw.rect(display, color, 
                [segment[0], segment[1], self.block_size, self.block_size])
            
        # Draw eyes on snake head (only if we have a head)
        if self.body:
            head = self.body[-1]
            eye_color = BLACK if not dark_mode else WHITE
            # Left eye
            pygame.draw.circle(display, eye_color, 
                               (head[0] + 5, head[1] + 5), 2)
            # Right eye
            pygame.draw.circle(display, eye_color, 
                               (head[0] + self.block_size - 5, head[1] + 5), 2)

class Food:
    def __init__(self, block_size):
        self.block_size = block_size
        self.type = "regular"
        self.respawn()
        self.special_food_timer = 0
        
    def respawn(self):
        """Place food at random location"""
        self.x = round(random.randrange(0, DISPLAY_WIDTH - self.block_size) / 
                      self.block_size) * self.block_size
        self.y = round(random.randrange(0, DISPLAY_HEIGHT - self.block_size) / 
                      self.block_size) * self.block_size
        
        # Randomly choose a food type if special foods are enabled
        if GameSettings().special_foods and random.random() < 0.2:  # 20% chance for special food
            food_types = list(FOODS.keys())
            self.type = random.choice(food_types)
        else:
            self.type = "regular"
            
    def draw(self, display, dark_mode=False):
        """Draw the food on screen"""
        food_color = FOODS[self.type].color
        
        # Different shapes for different food types
        if self.type == "regular":
            pygame.draw.rect(display, food_color, 
                            [self.x, self.y, self.block_size, self.block_size])
        elif self.type == "bonus":
            pygame.draw.rect(display, food_color, 
                            [self.x, self.y, self.block_size, self.block_size])
            # Draw star pattern
            points = [
                (self.x + self.block_size//2, self.y),
                (self.x + self.block_size, self.y + self.block_size//2),
                (self.x + self.block_size//2, self.y + self.block_size),
                (self.x, self.y + self.block_size//2)
            ]
            pygame.draw.polygon(display, YELLOW, points)
        elif self.type == "speed_up":
            pygame.draw.circle(display, food_color,
                               (self.x + self.block_size//2, self.y + self.block_size//2),
                                self.block_size//2)
        elif self.type == "slow_down":
            pygame.draw.circle(display, food_color,
                               (self.x + self.block_size//2, self.y + self.block_size//2),
                                self.block_size//2)
            pygame.draw.circle(display, BLACK,
                               (self.x + self.block_size//2, self.y + self.block_size//2),
                                self.block_size//4)
        elif self.type == "shrink":
            # Draw triangle for shrink
            points = [
                (self.x, self.y),
                (self.x + self.block_size, self.y),
                (self.x + self.block_size//2, self.y + self.block_size)
            ]
            pygame.draw.polygon(display, food_color, points)

class Game:
    def __init__(self):
        # Set up the game display
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Enhanced Snake Game')
        
        # Set game clock
        self.clock = pygame.time.Clock()
        
        # Set fonts
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.title_font = pygame.font.SysFont("comicsansms", 50)
        
        # Game objects
        self.settings = GameSettings()
        self.snake = Snake(GRID_SIZE)
        self.food = Food(GRID_SIZE)
        
        # Game state
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.game_paused = False
        
        # Power-ups and effects
        self.active_effects = {}  # {effect_name: expiry_time}
        self.snake_speed_modifier = 0
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open("C:\\Users\\toprak\\Desktop\\command-and-claude\\claudeworkspace\\snake_game\\high_score.txt", "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0
            
    def save_high_score(self):
        """Save high score to file"""
        with open("C:\\Users\\toprak\\Desktop\\command-and-claude\\claudeworkspace\\snake_game\\high_score.txt", "w") as f:
            f.write(str(self.high_score))
    
    def show_score(self):
        """Display current score and high score on screen"""
        bg_color = BLACK if self.settings.dark_mode else WHITE
        text_color = WHITE if self.settings.dark_mode else BLACK
        
        score_text = self.score_font.render(f"Score: {self.score}", True, text_color)
        self.display.blit(score_text, [10, 10])
        
        high_score_text = self.score_font.render(f"High Score: {self.high_score}", True, text_color)
        high_score_width = high_score_text.get_width()
        self.display.blit(high_score_text, [DISPLAY_WIDTH - high_score_width - 10, 10])
        
    def show_message(self, msg, color, y_displace=0):
        """Display message on screen"""
        mesg = self.font_style.render(msg, True, color)
        self.display.blit(mesg, [DISPLAY_WIDTH // 6, DISPLAY_HEIGHT // 3 + y_displace])
        
    def draw_grid(self):
        """Draw grid on the game screen"""
        if not self.settings.dark_mode:
            grid_color = (230, 230, 230)  # Light gray
        else:
            grid_color = (50, 50, 50)  # Dark gray
            
        for x in range(0, DISPLAY_WIDTH, GRID_SIZE):
            pygame.draw.line(self.display, grid_color, (x, 0), (x, DISPLAY_HEIGHT))
        for y in range(0, DISPLAY_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.display, grid_color, (0, y), (DISPLAY_WIDTH, y))
            
    def show_menu(self):
        """Display game menu"""
        menu_open = True
        selected_option = 0
        menu_options = ["Start Game", "Difficulty: " + self.settings.difficulty, 
                        "Walls: " + ("On" if self.settings.walls_enabled else "Off"),
                        "Special Foods: " + ("On" if self.settings.special_foods else "Off"),
                        "Dark Mode: " + ("On" if self.settings.dark_mode else "Off"),
                        "Quit"]
                        
        while menu_open:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        # Handle menu selection
                        if selected_option == 0:  # Start Game
                            menu_open = False
                        elif selected_option == 1:  # Difficulty
                            if self.settings.difficulty == "easy":
                                self.settings.difficulty = "medium"
                            elif self.settings.difficulty == "medium":
                                self.settings.difficulty = "hard"
                            else:
                                self.settings.difficulty = "easy"
                            self.settings.update_speed()
                            menu_options[1] = "Difficulty: " + self.settings.difficulty
                        elif selected_option == 2:  # Walls
                            self.settings.walls_enabled = not self.settings.walls_enabled
                            menu_options[2] = "Walls: " + ("On" if self.settings.walls_enabled else "Off")
                        elif selected_option == 3:  # Special Foods
                            self.settings.special_foods = not self.settings.special_foods
                            menu_options[3] = "Special Foods: " + ("On" if self.settings.special_foods else "Off")
                        elif selected_option == 4:  # Dark Mode
                            self.settings.dark_mode = not self.settings.dark_mode
                            menu_options[4] = "Dark Mode: " + ("On" if self.settings.dark_mode else "Off")
                        elif selected_option == 5:  # Quit
                            pygame.quit()
                            sys.exit()
            
            # Draw menu
            bg_color = (20, 20, 20) if self.settings.dark_mode else WHITE
            text_color = WHITE if self.settings.dark_mode else BLACK
            self.display.fill(bg_color)
            
            # Title
            title = self.title_font.render("SNAKE GAME", True, GREEN)
            self.display.blit(title, [DISPLAY_WIDTH // 2 - title.get_width() // 2, 50])
            
            # Menu options
            for i, option in enumerate(menu_options):
                color = GREEN if i == selected_option else text_color
                option_text = self.font_style.render(option, True, color)
                self.display.blit(option_text, 
                                 [DISPLAY_WIDTH // 2 - option_text.get_width() // 2, 
                                  200 + i * 50])
            
            # Display high score
            high_score_text = self.font_style.render(f"High Score: {self.high_score}", True, text_color)
            self.display.blit(high_score_text, 
                             [DISPLAY_WIDTH // 2 - high_score_text.get_width() // 2, 
                              DISPLAY_HEIGHT - 100])
                              
            # Update display
            pygame.display.update()
            self.clock.tick(15)
        
    def game_over_screen(self):
        """Display game over screen"""
        bg_color = (20, 20, 20) if self.settings.dark_mode else WHITE
        text_color = WHITE if self.settings.dark_mode else BLACK
        
        game_over_menu = True
        
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            new_high_score = True
        else:
            new_high_score = False
            
        while game_over_menu:
            self.display.fill(bg_color)
            
            # Game over message
            game_over_text = self.title_font.render("GAME OVER", True, RED)
            self.display.blit(game_over_text, 
                             [DISPLAY_WIDTH // 2 - game_over_text.get_width() // 2, 100])
            
            # Final score
            score_text = self.score_font.render(f"Final Score: {self.score}", True, text_color)
            self.display.blit(score_text, 
                             [DISPLAY_WIDTH // 2 - score_text.get_width() // 2, 200])
            
            # High score message
            if new_high_score:
                new_high_text = self.score_font.render("NEW HIGH SCORE!", True, GOLD)
                self.display.blit(new_high_text, 
                                 [DISPLAY_WIDTH // 2 - new_high_text.get_width() // 2, 250])
            
            # Options
            restart_text = self.font_style.render("Press ENTER to Play Again", True, GREEN)
            self.display.blit(restart_text, 
                             [DISPLAY_WIDTH // 2 - restart_text.get_width() // 2, 350])
            
            menu_text = self.font_style.render("Press M for Menu", True, BLUE)
            self.display.blit(menu_text, 
                             [DISPLAY_WIDTH // 2 - menu_text.get_width() // 2, 400])
            
            quit_text = self.font_style.render("Press Q to Quit", True, RED)
            self.display.blit(quit_text, 
                             [DISPLAY_WIDTH // 2 - quit_text.get_width() // 2, 450])
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        self.reset_game()
                        return True  # Return to game loop
                    elif event.key == pygame.K_m:
                        self.reset_game()
                        self.show_menu()
                        return True  # Return to game loop
            
            self.clock.tick(15)
        
    def reset_game(self):
        """Reset the game state"""
        self.snake = Snake(GRID_SIZE)
        self.food = Food(GRID_SIZE)
        self.score = 0
        self.game_over = False
        self.active_effects = {}
        self.snake_speed_modifier = 0
        
    def handle_food_collision(self):
        """Handle snake collision with food"""
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            food_type = self.food.type
            
            # Add points based on food type
            points = FOODS[food_type].points
            self.score += points
            
            # Grow the snake
            if points > 0:
                self.snake.grow(points)
            elif food_type == "shrink":
                self.snake.grow(-3)  # Shrink by 3 segments
            
            # Apply special food effects
            if food_type == "speed_up":
                self.snake_speed_modifier = 5  # Speed up temporarily
                self.active_effects["speed_up"] = pygame.time.get_ticks() + 5000  # 5 seconds
            elif food_type == "slow_down":
                self.snake_speed_modifier = -5  # Slow down temporarily
                self.active_effects["slow_down"] = pygame.time.get_ticks() + 5000  # 5 seconds
            
            # Generate new food
            self.food.respawn()
            
            return True
        return False
    
    def update_effects(self):
        """Update active effects"""
        current_time = pygame.time.get_ticks()
        
        # Check for expired effects
        expired_effects = []
        for effect, expiry_time in self.active_effects.items():
            if current_time >= expiry_time:
                expired_effects.append(effect)
                
        # Remove expired effects
        for effect in expired_effects:
            del self.active_effects[effect]
            if effect in ["speed_up", "slow_down"]:
                self.snake_speed_modifier = 0
    
    def game_loop(self):
        """Main game loop"""
        # Show menu first
        self.show_menu()
        
        # Reset game state
        self.reset_game()
        
        direction_set = False  # Flag to prevent multiple direction changes per frame
        
        while not self.game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    direction_set = True
                    if event.key == pygame.K_LEFT and self.snake.dx != GRID_SIZE:
                        self.snake.dx = -GRID_SIZE
                        self.snake.dy = 0
                    elif event.key == pygame.K_RIGHT and self.snake.dx != -GRID_SIZE:
                        self.snake.dx = GRID_SIZE
                        self.snake.dy = 0
                    elif event.key == pygame.K_UP and self.snake.dy != GRID_SIZE:
                        self.snake.dy = -GRID_SIZE
                        self.snake.dx = 0
                    elif event.key == pygame.K_DOWN and self.snake.dy != -GRID_SIZE:
                        self.snake.dy = GRID_SIZE
                        self.snake.dx = 0
                    elif event.key == pygame.K_p:  # Pause game
                        self.game_paused = not self.game_paused
                    direction_set = False  # Allow new direction change
            
            # Skip updates if game is paused
            if self.game_paused:
                # Display pause message
                bg_color = (20, 20, 20) if self.settings.dark_mode else WHITE
                self.display.fill(bg_color)
                pause_text = self.title_font.render("PAUSED", True, BLUE)
                self.display.blit(pause_text, 
                                 [DISPLAY_WIDTH // 2 - pause_text.get_width() // 2, 
                                  DISPLAY_HEIGHT // 2 - pause_text.get_height() // 2])
                pygame.display.update()
                
                # Check for pause toggle
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.game_paused = False
                
                self.clock.tick(15)
                continue
            
            # Update snake position
            self.snake.update()
            
            # Check collisions with walls
            if self.settings.walls_enabled:
                if self.snake.check_collision_with_walls():
                    self.game_over_screen()
                    continue
            else:
                self.snake.check_collision_with_walls(wrap_around=True)
            
            # Check collision with self
            if self.snake.check_collision_with_self():
                self.game_over_screen()
                continue
            
            # Handle food collision
            self.handle_food_collision()
            
            # Update effects
            self.update_effects()
            
            # Draw game elements
            bg_color = (20, 20, 20) if self.settings.dark_mode else WHITE
            self.display.fill(bg_color)
            
            # Draw grid if not in dark mode
            if not self.settings.dark_mode:
                self.draw_grid()
            
            # Draw food and snake
            self.food.draw(self.display, self.settings.dark_mode)
            self.snake.draw(self.display, self.settings.dark_mode)
            
            # Show score
            self.show_score()
            
            # Show active effects
            text_color = WHITE if self.settings.dark_mode else BLACK
            effect_y = 50
            for effect in self.active_effects:
                effect_text = self.font_style.render(f"{effect.replace('_', ' ').title()} Active", True, BLUE)
                self.display.blit(effect_text, [10, effect_y])
                effect_y += 30
            
            # Update display
            pygame.display.update()
            
            # Adjust game speed with modifiers
            adjusted_speed = self.settings.snake_speed + self.snake_speed_modifier
            if adjusted_speed < 5:  # Minimum speed
                adjusted_speed = 5
            self.clock.tick(adjusted_speed)

# Start the game
if __name__ == "__main__":
    game = Game()
    game.game_loop()
