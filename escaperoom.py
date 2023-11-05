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
PLAYER_SIZE = 30

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image
    
def solveKnapsackProblem(W, wt, val, n):
    if n == 0 or W == 0:
        return 0
    
    if wt[n-1] > W:
        return solveKnapsackProblem(W, wt, val, n-1)
    
    else:
        return max(val[n-1] + solveKnapsackProblem(W-wt[n-1], wt, val, n-1), solveKnapsackProblem(W, wt, val, n-1))


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

class Treasure:
    def __init__(self, trex, trey):
        self.x = trex
        self.y = trey
        self.size = TREASURE_SIZE
        self.weight = random.randint(10,50)
        self.profit = random.randint(10,200)

    def drawTreasures(self):
        weighttext = font2.render(str(self.weight),True,(0,0,0))
        profittext = font2.render(str(self.profit),True,(0,0,0))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, self.size, self.size))
        screen.blit(weighttext, (self.x, self.y)) 
        screen.blit(profittext, (self.x, self.y + 15)) 

def checkCollision(keys):
    global weight_sum
    global profit_sum
    global sc_no
    if keys[pygame.K_e]:
        for treasure in treasures:
            if pygame.Rect(player.player_x, player.player_y, PLAYER_SIZE, PLAYER_SIZE).colliderect(pygame.Rect(treasure.x, treasure.y, TREASURE_SIZE, TREASURE_SIZE)):
                collected_treasures.append(treasure)
                weight_sum += treasure.weight
                profit_sum += treasure.profit
                treasures.remove(treasure)

        if pygame.Rect(player.player_x, player.player_y, PLAYER_SIZE, PLAYER_SIZE).colliderect(pygame.Rect(door['x'],door['y'],door['size_x'],door['size_y'])):
            if profit_sum == knapsack_ans:
                print("game won")
                sc_no = 2
            else:
                print("Wrong answer")

# Creating the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt Game")

# initializing all the treasures with random weights
treasures = []
t1 = Treasure(200,100)
t2 = Treasure(300,100) 
t3 = Treasure(400,100)
t4 = Treasure(500,100)

treasures.append(t1)
treasures.append(t2)
treasures.append(t3)
treasures.append(t4)

#solving knapsack problem
wt = [t.weight for t in treasures]
pt = [t.profit for t in treasures]

knapsack_ans = solveKnapsackProblem(80, wt, pt, 4)
print(knapsack_ans)

# Initialize game variables
sc_no = 1
collected_treasures = []
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 20)
font3 = pygame.font.Font(None, 50)
clock = pygame.time.Clock()
spritesheet = SpriteSheet(pygame.image.load('amongus.png').convert_alpha())
player = Player()
player.manageAnimations()
weight_sum = 0
profit_sum = 0
trap = Trap(100,100,30)

#define game win point
door = {'x':0, 'y':300, 'size_x':20, 'size_y':40}

# Game loop
if __name__ == '__main__':
    running = True
    while running:
        dt = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if sc_no == 1:
            # Check for player input
            frame = player.updateAnimations(dt)
            keys = pygame.key.get_pressed()
            player.playerMovement(keys)

            # Check for all collisions
            checkCollision(keys)

            # Clear the screen
            screen.fill(WHITE)

            # Draw the player
            screen.blit(frame, (player.player_x,player.player_y))
            player.drawAttributes()
            
            trap.drawTrap()
            trap.trapActivation(player)
            
            # Draw the treasures
            for treasure in treasures:
                treasure.drawTreasures()
                
            # Draw collected treasures
            wt_text = font.render("Weights: " + str(weight_sum), True, (0, 0, 0))
            pt_text = font.render("Profit: " + str(profit_sum), True, (0, 0, 0))
            screen.blit(wt_text, (10, 10))
            screen.blit(pt_text, (10, 30))
            
            #draw the win point, i.e., the exit door
            pygame.draw.rect(screen, (0,125,125), pygame.Rect(door['x'], door['y'], 20,40))

        if sc_no == 2:
            screen.fill(WHITE)
            wintxt = font3.render("Game Won", True, (0,0,0))
            screen.blit(wintxt, (300, 250))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
