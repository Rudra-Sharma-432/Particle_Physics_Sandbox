import pygame

# 1. Initialize Pygame
pygame.init()

# 2. Window settings
WIDTH = 1000
HEIGHT = 630
FPS = 60
MASS_SLIDER = 100
G = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Gravity Simulator")

clock = pygame.time.Clock()


# Particle class
class Particle:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = 0

        self.mass = mass
        self.radius = max(3, mass ** 0.5)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (100, 200, 255),
            (int(self.x), int(self.y)),
            int(self.radius)
        )

    def distance(particle):
        return ((self.x - particle.x)**2 + (self.y - particle.y)**2)**0.5


particles = [
    Particle(300, 250, MASS_SLIDER),
    Particle(500, 350, MASS_SLIDER)
]

# 3. Main loop
running = True

while running:
    # Limit FPS
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
          
      if event.type == pygame.MOUSEBUTTONDOWN:
          if button.collidepoint(event.pos):
              print("Button clicked!")
              
          if world.collidepoint(event.pos):
              # Extract the coordinates directly from the click event
              x, y = event.pos
              print(f"Clicked inside world at X: {x}, Y: {y}")
              
              # spawn physics particles
              particles.append(Particle(x, y, MASS_SLIDER))
              print(particles)


    # Clear screen
    screen.fill((50, 50, 50))


    world = pygame.Rect(20, 80, 960, 530)
    pygame.draw.rect(screen, (0, 0, 0), world)
    
    button = pygame.Rect(20, 20, 120, 40)
    pygame.draw.rect(screen, (50, 100, 180), button)
    font = pygame.font.Font(None, 28)
    text = font.render("Play / Pause", True, (255, 255, 255))
    screen.blit(text, (button.x + 5, button.y + 10))


    slider = pygame.Rect(200, 30, 200, 6)
    pygame.draw.rect(screen, (150, 150, 150), slider)
    handle_x = 300
    pygame.draw.circle(
        screen,
        (100, 200, 255),
        (handle_x, slider.centery),
        10
    )

    
    for particle in particles:
      particle.draw(screen)

    for i in particles:
        for j in particles:
            i.ax += (G * j.mass / abs(j.x - i.x)**2)
            i.ay += (G * j.mass / abs(j.y - i.y)**2)

            


    # Display the frame
    pygame.display.flip()

# 4. Clean up
pygame.quit()
