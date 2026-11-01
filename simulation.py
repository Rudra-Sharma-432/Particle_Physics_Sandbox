import math
from geometry import Vector
from entities import Particle

class SimulationSpace:
    def __init__(self, G: float = 1.0):
        self.particles = []
        self.G = G  # Gravitational constant

    def add_particle(self, particle: Particle):
        self.particles.append(particle)

    def apply_gravity(self):
        """Calculates mutual gravitational attraction between all particles."""
        n = len(self.particles)
        
        # Reset accelerations to zero before calculating new forces
        for p in self.particles:
            p.acc = Vector(0, 0)

        # Pairwise comparison (Particle i acts on Particle j, and vice versa)
        for i in range(n):
            for j in range(i + 1, n):
                p1 = self.particles[i]
                p2 = self.particles[j]

                # Displacement vector from p1 to p2
                displacement = p2.pos - p1.pos
                distance = displacement.magnitude

                # Prevent division by zero if particles overlap perfectly
                if distance < 0.1:
                    continue

                # Newton's Law of Universal Gravitation: F = G * (m1 * m2) / r^2
                # Force magnitude
                force_mag = (self.G * p1.mass * p2.mass) / (distance ** 2)
                
                # Direction vector (unit vector pointing from p1 to p2)
                direction = displacement * (1.0 / distance)

                # Force vector
                force_vector = direction * force_mag

                # Acceleration = Force / Mass (F = ma -> a = F/m)
                p1.acc = p1.acc + (force_vector * (1.0 / p1.mass))
                p2.acc = p2.acc - (force_vector * (1.0 / p2.mass))  # Opposite direction

    def handle_collisions(self, restitution: float = 1.0):
        """Placeholder for handling bounce or merging collisions."""
        # You will loop through pairs here, check if their distance < (radius1 + radius2)
        # And adjust their velocities (velo) accordingly.
        pass

    def update(self, dt: float):
        """Advances the simulation by time step dt."""
        self.apply_gravity()
        self.handle_collisions()

        # Update positions and velocities for all particles using standard Euler integration
        for p in self.particles:
            # v = v + a * dt (Uses your Vector scalar multiplication and addition!)
            p.velo = p.velo + (p.acc * dt)
            # x = x + v * dt
            p.pos = p.pos + (p.velo * dt)
