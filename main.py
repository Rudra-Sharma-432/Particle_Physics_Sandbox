import math
import pygame

import settings
from geometry import Vector
from entities import Particle
from simulation import SimulationSpace

space = SimulationSpace(G=1.0)
planet = Particle(
        mass=100.0,
        pos=Vector(x=100.0, y=100.0),
        velo=Vector(x=0.0, y=0.0)
    )
moon = Particle(
        mass=40.0,
        pos=Vector(x=50.0, y=0.0),
        velo=Vector(x=0.0, y=50.0)
    )

space.add_particle(planet)
space.add_particle(moon)

FPS = 60
dt = 1/1000
steps_per_second = int(1.0 / dt)



# pygame setup
pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Space Gravity Simulator")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

running = True
paused = False

mass = 25
MIN_MASS = 1
MAX_MASS = 100

BLACK = (0, 0, 0)
BGC = (25, 25, 25)
WHITE = (255, 255, 255)
BLUE = (100, 200, 255)
GRAY = (120, 120, 120)
DARK_GRAY = (45, 45, 45)


# Slider geometry
slider = pygame.Rect(110, 16, 200, 6)
slider_dragging = False

# Buttons
play_button = pygame.Rect(10, 40, 100, 40)
restart_button = pygame.Rect(120, 40, 100, 40)

world = pygame.Rect(10, 100, settings.WIDTH - 20, settings.HEIGHT - 110)


def draw_text(text, x, y, color=WHITE):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def draw_ui():
    # Mass slider
    draw_text(f"Mass: {mass}", 10, 10)

    pygame.draw.rect(screen, GRAY, slider)

    slider_x = slider.x + (
        (mass - MIN_MASS) / (MAX_MASS - MIN_MASS)
    ) * slider.width

    pygame.draw.circle(
        screen,
        BLUE,
        (int(slider_x), slider.centery),
        10
    )

    # Play / Pause button
    pygame.draw.rect(
        screen,
        DARK_GRAY,
        play_button,
        border_radius=6
    )
    draw_text(
        "Resume" if paused else "Pause",
        play_button.x + 13 if paused else play_button.x + 20,
        play_button.y + 10
    )

    # Restart button
    pygame.draw.rect(
        screen,
        DARK_GRAY,
        restart_button,
        border_radius=6
    )
    draw_text("Restart", restart_button.x + 15, restart_button.y + 10)

    pygame.draw.rect(screen, BLACK, world, border_radius=6)



# =========================
# 5. INPUT HANDLING
# =========================
def update_mass_from_mouse(mouse_x):
    global mass

    ratio = (mouse_x - slider.x) / slider.width
    ratio = max(0, min(1, ratio))

    mass = round(
        MIN_MASS + ratio * (MAX_MASS - MIN_MASS)
    )


while running:
    dt = clock.tick(FPS) / 1000
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if slider.collidepoint(mouse_pos) or (
                math.hypot(
                    mouse_pos[0] - (
                        slider.x
                        + (mass - MIN_MASS)
                        / (MAX_MASS - MIN_MASS)
                        * slider.width
                    ),
                    mouse_pos[1] - slider.centery
                ) <= 15
            ):
                slider_dragging = True
                update_mass_from_mouse(mouse_pos[0])

            elif play_button.collidepoint(mouse_pos):
                paused = not paused

            elif restart_button.collidepoint(mouse_pos):
                space = SimulationSpace(G=1.0)
                paused = False

            elif world.collidepoint(mouse_pos):
                # Spawn a particle in the simulation area
                pos_vector = Vector(mouse_pos[0], mouse_pos[1])
                space.add_particle(Particle(mass, pos_vector))

        elif event.type == pygame.MOUSEBUTTONUP:
            slider_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if slider_dragging:
                update_mass_from_mouse(event.pos[0])


    # ---- Physics ----
    if not paused:
        space.update(dt)

    # ---- Drawing ----
    screen.fill(BGC)

    draw_ui()

    for particle in space.particles:
        particle.draw(screen, BLUE)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(settings.FPS)  # limits FPS to 60

pygame.quit()