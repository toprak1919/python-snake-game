import pygame
import time
import random
import sys
import os
import math
import json
from pygame import mixer

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
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (150, 150, 150)

# Set display dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
GRID_SIZE = 20

# Sound effects paths (create sounds directory)
SOUNDS_DIR = "C:\\Users\\toprak\\Desktop\\command-and-claude\\claudeworkspace\\snake_game\\sounds"
os.makedirs(SOUNDS_DIR, exist_ok=True)

# Create empty sound files
def create_dummy_sound_files():
    sound_files = {
        "eat.wav": b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"V\x00\x00"V\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00',
        "game_over.wav": b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"V\x00\x00"V\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00',
        "powerup.wav": b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"V\x00\x00"V\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00',
        "menu_select.wav": b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"V\x00\x00"V\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00',
    }
    
    for filename, content in sound_files.items():
        filepath = os.path.join(SOUNDS_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'wb') as f:
                f.write(content)

create_dummy_sound_files()

# Load sounds
try:
    eat_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "eat.wav"))
    game_over_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "game_over.wav"))
    powerup_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "powerup.wav"))
    menu_select_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "menu_select.wav"))
except:
    # Create dummy sound object if loading fails
    class DummySound:
        def play(self): pass
    eat_sound = DummySound()
    game_over_sound = DummySound()
    powerup_sound = DummySound()
    menu_select_sound = DummySound()

# Game settings
class GameSettings:
    def __init__(self):
        self.difficulty = "medium"     # "easy", "medium", "hard"
        self.snake_speed = 15
        self.walls_enabled = False
        self.special_foods = True
        self.dark_mode = False
        self.sound_enabled = True
        self.particles_enabled = True
        self.background_style = "grid" # "grid", "none", "gradient"
        self.snake_style = "classic"   # "classic", "gradient", "patterned"
        self.food_style = "animated"   # "simple", "animated", "realistic"
        self.control_scheme = "arrow"  # "arrow", "wasd"
        
    def update_speed(self):
        if self.difficulty == "easy":
            self.snake_speed = 10
        elif self.difficulty == "medium":
            self.snake_speed = 15
        elif self.difficulty == "hard":
            self.snake_speed = 25
            
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        
    def toggle_particles(self):
        self.particles_enabled = not self.particles_enabled
    
    def cycle_background(self):
        styles = ["grid", "none", "gradient"]
        current_index = styles.index(self.background_style)
        self.background_style = styles[(current_index + 1) % len(styles)]
        
    def cycle_snake_style(self):
        styles = ["classic", "gradient", "patterned"]
        current_index = styles.index(self.snake_style)
        self.snake_style = styles[(current_index + 1) % len(styles)]
        
    def cycle_food_style(self):
        styles = ["simple", "animated", "realistic"]
        current_index = styles.index(self.food_style)
        self.food_style = styles[(current_index + 1) % len(styles)]
        
    def toggle_control_scheme(self):
        if self.control_scheme == "arrow":
            self.control_scheme = "wasd"
        else:
            self.control_scheme = "arrow"

