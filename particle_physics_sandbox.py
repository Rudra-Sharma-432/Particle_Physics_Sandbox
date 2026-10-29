
import pygame
import math

# =========================
# 1. INITIALIZATION & SETTINGS
# =========================
pygame.init()

WIDTH, HEIGHT = 1000, 640
FPS = 60

G = 1


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Gravity Simulator")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

BLACK = (0, 0, 0)
BGC = (25, 25, 25)
WHITE = (255, 255, 255)
BLUE = (100, 200, 255)
GRAY = (120, 120, 120)
DARK_GRAY = (45, 45, 45)

# =========================
# 2. PARTICLE CLASS
# =========================
class Particle:
    def __init__(self, x, y, mass):
        self.x = float(x)
        self.y = float(y)
        self.mass = mass
        self.radius = max(3, math.sqrt(mass))

        # Motion
        self.vx = 0.0
        self.vy = 0.0

        self.ax = 0.0
        self.ay = 0.0

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            BLUE,
            (int(self.x), int(self.y)),
            int(self.radius)
        )


# =========================
# 3. SIMULATION STATE
# =========================
particles = []

running = True
paused = False

mass = 25
MIN_MASS = 1
MAX_MASS = 100

# Slider geometry
slider = pygame.Rect(110, 16, 200, 6)
slider_dragging = False

# Buttons
play_button = pygame.Rect(10, 40, 100, 40)
restart_button = pygame.Rect(120, 40, 100, 40)

world = pygame.Rect(10, 100, WIDTH - 20, HEIGHT - 110)


# =========================
# 4. UI DRAWING
# =========================
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


# =========================
# 6. MAIN LOOP
# =========================
while running:
    dt = clock.tick(FPS) / 100

    # ---- Events ----
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
                particles.clear()
                paused = False

            elif world.collidepoint(mouse_pos):
                # Spawn a particle in the simulation area
                particles.append(
                    Particle(mouse_pos[0], mouse_pos[1], mass)
                )

        elif event.type == pygame.MOUSEBUTTONUP:
            slider_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if slider_dragging:
                update_mass_from_mouse(event.pos[0])

    # ---- Physics ----
    if not paused:
        # TODO 1: Calculate gravitational acceleration
        # between every pair of particles.
        for p1 in particles:
            p1.ax = 0.0
            p1.ay = 0.0

            for p2 in particles:
                if p1 == p2:
                    continue

                dist = ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5 + 0.0000000001

                a = G * p2.mass/dist**2

                p1.ax += a * (p2.x - p1.x)/dist
                p1.ay += a * (p2.y - p1.y)/dist


        # TODO 2: Update particle velocities using dt.
        for p in particles:
            p.vx += p.ax * dt
            p.vy += p.ay * dt


        # TODO 3: Update particle positions using dt.
        for p in particles:
            p.x += p.vx * dt
            p.y += p.vy * dt

        for p1_idx in range(len(particles)):
            for p2_idx in range(p1_idx + 1, len(particles)):
                
                p1 = particles[p1_idx]
                p2 = particles[p2_idx]

                dx = p2.x - p1.x
                dy = p2.y - p1.y

                dist = ((dx)**2 + (dy)**2)**0.5 + 0.0000000001
                overlap = p1.radius + p2.radius - dist
                if overlap > 0:
                    
                    nx = (dx)/dist
                    ny = (dy)/dist

                    p1.x -= nx*overlap/2
                    p1.y -= ny*overlap/2

                    p2.x += nx*overlap/2
                    p2.y += ny*overlap/2

                    rvx = p2.vx - p1.vx
                    rvy = p2.vy - p1.vy

                    relative_speed = rvx * nx + rvy * ny

                    if relative_speed < 0:
                        restitution = 0.9

                        inv_m1 = 1 / p1.mass
                        inv_m2 = 1 / p2.mass

                        j = -(1 + restitution) * relative_speed
                        j /= inv_m1 + inv_m2

                        impulse_x = j * nx
                        impulse_y = j * ny

                        p1.vx -= impulse_x / p1.mass
                        p1.vy -= impulse_y / p1.mass

                        p2.vx += impulse_x / p2.mass
                        p2.vy += impulse_y / p2.mass


#                     velo = ((p1.vx)**2 + (p1.vy)**2)**0.5
# 
#                     p1.vx -= nx * overlap/(2*dt)
#                     p1.vy -= ny * overlap/(2*dt)
# 
#                     p2.vx += nx * overlap/(2*dt)
#                     p2.vy += ny * overlap/(2*dt)


        pass

    # ---- Drawing ----
    screen.fill(BGC)

    draw_ui()

    for particle in particles:
        particle.draw(screen)


    pygame.display.flip()


# =========================
# 7. CLEANUP
# =========================
pygame.quit()
