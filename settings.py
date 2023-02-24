import pygame
#pygame settings go here

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Zombie Infection Simulator"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
CYAN = (0, 255, 255)

# Player settings
PLAYER_MOVE_SPEED = 1
PLAYER_HEALTH = 100

# Zombie settings
ZOMBIE_MOVE_SPEED = .1
ZOMBIE_HEALTH = 100

# Game settings
FPS = 60

# Human settings
NUM_HUMANS = 100

# Zombie settings
NUM_ZOMBIES = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))