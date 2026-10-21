class Particle:
    def __init__(self, x, y, mass=1.0, radius=5):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.mass = mass
        self.radius = radius