# Particle system for visual effects
class Particle:
    def __init__(self, x, y, color, velocity=None, size=None, life=None):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity or [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.size = size or random.randint(2, 5)
        self.life = life or random.randint(20, 40)
        self.original_life = self.life
        
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.life -= 1
        # Gradually reduce size as life decreases
        self.size = max(1, self.size * (self.life / self.original_life))
        return self.life <= 0
        
    def draw(self, display):
        # Fade out color as life decreases
        alpha = int(255 * (self.life / self.original_life))
        color = (self.color[0], self.color[1], self.color[2])
        pygame.draw.circle(display, color, (int(self.x), int(self.y)), int(self.size))


# Food types and their properties
class FoodType:
    def __init__(self, color, points, duration=None, effect=None, particle_color=None, sound=None):
        self.color = color
        self.points = points
        self.duration = duration  # For temporary effects in milliseconds
        self.effect = effect      # Function to call when eaten
        self.particle_color = particle_color or color
        self.sound = sound
        
    def create_particles(self, x, y, count=20):
        particles = []
        for _ in range(count):
            particles.append(Particle(
                x + GRID_SIZE/2,
                y + GRID_SIZE/2,
                self.particle_color
            ))
        return particles

# Define food types
FOODS = {
    "regular": FoodType(RED, 1, particle_color=RED, sound=eat_sound),
    "bonus": FoodType(GOLD, 3, particle_color=GOLD, sound=eat_sound),
    "speed_up": FoodType(BLUE, 1, duration=5000, particle_color=BLUE, sound=powerup_sound),
    "slow_down": FoodType(PURPLE, 1, duration=5000, particle_color=PURPLE, sound=powerup_sound),
    "shrink": FoodType(YELLOW, -3, particle_color=YELLOW, sound=powerup_sound),  # Reduces length by 3 (min length is 1)
    "ghost": FoodType(CYAN, 1, duration=7000, particle_color=CYAN, sound=powerup_sound),  # Pass through walls and self
    "double_score": FoodType(ORANGE, 1, duration=10000, particle_color=ORANGE, sound=powerup_sound),  # Double points for duration
    "rainbow": FoodType(MAGENTA, 5, particle_color=MAGENTA, sound=powerup_sound),  # Rainbow snake effect
    "freeze": FoodType(GRAY, 0, duration=3000, particle_color=GRAY, sound=powerup_sound),  # Stops snake movement temporarily
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
        # Visual customization
        self.color_scheme = [(0, 255, 0), (0, 220, 0), (0, 190, 0)]
        self.pattern = "solid"  # solid, gradient, striped, rainbow
        self.rainbow_offset = 0  # Used for rainbow pattern
        # Gameplay effects
        self.ghost_mode = False
        self.double_score = False
        self.frozen = False
        self.direction_queue = []  # Queue for input during frozen state
        
    def update(self):
        # Don't move if frozen
        if self.frozen:
            # Keep the head in the body list
            if len(self.body) > 0 and self.body[-1] != self.head:
                self.body.append(self.head)
                if len(self.body) > self.length:
                    del self.body[0]
            return
            
        # Move snake
        self.x += self.dx
        self.y += self.dy
        
        # Update head position
        self.head = [self.x, self.y]
        self.body.append(self.head)
        
        # Remove tail if snake is longer than it should be
        if len(self.body) > self.length:
            del self.body[0]
            
        # Update rainbow pattern
        if self.pattern == "rainbow":
            self.rainbow_offset = (self.rainbow_offset + 0.05) % 1.0
            
    def grow(self, amount=1):
        """Increase snake length"""
        self.length += amount
        if self.length < 1:  # Minimum length
            self.length = 1
            
    def set_effect(self, effect_name, active=True, duration=None):
        """Set a gameplay effect"""
        if effect_name == "ghost":
            self.ghost_mode = active
        elif effect_name == "double_score":
            self.double_score = active
        elif effect_name == "freeze":
            self.frozen = active
            if not active and self.direction_queue:
                # Apply the last queued direction when unfreezing
                last_dir = self.direction_queue[-1]
                self.dx, self.dy = last_dir
                self.direction_queue = []
        elif effect_name == "rainbow":
            self.pattern = "rainbow" if active else "solid"
            
    def queue_direction(self, dx, dy):
        """Queue a direction change for when the snake unfreezes"""
        if self.frozen:
            self.direction_queue.append((dx, dy))
            return True
        return False
            
    def check_collision_with_self(self):
        """Check if snake head collides with its body"""
        if self.ghost_mode:
            return False
            
        for segment in self.body[:-1]:  # All segments except head
            if segment == self.head:
                return True
        return False
    
    def check_collision_with_walls(self, wrap_around=False):
        """Check if snake hits the walls"""
        if wrap_around or self.ghost_mode:
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
        
    def get_segment_color(self, i, total, dark_mode=False):
        """Get color for a specific segment based on pattern"""
        is_head = (i == total - 1)
        
        if self.pattern == "solid":
            if is_head:
                return (0, 200, 0) if not dark_mode else (0, 150, 0)
            else:
                return GREEN if not dark_mode else DARK_GREEN
                
        elif self.pattern == "gradient":
            # Gradient from tail to head
            progress = i / max(1, total - 1)
            if dark_mode:
                r = int(0)
                g = int(50 + 100 * progress)
                b = int(0)
            else:
                r = int(0)
                g = int(150 + 105 * progress)
                b = int(0)
            return (r, g, b)
            
        elif self.pattern == "striped":
            if i % 2 == 0:
                return GREEN if not dark_mode else DARK_GREEN
            else:
                return (150, 255, 150) if not dark_mode else (0, 100, 50)
                
        elif self.pattern == "rainbow":
            # Rainbow pattern
            hue = (i / max(1, total - 1) + self.rainbow_offset) % 1.0
            r, g, b = hsv_to_rgb(hue, 1.0, 1.0 if not dark_mode else 0.7)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        return GREEN if not dark_mode else DARK_GREEN
        
    def draw(self, display, dark_mode=False, style="classic"):
        """Draw the snake on screen"""
        # Ghost mode effect - semi-transparent
        ghost_alpha = 128 if self.ghost_mode else 255
        
        for i, segment in enumerate(self.body):
            color = self.get_segment_color(i, len(self.body), dark_mode)
            
            # Different drawing styles
            if style == "classic":
                pygame.draw.rect(display, color, 
                    [segment[0], segment[1], self.block_size, self.block_size])
                    
            elif style == "rounded":
                # Rounded segments
                pygame.draw.circle(display, color, 
                    (segment[0] + self.block_size//2, segment[1] + self.block_size//2), 
                    self.block_size//2)
                    
            elif style == "gradient":
                # Draw with gradient
                pygame.draw.rect(display, color, 
                    [segment[0], segment[1], self.block_size, self.block_size])
                    
            elif style == "patterned":
                # Patterned segments (checkerboard within each segment)
                pygame.draw.rect(display, color, 
                    [segment[0], segment[1], self.block_size, self.block_size])
                if (i % 2) == 0:
                    inner_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
                    pygame.draw.rect(display, inner_color, 
                        [segment[0] + 4, segment[1] + 4, self.block_size - 8, self.block_size - 8])
            
        # Draw eyes on snake head (only if we have a head)
        if self.body:
            head = self.body[-1]
            eye_color = BLACK if not dark_mode else WHITE
            
            # Add direction-aware eyes
            eye_offset_x = 0
            eye_offset_y = 0
            
            if self.dx > 0:  # Moving right
                eye_offset_x = 2
                eye_offset_y = -3
            elif self.dx < 0:  # Moving left
                eye_offset_x = -2
                eye_offset_y = -3
            elif self.dy > 0:  # Moving down
                eye_offset_y = 2
            elif self.dy < 0:  # Moving up
                eye_offset_y = -2
                
            # Left eye
            pygame.draw.circle(display, eye_color, 
                               (head[0] + 5 + eye_offset_x, head[1] + 5 + eye_offset_y), 3)
            # Right eye
            pygame.draw.circle(display, eye_color, 
                               (head[0] + self.block_size - 5 + eye_offset_x, head[1] + 5 + eye_offset_y), 3)

# Helper function for rainbow color calculations
def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB"""
    if s == 0.0:
        return v, v, v
        
    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    
    i %= 6
    
    if i == 0:
        return v, t, p
    elif i == 1:
        return q, v, p
    elif i == 2:
        return p, v, t
    elif i == 3:
        return p, q, v
    elif i == 4:
        return t, p, v
    else:
        return v, p, q

class Food:
    def __init__(self, block_size):
        self.block_size = block_size
        self.type = "regular"
        self.respawn()
        self.special_food_timer = 0
        self.animation_timer = 0
        self.pulse_size = 0
        self.pulse_growing = True
        self.rotation_angle = 0
        self.hover_offset = 0
        self.hover_direction = 1
        self.sparkle_timer = 0
        self.sparkle_particles = []
        self.lifespan = random.randint(15000, 25000)  # Food disappears after 15-25 seconds
        self.spawn_time = pygame.time.get_ticks()
        
    def respawn(self):
        """Place food at random location"""
        self.x = round(random.randrange(0, DISPLAY_WIDTH - self.block_size) / 
                      self.block_size) * self.block_size
        self.y = round(random.randrange(0, DISPLAY_HEIGHT - self.block_size) / 
                      self.block_size) * self.block_size
        
        # Randomly choose a food type if special foods are enabled
        if GameSettings().special_foods:
            # Regular food: 60%, Special food: 40%
            if random.random() < 0.4:
                # Choose from special food types (exclude regular)
                food_types = list(FOODS.keys())
                food_types.remove("regular")
                self.type = random.choice(food_types)
            else:
                self.type = "regular"
        else:
            self.type = "regular"
            
        # Reset animation variables
        self.animation_timer = 0
        self.pulse_size = 0
        self.pulse_growing = True
        self.rotation_angle = 0
        self.hover_offset = 0
        self.hover_direction = 1
        self.sparkle_timer = 0
        self.sparkle_particles = []
        self.spawn_time = pygame.time.get_ticks()
        
    def update(self, current_time):
        """Update food animations"""
        # Check if food should disappear (except regular food)
        if self.type != "regular" and current_time - self.spawn_time > self.lifespan:
            self.respawn()
            return
        
        # Update animation timer
        self.animation_timer += 1
        
        # Pulse animation
        if self.pulse_growing:
            self.pulse_size += 0.1
            if self.pulse_size >= 3:
                self.pulse_growing = False
        else:
            self.pulse_size -= 0.1
            if self.pulse_size <= 0:
                self.pulse_growing = True
        
        # Rotation animation (for some food types)
        self.rotation_angle = (self.rotation_angle + 1) % 360
        
        # Hover animation
        self.hover_offset += 0.1 * self.hover_direction
        if abs(self.hover_offset) > 3:
            self.hover_direction *= -1
            
        # Sparkle effect for special foods
        if self.type != "regular" and random.random() < 0.1:  # 10% chance per update
            self.sparkle_particles.append({
                "x": self.x + random.randint(0, self.block_size),
                "y": self.y + random.randint(0, self.block_size),
                "size": random.uniform(1, 3),
                "life": random.randint(10, 30)
            })
            
        # Update sparkle particles
        for particle in self.sparkle_particles[:]:
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.sparkle_particles.remove(particle)
            
    def draw(self, display, dark_mode=False, style="animated"):
        """Draw the food on screen"""
        food_color = FOODS[self.type].color
        center_x = self.x + self.block_size//2
        center_y = self.y + self.block_size//2 + self.hover_offset
        
        if style == "simple":
            # Simple rendering without animations
            if self.type == "regular":
                pygame.draw.rect(display, food_color, 
                                [self.x, self.y, self.block_size, self.block_size])
            else:
                pygame.draw.circle(display, food_color,
                                  (center_x, center_y),
                                   self.block_size//2)
                                   
        elif style == "animated":
            # Animated food rendering
            if self.type == "regular":
                # Basic apple shape
                pygame.draw.circle(display, RED,
                                  (center_x, center_y),
                                   self.block_size//2 + self.pulse_size)
                # Stem
                pygame.draw.rect(display, (139, 69, 19),  # Brown
                                [center_x - 1, center_y - self.block_size//2 - 2,
                                 3, 5])
                # Leaf
                pygame.draw.ellipse(display, GREEN,
                                   [center_x + 2, center_y - self.block_size//2,
                                    5, 3])
                    
            elif self.type == "bonus":
                # Gold star
                radius = self.block_size//2 + self.pulse_size
                points = []
                for i in range(5):
                    # Outer points (star tips)
                    angle = self.rotation_angle + i * 72
                    x = center_x + int(radius * math.cos(math.radians(angle)))
                    y = center_y + int(radius * math.sin(math.radians(angle)))
                    points.append((x, y))
                    
                    # Inner points
                    angle = self.rotation_angle + i * 72 + 36
                    x = center_x + int(radius//2 * math.cos(math.radians(angle)))
                    y = center_y + int(radius//2 * math.sin(math.radians(angle)))
                    points.append((x, y))
                    
                pygame.draw.polygon(display, GOLD, points)
                
            elif self.type == "speed_up":
                # Lightning bolt
                pygame.draw.circle(display, BLUE,
                                  (center_x, center_y),
                                   self.block_size//2 + self.pulse_size)
                # Lightning symbol
                points = [
                    (center_x - 4, center_y - 6),
                    (center_x + 2, center_y - 2),
                    (center_x - 2, center_y + 2),
                    (center_x + 4, center_y + 6)
                ]
                pygame.draw.lines(display, YELLOW, False, points, 2)
                
            elif self.type == "slow_down":
                # Slow symbol (clock)
                pygame.draw.circle(display, PURPLE,
                                  (center_x, center_y),
                                   self.block_size//2 + self.pulse_size)
                # Clock face
                pygame.draw.circle(display, WHITE,
                                  (center_x, center_y),
                                   self.block_size//3)
                # Clock hands
                hand_angle = math.radians(self.rotation_angle)
                # Hour hand
                hour_x = center_x + int((self.block_size//5) * math.cos(hand_angle))
                hour_y = center_y + int((self.block_size//5) * math.sin(hand_angle))
                pygame.draw.line(display, BLACK, (center_x, center_y), (hour_x, hour_y), 2)
                # Minute hand
                min_angle = math.radians(self.rotation_angle * 2)
                min_x = center_x + int((self.block_size//4) * math.cos(min_angle))
                min_y = center_y + int((self.block_size//4) * math.sin(min_angle))
                pygame.draw.line(display, BLACK, (center_x, center_y), (min_x, min_y), 1)
                
            elif self.type == "shrink":
                # Shrink symbol
                pygame.draw.circle(display, YELLOW,
                                  (center_x, center_y),
                                   self.block_size//2 + self.pulse_size)
                # Arrows pointing inward
                arrow_size = 6 + int(self.pulse_size)
                # Left arrow
                pygame.draw.line(display, BLACK, 
                                (center_x - arrow_size, center_y),
                                (center_x - 2, center_y), 2)
                pygame.draw.polygon(display, BLACK, [
                    (center_x - 2, center_y - 3),
                    (center_x - 2, center_y + 3),
                    (center_x + 2, center_y)
                ])
                # Right arrow
                pygame.draw.line(display, BLACK, 
                                (center_x + arrow_size, center_y),
                                (center_x + 2, center_y), 2)
                pygame.draw.polygon(display, BLACK, [
                    (center_x + 2, center_y - 3),
                    (center_x + 2, center_y + 3),
                    (center_x - 2, center_y)
                ])
                
            elif self.type == "ghost":
                # Ghost mode food (transparent look)
                pygame.draw.circle(display, CYAN,
                                  (center_x, center_y),
                                   self.block_size//2 + self.pulse_size)
                # Ghost icon
                ghost_points = []
                for i in range(8):
                    angle = self.rotation_angle + i * 45
                    rad = self.block_size//3
                    if i % 2 == 1:  # Make every other point wavier
                        rad += self.pulse_size * 1.5
                    x = center_x + int(rad * math.cos(math.radians(angle)))
                    y = center_y + int(rad * math.sin(math.radians(angle)))
                    ghost_points.append((x, y))
                pygame.draw.polygon(display, WHITE, ghost_points)
                # Eyes
                eye_offset = 3
                pygame.draw.circle(display, BLACK, (center_x - eye_offset, center_y - 1), 2)
                pygame.draw.circle(display, BLACK, (center_x + eye_offset, center_y - 1), 2)
                
            elif self.type == "double_score":
                # Double score symbol
                pygame.draw.circle(display, ORANGE,
                                  (center_x, center_y),
                                   self.block_size//2 + self.pulse_size)
                # "2x" text
                font = pygame.font.SysFont("Arial", 12, bold=True)
                text = font.render("2x", True, WHITE)
                text_rect = text.get_rect(center=(center_x, center_y))
                display.blit(text, text_rect)
                
            elif self.type == "rainbow":
                # Rainbow food
                rainbow_colors = [
                    (255, 0, 0),    # Red
                    (255, 127, 0),  # Orange
                    (255, 255, 0),  # Yellow
                    (0, 255, 0),    # Green
                    (0, 0, 255),    # Blue
                    (75, 0, 130),   # Indigo
                    (143, 0, 255)   # Violet
                ]
                
                for i, color in enumerate(rainbow_colors):
                    size = self.block_size//2 - i * 2 + self.pulse_size
                    if size > 0:
                        pygame.draw.circle(display, color, (center_x, center_y), size)
                
            elif self.type == "freeze":
                # Freeze symbol (snowflake)
                pygame.draw.circle(display, CYAN,
                                  (center_x, center_y),
                                   self.block_size//2 + self.pulse_size)
                # Snowflake
                for i in range(6):
                    angle = self.rotation_angle + i * 60
                    rad = self.block_size//2 - 2
                    end_x = center_x + int(rad * math.cos(math.radians(angle)))
                    end_y = center_y + int(rad * math.sin(math.radians(angle)))
                    pygame.draw.line(display, WHITE, (center_x, center_y), (end_x, end_y), 2)
                    
                    # Add small perpendicular lines
                    mid_x = center_x + int(rad*0.6 * math.cos(math.radians(angle)))
                    mid_y = center_y + int(rad*0.6 * math.sin(math.radians(angle)))
                    perp_angle1 = angle + 60
                    perp_angle2 = angle - 60
                    perp_len = rad * 0.2
                    
                    px1 = mid_x + int(perp_len * math.cos(math.radians(perp_angle1)))
                    py1 = mid_y + int(perp_len * math.sin(math.radians(perp_angle1)))
                    pygame.draw.line(display, WHITE, (mid_x, mid_y), (px1, py1), 1)
                    
                    px2 = mid_x + int(perp_len * math.cos(math.radians(perp_angle2)))
                    py2 = mid_y + int(perp_len * math.sin(math.radians(perp_angle2)))
                    pygame.draw.line(display, WHITE, (mid_x, mid_y), (px2, py2), 1)
        
        elif style == "realistic":
            # More detailed and realistic food renderings
            if self.type == "regular":
                # Apple with shading
                pygame.draw.circle(display, (200, 0, 0), # Dark red
                                  (center_x, center_y),
                                   self.block_size//2 + self.pulse_size)
                # Highlight
                highlight_x = center_x - self.block_size//6
                highlight_y = center_y - self.block_size//6
                pygame.draw.circle(display, (255, 50, 50), # Light red
                                  (highlight_x, highlight_y),
                                   self.block_size//6)
                # Stem
                pygame.draw.rect(display, (100, 50, 0),  # Dark brown
                                [center_x - 1, center_y - self.block_size//2 - 2,
                                 3, 5])
                # Leaf
                leaf_points = [
                    (center_x + 2, center_y - self.block_size//2),
                    (center_x + 7, center_y - self.block_size//2 - 2),
                    (center_x + 5, center_y - self.block_size//2 + 3)
                ]
                pygame.draw.polygon(display, (0, 150, 0), leaf_points)  # Dark green
            else:
                # For other food types, use the animated style
                self.draw(display, dark_mode, "animated")
                
        # Draw sparkle particles for special foods
        for particle in self.sparkle_particles:
            alpha = int(255 * (particle["life"] / 30))  # Fade out
            size = particle["size"] * (particle["life"] / 15)
            color = GOLD if self.type == "bonus" else FOODS[self.type].color
            pygame.draw.circle(display, color,
                              (int(particle["x"]), int(particle["y"])),
                               int(size))

class Game:
    def __init__(self):
        # Set up the game display
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Ultimate Snake Game')
        
        # Set game clock
        self.clock = pygame.time.Clock()
        
        # Set fonts
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.title_font = pygame.font.SysFont("comicsansms", 50)
        self.small_font = pygame.font.SysFont("bahnschrift", 15)
        
        # Game objects
        self.settings = GameSettings()
        self.snake = Snake(GRID_SIZE)
        self.food = Food(GRID_SIZE)
        
        # Game state
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.game_paused = False
        self.level = 1
        self.score_to_next_level = 10
        self.game_time = 0  # Seconds since game started
        
        # Power-ups and effects
        self.active_effects = {}  # {effect_name: expiry_time}
        self.snake_speed_modifier = 0
        self.particles = []
        
        # Statistics
        self.stats = {
            "apples_eaten": 0,
            "special_foods_eaten": 0,
            "power_ups_used": 0,
            "distance_traveled": 0,
            "longest_snake": 1,
            "games_played": 0,
            "highest_level": 1,
            "play_time": 0  # In seconds
        }
        self.load_stats()
        
    def load_high_score(self):
        """Load high score from file"""
        score_file = os.path.join("C:\\Users\\toprak\\Desktop\\command-and-claude\\claudeworkspace\\snake_game", "high_score.txt")
        try:
            with open(score_file, "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0
            
    def save_high_score(self):
        """Save high score to file"""
        score_file = os.path.join("C:\\Users\\toprak\\Desktop\\command-and-claude\\claudeworkspace\\snake_game", "high_score.txt")
        with open(score_file, "w") as f:
            f.write(str(self.high_score))
            
    def load_stats(self):
        """Load game statistics from file"""
        stats_file = os.path.join("C:\\Users\\toprak\\Desktop\\command-and-claude\\claudeworkspace\\snake_game", "stats.json")
        try:
            with open(stats_file, "r") as f:
                loaded_stats = json.loads(f.read())
                for key, value in loaded_stats.items():
                    if key in self.stats:
                        self.stats[key] = value
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is corrupted, keep default stats
            pass
            
    def save_stats(self):
        """Save game statistics to file"""
        stats_file = os.path.join("C:\\Users\\toprak\\Desktop\\command-and-claude\\claudeworkspace\\snake_game", "stats.json")
        with open(stats_file, "w") as f:
            f.write(json.dumps(self.stats))
            
    def update_stats(self, game_over=False):
        """Update game statistics"""
        # Update longest snake stat
        if self.snake.length > self.stats["longest_snake"]:
            self.stats["longest_snake"] = self.snake.length
            
        # Update highest level
        if self.level > self.stats["highest_level"]:
            self.stats["highest_level"] = self.level
            
        # If game is over, update game-level stats
        if game_over:
            self.stats["games_played"] += 1
            self.stats["play_time"] += self.game_time
            self.save_stats()
    
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
        """Display game menu with multiple pages"""
        menu_open = True
        current_page = "main"  # main, gameplay, visuals, controls, stats
        selected_option = 0
        
        # Menu structure with multiple pages
        menu_pages = {
            "main": ["Start Game", "Gameplay Settings", "Visual Settings", "Controls", "Statistics", "Quit"],
            "gameplay": ["Difficulty: " + self.settings.difficulty, 
                         "Walls: " + ("On" if self.settings.walls_enabled else "Off"),
                         "Special Foods: " + ("On" if self.settings.special_foods else "Off"),
                         "Sound: " + ("On" if self.settings.sound_enabled else "Off"),
                         "Back to Main Menu"],
            "visuals": ["Dark Mode: " + ("On" if self.settings.dark_mode else "Off"),
                        "Particles: " + ("On" if self.settings.particles_enabled else "Off"),
                        "Background: " + self.settings.background_style.title(),
                        "Snake Style: " + self.settings.snake_style.title(),
                        "Food Style: " + self.settings.food_style.title(),
                        "Back to Main Menu"],
            "controls": ["Control Scheme: " + self.settings.control_scheme.upper(),
                         "Back to Main Menu"],
            "stats": ["Games Played: " + str(self.stats["games_played"]),
                      "Highest Score: " + str(self.high_score),
                      "Highest Level: " + str(self.stats["highest_level"]),
                      "Longest Snake: " + str(self.stats["longest_snake"]),
                      "Apples Eaten: " + str(self.stats["apples_eaten"]),
                      "Special Foods Eaten: " + str(self.stats["special_foods_eaten"]),
                      "Power-ups Used: " + str(self.stats["power_ups_used"]),
                      "Total Play Time: " + self.format_time(self.stats["play_time"]),
                      "Reset Statistics",
                      "Back to Main Menu"]
        }
        
        # Animation elements
        snake_demo_pos = [DISPLAY_WIDTH // 2, 150]
        snake_demo_dir = [GRID_SIZE, 0]
        snake_demo_body = [[snake_demo_pos[0] - (i * GRID_SIZE), snake_demo_pos[1]] for i in range(5)]
        snake_demo_timer = 0
        food_demo_pos = [DISPLAY_WIDTH // 2 + 100, 150]
        
        while menu_open:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.settings.sound_enabled:
                        menu_select_sound.play()
                        
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_pages[current_page])
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_pages[current_page])
                    elif event.key == pygame.K_RETURN:
                        # Handle menu selection based on current page
                        result = self.handle_menu_selection(current_page, selected_option, menu_pages)
                        
                        # Check if we should exit the menu
                        if result is False:
                            menu_open = False
                            continue
                            
                        # Update current page and selected option
                        if isinstance(result, tuple) and len(result) == 2:
                            current_page, selected_option = result
                        
                        # Update menu options after selection
                        if current_page == "gameplay":
                            menu_pages["gameplay"] = [
                                "Difficulty: " + self.settings.difficulty, 
                                "Walls: " + ("On" if self.settings.walls_enabled else "Off"),
                                "Special Foods: " + ("On" if self.settings.special_foods else "Off"),
                                "Sound: " + ("On" if self.settings.sound_enabled else "Off"),
                                "Back to Main Menu"
                            ]
                        elif current_page == "visuals":
                            menu_pages["visuals"] = [
                                "Dark Mode: " + ("On" if self.settings.dark_mode else "Off"),
                                "Particles: " + ("On" if self.settings.particles_enabled else "Off"),
                                "Background: " + self.settings.background_style.title(),
                                "Snake Style: " + self.settings.snake_style.title(),
                                "Food Style: " + self.settings.food_style.title(),
                                "Back to Main Menu"
                            ]
                        elif current_page == "controls":
                            menu_pages["controls"] = [
                                "Control Scheme: " + self.settings.control_scheme.upper(),
                                "Back to Main Menu"
                            ]
                        elif current_page == "stats":
                            menu_pages["stats"] = [
                                "Games Played: " + str(self.stats["games_played"]),
                                "Highest Score: " + str(self.high_score),
                                "Highest Level: " + str(self.stats["highest_level"]),
                                "Longest Snake: " + str(self.stats["longest_snake"]),
                                "Apples Eaten: " + str(self.stats["apples_eaten"]),
                                "Special Foods Eaten: " + str(self.stats["special_foods_eaten"]),
                                "Power-ups Used: " + str(self.stats["power_ups_used"]),
                                "Total Play Time: " + self.format_time(self.stats["play_time"]),
                                "Reset Statistics",
                                "Back to Main Menu"
                            ]
            
            # Draw menu background
            bg_color = (20, 20, 20) if self.settings.dark_mode else WHITE
            text_color = WHITE if self.settings.dark_mode else BLACK
            self.display.fill(bg_color)
            
            # Update and draw animated elements
            self.update_menu_animations(snake_demo_pos, snake_demo_dir, snake_demo_body, 
                                      snake_demo_timer, food_demo_pos, current_page == "main")
            
            # Draw page-specific content
            if current_page == "main":
                self.draw_main_menu(menu_pages[current_page], selected_option, text_color)
            elif current_page == "stats":
                self.draw_stats_menu(menu_pages[current_page], selected_option, text_color)
            else:
                self.draw_settings_menu(menu_pages[current_page], selected_option, text_color, current_page)
            
            # Draw page navigation help
            help_text = self.small_font.render("Use UP/DOWN arrows to navigate, ENTER to select", True, text_color)
            self.display.blit(help_text, 
                            [DISPLAY_WIDTH // 2 - help_text.get_width() // 2, 
                            DISPLAY_HEIGHT - 40])
                            
            # Update display
            pygame.display.update()
            self.clock.tick(15)
            
    def handle_menu_selection(self, current_page, selected_option, menu_pages):
        """Handle menu selection based on current page"""
        # Return the updated current_page and selected_option
        new_page = current_page
        new_option = selected_option
        
        if current_page == "main":
            if selected_option == 0:  # Start Game
                return False, 0  # Close menu and start game
            elif selected_option == 1:  # Gameplay Settings
                new_page = "gameplay"
                new_option = 0
            elif selected_option == 2:  # Visual Settings
                new_page = "visuals"
                new_option = 0
            elif selected_option == 3:  # Controls
                new_page = "controls"
                new_option = 0
            elif selected_option == 4:  # Statistics
                new_page = "stats"
                new_option = 0
            elif selected_option == 5:  # Quit
                pygame.quit()
                sys.exit()
        elif current_page == "gameplay":
            if selected_option == 0:  # Difficulty
                if self.settings.difficulty == "easy":
                    self.settings.difficulty = "medium"
                elif self.settings.difficulty == "medium":
                    self.settings.difficulty = "hard"
                else:
                    self.settings.difficulty = "easy"
                self.settings.update_speed()
            elif selected_option == 1:  # Walls
                self.settings.walls_enabled = not self.settings.walls_enabled
            elif selected_option == 2:  # Special Foods
                self.settings.special_foods = not self.settings.special_foods
            elif selected_option == 3:  # Sound
                self.settings.toggle_sound()
            elif selected_option == 4:  # Back
                new_page = "main"
                new_option = 1
                
        elif current_page == "visuals":
            if selected_option == 0:  # Dark Mode
                self.settings.dark_mode = not self.settings.dark_mode
            elif selected_option == 1:  # Particles
                self.settings.toggle_particles()
            elif selected_option == 2:  # Background
                self.settings.cycle_background()
            elif selected_option == 3:  # Snake Style
                self.settings.cycle_snake_style()
            elif selected_option == 4:  # Food Style
                self.settings.cycle_food_style()
            elif selected_option == 5:  # Back
                new_page = "main"
                new_option = 2
                
        elif current_page == "controls":
            if selected_option == 0:  # Control Scheme
                self.settings.toggle_control_scheme()
            elif selected_option == 1:  # Back
                new_page = "main"
                new_option = 3
                
        elif current_page == "stats":
            if selected_option == 8:  # Reset Statistics
                self.reset_stats()
            elif selected_option == 9:  # Back
                new_page = "main"
                new_option = 4
                
        return new_page, new_option
        
    def format_time(self, seconds):
        """Format seconds into a readable time string"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours}h {minutes}m {seconds}s"
        
    def reset_stats(self):
        """Reset game statistics"""
        # Keep games played and play time
        games_played = self.stats["games_played"]
        play_time = self.stats["play_time"]
        
        # Reset all other stats
        self.stats = {
            "apples_eaten": 0,
            "special_foods_eaten": 0,
            "power_ups_used": 0,
            "distance_traveled": 0,
            "longest_snake": 1,
            "games_played": games_played,
            "highest_level": 1,
            "play_time": play_time
        }
        self.save_stats()
        
    def update_menu_animations(self, snake_pos, snake_dir, snake_body, timer, food_pos, active=True):
        """Update and draw animated elements in the menu"""
        if not active:
            return
            
        # Update snake demo animation
        timer += 1
        if timer % 5 == 0:  # Move every 5 frames
            # Update head position
            snake_pos[0] += snake_dir[0]
            snake_pos[1] += snake_dir[1]
            
            # Check boundaries and change direction
            if snake_pos[0] >= DISPLAY_WIDTH - GRID_SIZE:
                snake_dir[0], snake_dir[1] = 0, GRID_SIZE  # Go down
            elif snake_pos[1] >= DISPLAY_HEIGHT // 2:
                snake_dir[0], snake_dir[1] = -GRID_SIZE, 0  # Go left
            elif snake_pos[0] <= DISPLAY_WIDTH // 4:
                snake_dir[0], snake_dir[1] = 0, -GRID_SIZE  # Go up
            elif snake_pos[1] <= 100:
                snake_dir[0], snake_dir[1] = GRID_SIZE, 0  # Go right
                
            # Update body
            snake_body.insert(0, list(snake_body[0]))  # Add new segment at the front (copy of current front)
            snake_body[0][0] += snake_dir[0]  # Move the new front segment
            snake_body[0][1] += snake_dir[1]
            if len(snake_body) > 5:  # Keep snake at 5 segments
                snake_body.pop()
                
        # Draw snake
        for i, segment in enumerate(snake_body):
            color = GREEN if i == 0 else DARK_GREEN  # Head is lighter green
            pygame.draw.rect(self.display, color, 
                           [segment[0], segment[1], GRID_SIZE, GRID_SIZE])
                           
        # Draw food
        pygame.draw.rect(self.display, RED, 
                       [food_pos[0], food_pos[1], GRID_SIZE, GRID_SIZE])
                       
    def draw_main_menu(self, options, selected, text_color):
        """Draw the main menu page"""
        # Title
        title = self.title_font.render("SNAKE GAME", True, GREEN)
        self.display.blit(title, [DISPLAY_WIDTH // 2 - title.get_width() // 2, 50])
        
        # Menu options
        for i, option in enumerate(options):
            color = GREEN if i == selected else text_color
            option_text = self.font_style.render(option, True, color)
            self.display.blit(option_text, 
                             [DISPLAY_WIDTH // 2 - option_text.get_width() // 2, 
                              200 + i * 50])
        
        # Display high score
        high_score_text = self.font_style.render(f"High Score: {self.high_score}", True, text_color)
        self.display.blit(high_score_text, 
                         [DISPLAY_WIDTH // 2 - high_score_text.get_width() // 2, 
                          DISPLAY_HEIGHT - 100])
                          
    def draw_settings_menu(self, options, selected, text_color, page_name):
        """Draw a settings menu page"""
        # Title
        title_text = page_name.replace("_", " ").title() + " Settings"
        title = self.title_font.render(title_text, True, BLUE)
        self.display.blit(title, [DISPLAY_WIDTH // 2 - title.get_width() // 2, 50])
        
        # Menu options
        for i, option in enumerate(options):
            color = GREEN if i == selected else text_color
            option_text = self.font_style.render(option, True, color)
            self.display.blit(option_text, 
                             [DISPLAY_WIDTH // 2 - option_text.get_width() // 2, 
                              150 + i * 40])
                              
    def draw_stats_menu(self, options, selected, text_color):
        """Draw the statistics menu page"""
        # Title
        title = self.title_font.render("GAME STATISTICS", True, GOLD)
        self.display.blit(title, [DISPLAY_WIDTH // 2 - title.get_width() // 2, 50])
        
        # Stats options
        for i, option in enumerate(options):
            color = GREEN if i == selected else text_color
            # Make reset and back options stand out
            if i >= 8:  # Reset or Back option
                color = RED if i == selected else BLUE
                
            option_text = self.font_style.render(option, True, color)
            self.display.blit(option_text, 
                             [DISPLAY_WIDTH // 2 - option_text.get_width() // 2, 
                              120 + i * 35])
        
    def game_over_screen(self):
        """Display game over screen with final stats and options"""
        # Update statistics
        self.update_stats(game_over=True)
        
        bg_color = (20, 20, 20) if self.settings.dark_mode else WHITE
        text_color = WHITE if self.settings.dark_mode else BLACK
        
        game_over_menu = True
        
        # Create final stats summary
        final_stats = {
            "Score": self.score,
            "Level": self.level,
            "Snake Length": self.snake.length,
            "Time Played": self.format_time(self.game_time),
            "Foods Eaten": self.stats["apples_eaten"] + self.stats["special_foods_eaten"]
        }
        
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            new_high_score = True
        else:
            new_high_score = False
            
        # Create game over particles
        if self.settings.particles_enabled:
            self.particles = []
            for _ in range(50):
                pos_x = random.randint(0, DISPLAY_WIDTH)
                pos_y = random.randint(0, DISPLAY_HEIGHT)
                color = random.choice([RED, BLUE, GREEN, YELLOW, PURPLE])
                self.particles.append(Particle(pos_x, pos_y, color, size=random.randint(3, 8)))
            
        while game_over_menu:
            current_time = pygame.time.get_ticks()
            
            self.display.fill(bg_color)
            
            # Update and draw particles
            if self.settings.particles_enabled:
                for particle in self.particles[:]:
                    if particle.update():
                        self.particles.remove(particle)
                    else:
                        particle.draw(self.display)
            
            # Game over message with animation
            pulse = (math.sin(current_time / 300) + 1) * 10  # Pulsing size
            game_over_text = self.title_font.render("GAME OVER", True, RED)
            self.display.blit(game_over_text, 
                             [DISPLAY_WIDTH // 2 - game_over_text.get_width() // 2, 
                              80 + int(pulse)])
            
            # Final score
            score_text = self.score_font.render(f"Final Score: {self.score}", True, GOLD)
            self.display.blit(score_text, 
                             [DISPLAY_WIDTH // 2 - score_text.get_width() // 2, 180])
            
            # High score message
            if new_high_score:
                flash_color = RED if (current_time // 500) % 2 == 0 else GOLD
                new_high_text = self.score_font.render("NEW HIGH SCORE!", True, flash_color)
                self.display.blit(new_high_text, 
                                 [DISPLAY_WIDTH // 2 - new_high_text.get_width() // 2, 230])
            
            # Game stats
            stats_y = 280
            for stat, value in final_stats.items():
                if stat == "Score":
                    continue  # Already displayed above
                stat_text = self.font_style.render(f"{stat}: {value}", True, text_color)
                self.display.blit(stat_text, 
                                 [DISPLAY_WIDTH // 2 - stat_text.get_width() // 2, stats_y])
                stats_y += 30
            
            # Options
            options_y = 450
            options = [
                ("Press ENTER to Play Again", GREEN),
                ("Press M for Menu", BLUE),
                ("Press Q to Quit", RED)
            ]
            
            for text, color in options:
                option_text = self.font_style.render(text, True, color)
                self.display.blit(option_text, 
                                 [DISPLAY_WIDTH // 2 - option_text.get_width() // 2, options_y])
                options_y += 40
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()
                    self.save_stats()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.settings.sound_enabled:
                        menu_select_sound.play()
                        
                    if event.key == pygame.K_q:
                        self.save_high_score()
                        self.save_stats()
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        self.reset_game()
                        return True  # Return to game loop
                    elif event.key == pygame.K_m:
                        self.reset_game()
                        self.show_menu()
                        return True  # Return to game loop
            
            self.clock.tick(30)
        
    def reset_game(self):
        """Reset the game state"""
        self.snake = Snake(GRID_SIZE)
        self.food = Food(GRID_SIZE)
        self.score = 0
        self.level = 1
        self.score_to_next_level = 10
        self.game_over = False
        self.game_paused = False
        self.active_effects = {}
        self.snake_speed_modifier = 0
        self.particles = []
        self.game_time = 0
        self.settings.update_speed()  # Reset speed to difficulty setting
        
    def handle_food_collision(self):
        """Handle snake collision with food"""
        if self.snake.x == self.food.x and self.snake.y == self.food.y:
            food_type = self.food.type
            food_info = FOODS[food_type]
            
            # Play appropriate sound
            if self.settings.sound_enabled and food_info.sound:
                food_info.sound.play()
            
            # Create particles at food location
            if self.settings.particles_enabled:
                new_particles = food_info.create_particles(self.food.x, self.food.y)
                self.particles.extend(new_particles)
            
            # Add points based on food type (apply double_score if active)
            points = food_info.points
            if self.snake.double_score and points > 0:
                points *= 2
                
            self.score += points
            
            # Update statistics
            if food_type == "regular":
                self.stats["apples_eaten"] += 1
            else:
                self.stats["special_foods_eaten"] += 1
                if food_info.duration:  # If it's a power-up
                    self.stats["power_ups_used"] += 1
            
            # Grow the snake
            if points > 0:
                self.snake.grow(points)
            elif food_type == "shrink":
                self.snake.grow(-3)  # Shrink by 3 segments
            
            # Apply special food effects
            if food_type == "speed_up":
                self.snake_speed_modifier = 5  # Speed up temporarily
                self.active_effects["speed_up"] = pygame.time.get_ticks() + food_info.duration
                self.snake.set_effect("speed_up", True)
                
            elif food_type == "slow_down":
                self.snake_speed_modifier = -5  # Slow down temporarily
                self.active_effects["slow_down"] = pygame.time.get_ticks() + food_info.duration
                self.snake.set_effect("slow_down", True)
                
            elif food_type == "ghost":
                self.active_effects["ghost"] = pygame.time.get_ticks() + food_info.duration
                self.snake.set_effect("ghost", True)
                
            elif food_type == "double_score":
                self.active_effects["double_score"] = pygame.time.get_ticks() + food_info.duration
                self.snake.set_effect("double_score", True)
                
            elif food_type == "rainbow":
                self.active_effects["rainbow"] = pygame.time.get_ticks() + 15000  # 15 seconds of rainbow effect
                self.snake.set_effect("rainbow", True)
                
            elif food_type == "freeze":
                self.active_effects["freeze"] = pygame.time.get_ticks() + food_info.duration
                self.snake.set_effect("freeze", True)
            
            # Check for level up
            if self.score >= self.score_to_next_level:
                self.level_up()
            
            # Generate new food
            self.food.respawn()
            
            return True
        return False
        
    def level_up(self):
        """Level up the game, making it progressively harder"""
        self.level += 1
        self.score_to_next_level += 10 * self.level  # Increase score needed for next level
        
        # Update highest level stat
        if self.level > self.stats["highest_level"]:
            self.stats["highest_level"] = self.level
            
        # Increase snake speed slightly with each level
        if self.settings.difficulty != "easy":  # Don't make easy mode too hard
            self.settings.snake_speed += 1
    
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
            
            # Reset corresponding snake effects
            self.snake.set_effect(effect, False)
            
            # Reset speed modifier
            if effect in ["speed_up", "slow_down"]:
                self.snake_speed_modifier = 0
            
        # Update particles
        if self.settings.particles_enabled:
            for particle in self.particles[:]:
                if particle.update():  # If particle is expired
                    self.particles.remove(particle)
    
    def game_loop(self):
        """Main game loop"""
        # Show menu first
        self.show_menu()
        
        # Reset game state
        self.reset_game()
        
        # Game timing variables
        game_start_time = time.time()
        frame_count = 0
        fps_timer = time.time()
        fps = 0
        
        # Control flags
        direction_set = False  # Flag to prevent multiple direction changes per frame
        
        while not self.game_over:
            current_time = pygame.time.get_ticks()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Save stats before quitting
                    self.update_stats(game_over=True)
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if not direction_set:
                        # Process direction keys based on control scheme
                        if self.settings.control_scheme == "arrow":
                            if event.key == pygame.K_LEFT and self.snake.dx != GRID_SIZE:
                                if not self.snake.queue_direction(-GRID_SIZE, 0):
                                    self.snake.dx = -GRID_SIZE
                                    self.snake.dy = 0
                            elif event.key == pygame.K_RIGHT and self.snake.dx != -GRID_SIZE:
                                if not self.snake.queue_direction(GRID_SIZE, 0):
                                    self.snake.dx = GRID_SIZE
                                    self.snake.dy = 0
                            elif event.key == pygame.K_UP and self.snake.dy != GRID_SIZE:
                                if not self.snake.queue_direction(0, -GRID_SIZE):
                                    self.snake.dy = -GRID_SIZE
                                    self.snake.dx = 0
                            elif event.key == pygame.K_DOWN and self.snake.dy != -GRID_SIZE:
                                if not self.snake.queue_direction(0, GRID_SIZE):
                                    self.snake.dy = GRID_SIZE
                                    self.snake.dx = 0
                        else:  # WASD controls
                            if event.key == pygame.K_a and self.snake.dx != GRID_SIZE:
                                if not self.snake.queue_direction(-GRID_SIZE, 0):
                                    self.snake.dx = -GRID_SIZE
                                    self.snake.dy = 0
                            elif event.key == pygame.K_d and self.snake.dx != -GRID_SIZE:
                                if not self.snake.queue_direction(GRID_SIZE, 0):
                                    self.snake.dx = GRID_SIZE
                                    self.snake.dy = 0
                            elif event.key == pygame.K_w and self.snake.dy != GRID_SIZE:
                                if not self.snake.queue_direction(0, -GRID_SIZE):
                                    self.snake.dy = -GRID_SIZE
                                    self.snake.dx = 0
                            elif event.key == pygame.K_s and self.snake.dy != -GRID_SIZE:
                                if not self.snake.queue_direction(0, GRID_SIZE):
                                    self.snake.dy = GRID_SIZE
                                    self.snake.dx = 0
                                    
                        direction_set = True
                        
                    # Other key commands
                    if event.key == pygame.K_p:  # Pause game
                        self.game_paused = not self.game_paused
                    elif event.key == pygame.K_m:  # Back to menu
                        self.save_high_score()
                        self.update_stats(game_over=True)
                        self.show_menu()
                        self.reset_game()
                        game_start_time = time.time()
                    elif event.key == pygame.K_ESCAPE:  # Quit game
                        self.update_stats(game_over=True)
                        pygame.quit()
                        sys.exit()
            
            # Reset direction flag for next frame
            direction_set = False
            
            # Skip updates if game is paused
            if self.game_paused:
                self.draw_pause_screen()
                continue
                
            # Update game time
            self.game_time = int(time.time() - game_start_time)
            
            # Update food animations
            self.food.update(current_time)
            
            # Update snake position
            self.snake.update()
            
            # Track distance traveled for stats
            if self.snake.dx != 0 or self.snake.dy != 0:
                self.stats["distance_traveled"] += 1
            
            # Check collisions with walls
            if self.settings.walls_enabled:
                if self.snake.check_collision_with_walls():
                    if self.settings.sound_enabled:
                        game_over_sound.play()
                    self.game_over_screen()
                    continue
            else:
                self.snake.check_collision_with_walls(wrap_around=True)
            
            # Check collision with self
            if self.snake.check_collision_with_self():
                if self.settings.sound_enabled:
                    game_over_sound.play()
                self.game_over_screen()
                continue
            
            # Handle food collision
            self.handle_food_collision()
            
            # Update effects
            self.update_effects()
            
            # Draw game elements
            self.draw_game_screen()
            
            # Calculate and display FPS
            frame_count += 1
            if time.time() - fps_timer > 1.0:  # Update FPS every second
                fps = frame_count
                frame_count = 0
                fps_timer = time.time()
                
            # Show FPS if in debug mode
            # self.display.blit(self.small_font.render(f"FPS: {fps}", True, GREEN), [DISPLAY_WIDTH - 80, DISPLAY_HEIGHT - 20])
            
            # Update display
            pygame.display.update()
            
            # Adjust game speed with modifiers
            adjusted_speed = self.settings.snake_speed + self.snake_speed_modifier
            if adjusted_speed < 5:  # Minimum speed
                adjusted_speed = 5
            self.clock.tick(adjusted_speed)
            
    def draw_pause_screen(self):
        """Draw the pause screen"""
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black overlay
        self.display.blit(overlay, (0, 0))
        
        # Pause title
        pause_text = self.title_font.render("PAUSED", True, BLUE)
        self.display.blit(pause_text, 
                         [DISPLAY_WIDTH // 2 - pause_text.get_width() // 2, 
                          DISPLAY_HEIGHT // 2 - pause_text.get_height() // 2 - 50])
                          
        # Instructions
        text_color = WHITE
        instructions = [
            "Press P to Resume",
            "Press M for Menu",
            "Press ESC to Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            instr_text = self.font_style.render(instruction, True, text_color)
            self.display.blit(instr_text, 
                             [DISPLAY_WIDTH // 2 - instr_text.get_width() // 2, 
                              DISPLAY_HEIGHT // 2 + i * 40])
        
        # Check for pause toggle or other commands
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.update_stats(game_over=True)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game_paused = False
                elif event.key == pygame.K_m:
                    self.save_high_score()
                    self.update_stats(game_over=True)
                    self.show_menu()
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.update_stats(game_over=True)
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
        self.clock.tick(15)
        
    def draw_game_screen(self):
        """Draw all game elements"""
        # Determine background based on settings
        if self.settings.dark_mode:
            bg_color = (20, 20, 20)  # Dark background
        else:
            bg_color = WHITE  # Light background
            
        self.display.fill(bg_color)
        
        # Draw background based on style
        if self.settings.background_style == "grid" and not self.settings.dark_mode:
            self.draw_grid()
        elif self.settings.background_style == "gradient":
            self.draw_gradient_background()
            
        # Draw particles
        if self.settings.particles_enabled:
            for particle in self.particles:
                particle.draw(self.display)
        
        # Draw food
        self.food.draw(self.display, self.settings.dark_mode, self.settings.food_style)
        
        # Draw snake
        self.snake.draw(self.display, self.settings.dark_mode, self.settings.snake_style)
        
        # Draw UI elements
        self.draw_game_ui()
        
    def draw_gradient_background(self):
        """Draw gradient background"""
        if self.settings.dark_mode:
            color1 = (10, 10, 40)  # Dark blue
            color2 = (40, 10, 40)  # Dark purple
        else:
            color1 = (220, 240, 255)  # Light blue
            color2 = (240, 220, 255)  # Light purple
            
        for y in range(DISPLAY_HEIGHT):
            # Interpolate between the two colors
            ratio = y / DISPLAY_HEIGHT
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(self.display, (r, g, b), (0, y), (DISPLAY_WIDTH, y))
            
    def draw_game_ui(self):
        """Draw game UI elements"""
        text_color = WHITE if self.settings.dark_mode else BLACK
        
        # Score and high score
        self.show_score()
        
        # Level indicator
        level_text = self.font_style.render(f"Level: {self.level}", True, BLUE)
        self.display.blit(level_text, [10, 50])
        
        # Timer
        time_text = self.small_font.render(f"Time: {self.format_time(self.game_time)}", True, text_color)
        self.display.blit(time_text, [10, 80])
        
        # Next level progress
        next_level_text = self.small_font.render(
            f"Next level: {self.score}/{self.score_to_next_level}", True, text_color)
        self.display.blit(next_level_text, [10, 100])
        
        # Draw progress bar for next level
        progress_width = 150
        progress_height = 10
        progress_x = 10
        progress_y = 120
        progress_fill = min(1.0, self.score / self.score_to_next_level) * progress_width
        
        # Bar background
        pygame.draw.rect(self.display, GRAY, 
                        [progress_x, progress_y, progress_width, progress_height])
        # Fill based on progress
        pygame.draw.rect(self.display, GREEN, 
                        [progress_x, progress_y, progress_fill, progress_height])
        
        # Show active effects
        effect_y = 150
        for effect, expiry_time in self.active_effects.items():
            # Calculate time remaining
            time_left = max(0, (expiry_time - pygame.time.get_ticks()) // 1000)
            effect_text = self.small_font.render(
                f"{effect.replace('_', ' ').title()}: {time_left}s", True, BLUE)
            self.display.blit(effect_text, [10, effect_y])
            effect_y += 20
            
            # Draw time bar
            if effect in FOODS and FOODS[effect].duration:
                duration = FOODS[effect].duration // 1000  # Convert to seconds
                time_ratio = time_left / duration
                bar_width = 100 * time_ratio
                pygame.draw.rect(self.display, GRAY, [110, effect_y - 15, 100, 5])
                pygame.draw.rect(self.display, FOODS[effect].color, [110, effect_y - 15, bar_width, 5])

# Start the game
if __name__ == "__main__":
    game = Game()
    game.game_loop()
