#Inspired by Ethan Mollick and BING and ChatGPT
#phew but needed much polishing and code correcting!
# Import libraries to use in the code
import pygame
import random
import math

# Define constants to use in the code
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WIDTH = 800
HEIGHT = 600
FPS = 60
NUM_PARTICLES = 100
RADIUS = 10
SPEED = 5
ENTROPY_THRESHOLD = 0.95

# Define Molecule class
# Define a class for molecules
class Molecule(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2*RADIUS, 2*RADIUS))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, color, (RADIUS, RADIUS), RADIUS)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vx = random.choice([-SPEED, SPEED])
        self.vy = random.choice([-SPEED, SPEED])

    def update(self):
        # Move the molecule according to its velocity
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Bounce off the walls if necessary
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy = -self.vy

    def collide(self, other):
        # Check if this molecule collides with another molecule
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        return distance < 2*RADIUS

    def bounce(self, other):
        # Exchange velocities with another molecule after collision
        temp_vx = self.vx
        temp_vy = self.vy
        self.vx = other.vx
        self.vy = other.vy
        other.vx = temp_vx
        other.vy = temp_vy

#
# Define a function to calculate the entropy of the system
def entropy():
    # Initialize the count variables to zero
    count1 = 0 # Top left quadrant
    count2 = 0 # Top right quadrant
    count3 = 0 # Bottom left quadrant
    count4 = 0 # Bottom right quadrant

    for molecule in all_sprites:
        x = molecule.rect.centerx
        y = molecule.rect.centery

        if x < WIDTH / 2 and y < HEIGHT / 2:
            count1 += 1
        elif x > WIDTH / 2 and y < HEIGHT / 2:
            count2 += 1
        elif x < WIDTH / 2 and y > HEIGHT / 2:
            count3 += 1
        else:
            count4 += 1

    p1 = count1 / NUM_PARTICLES
    p2 = count2 / NUM_PARTICLES
    p3 = count3 / NUM_PARTICLES
    p4 = count4 / NUM_PARTICLES

    k = 1
    S = 0
    if p1 > 0:
        S += -k * p1 * math.log(p1)
    if p2 > 0:
        S += -k * p2 * math.log(p2)
    if p3 > 0:
        S += -k * p3 * math.log(p3)
    if p4 > 0:
        S += -k * p4 * math.log(p4)

    return S
        
# Return the entropy value
# Define a function to render the entropy value as text
def display_entropy():
    S = entropy()
    text = font.render(f"Entropy: {S:.2f}", True, BLACK)
    screen.blit(text, (10, 10))

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BING-Entropy Game")
clock = pygame.time.Clock()

# Create a group of sprites for the molecules
all_sprites = pygame.sprite.Group()

# Create N molecules with random positions and colors
for i in range(NUM_PARTICLES):
    x = random.randint(RADIUS, WIDTH - RADIUS)
    y = random.randint(RADIUS, HEIGHT - RADIUS)
    color = random.choice([RED, GREEN, BLUE])
    molecule = Molecule(x, y, color)
    all_sprites.add(molecule)

# Create a single white molecule
x = random.randint(RADIUS, WIDTH - RADIUS)
y = random.randint(RADIUS, HEIGHT - RADIUS)
white_molecule = Molecule(x, y, WHITE)
all_sprites.add(white_molecule)

# Create a font object for rendering text
font = pygame.font.SysFont("Arial", 32)

# Create a boolean variable to indicate the game status
running = True
won = False

ENTROPY_THRESHOLD = 0.95  # Set the entropy threshold value
# Main game loop
while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # Check for closing the window
        if event.type == pygame.QUIT:
            running = False

        # Check for pressing the arrow keys
        if event.type == pygame.KEYDOWN:
            # Increase or decrease the speed of the molecules
            if event.key == pygame.K_UP:
                for molecule in all_sprites:
                    molecule.vx *= 1.1
                    molecule.vy *= 1.1
            if event.key == pygame.K_DOWN:
                for molecule in all_sprites:
                    molecule.vx *= 0.9
                    molecule.vy *= 0.9

            # Change the direction of the molecules
            if event.key == pygame.K_LEFT:
                for molecule in all_sprites:
                    temp_vx = molecule.vx
                    molecule.vx = -molecule.vy
                    molecule.vy = temp_vx
            if event.key == pygame.K_RIGHT:
                for molecule in all_sprites:
                    temp_vx = molecule.vx
                    molecule.vx = molecule.vy
                    molecule.vy = -temp_vx

    # Update the sprites
    all_sprites.update()
    
    # Check for collisions between the molecules and bounce them off each other
    for i, molecule1 in enumerate(all_sprites):
        for j, molecule2 in enumerate(all_sprites):
            if i < j and molecule1.collide(molecule2):
                molecule1.bounce(molecule2)

    # Draw everything on the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    display_entropy()
    
    # Check if the entropy reaches the threshold and end the game if so
    S = entropy()
    if S > ENTROPY_THRESHOLD and not won:
        text = font.render("You win!", True, RED)
        screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
        pygame.display.flip()
        won = True


    # Flip the display buffer to show everything on the screen
    pygame.display.flip()

# Quit pygame and exit the program
pygame.quit()

