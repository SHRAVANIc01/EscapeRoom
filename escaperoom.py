import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0,255,0)
TREASURE_SIZE = 40
PLAYER_SIZE = 20

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image


class Player:
    def __init__(self):
        self.player_x, self.player_y = WIDTH // 2, HEIGHT // 2
        self.animation_list = []
        self.which_anim = 0
        self.ut = 0
        self.isMoving = False
        self.health = 100

    def playerMovement(self, keys):
        # handling player movement speed
        self.isMoving = True
        if keys[pygame.K_UP]:
            self.player_y -= 5
        if keys[pygame.K_DOWN]:
            self.player_y += 5
        if keys[pygame.K_LEFT]:
            self.player_x -= 5
        if keys[pygame.K_RIGHT]:
            self.player_x += 5

    def manageAnimations(self):
        #add all the animations in the list to get access later

        self.animation_list.append([spritesheet.get_image(0, 120, 130, 0.4, BLACK)])
        temp = []
        for i in range(1,8):
            temp.append(spritesheet.get_image(i, 125, 130, 0.4, BLACK))
        self.animation_list.append(temp)

    def updateAnimations(self, dt):
        if self.isMoving:
            #set moving animations
            self.ut += 5
            if self.ut * dt >= 0.4:
                self.which_anim = (self.which_anim + 1)%7
                self.ut = 0
            frame = self.animation_list[1][self.which_anim]
        else:
            #set idle animation
            frame = self.animation_list[0][0]
            self.which_anim = 0

        return frame
    
    def updateHealth(self, damage):
        self.health -= damage
        
    def drawAttributes(self):
        pygame.draw.rect(screen, GREEN, pygame.Rect(600,50,self.health,20))
    
class Trap:
    def __init__(self, trapx, trapy, trapdamage):
        self.x = trapx
        self.y = trapy
        self.damage = trapdamage
        self.trapSize = 30
        self.isDestroyed = False
        
    def drawTrap(self):
        if not self.isDestroyed:
            pygame.draw.rect(screen, BLACK,pygame.Rect(self.x,self.y,self.trapSize,self.trapSize))
        
    def trapActivation(self, player):
        if pygame.Rect(player.player_x, player.player_y, PLAYER_SIZE, PLAYER_SIZE).colliderect(pygame.Rect(self.x,self.y,self.trapSize,self.trapSize)) and not self.isDestroyed:
            player.updateHealth(self.damage)
            self.isDestroyed = True

# Creating the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt Game")

# Define the treasures with random positions
# treasures = [{"x": random.randint(0, WIDTH - TREASURE_SIZE), "y": random.randint(0, HEIGHT - TREASURE_SIZE)} for _ in range(5)]
treasures = [{'x':200, 'y':100, 'weight':100},
             {'x':300, 'y':200, 'weight':20},
             {'x':100, 'y':300, 'weight':30},
             {'x':500, 'y':400, 'weight':40}]

# Initialize game variables
collected_treasures = []
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
spritesheet = SpriteSheet(pygame.image.load('amongus.png').convert_alpha())
player = Player()
player.manageAnimations()
weight_sum = 0
trap = Trap(100,100,30)

# Game loop
running = True
while running:
    dt = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for player input
    frame = player.updateAnimations(dt)
    keys = pygame.key.get_pressed()
    player.playerMovement(keys)

    # Check for treasure collection
    for treasure in treasures:
        if pygame.Rect(player.player_x, player.player_y, PLAYER_SIZE, PLAYER_SIZE).colliderect(pygame.Rect(treasure["x"], treasure["y"], TREASURE_SIZE, TREASURE_SIZE)):
            collected_treasures.append(treasure)
            weight_sum += treasure['weight']
            treasures.remove(treasure)

    # Clear the screen
    screen.fill(WHITE)

    if weight_sum == 120:
        wintxt = font.render("Game Won", True, (0,0,0))
        screen.blit(wintxt, (10, 10))

    # Draw the player
    # pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(player.player_x, player.player_y, PLAYER_SIZE, PLAYER_SIZE))
    screen.blit(frame, (player.player_x,player.player_y))
    player.drawAttributes()
    
    trap.drawTrap()
    trap.trapActivation(player)
    

    # Draw the treasures
    for treasure in treasures:
        w = treasure['weight']
        weighttext = font.render(str(w),False,(0,0,0))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(treasure["x"], treasure["y"], TREASURE_SIZE, TREASURE_SIZE))
        screen.blit(weighttext, (treasure["x"], treasure["y"])) 

    # Draw collected treasures
    # text = font.render("Collected Treasures: " + str(len(collected_treasures)), True, (0, 0, 0))
    # screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
