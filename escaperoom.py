import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
PLAYER_SIZE = 50
PLAYER_SPEED = 5

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basic Movement in Pygame")

# Player variables
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Move the player based on key presses
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_y += PLAYER_SPEED

    # Ensure the player stays within the screen bounds
    player_x = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, player_x))
    player_y = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, player_y))

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(30)
