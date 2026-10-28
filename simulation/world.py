from engine import physics, collisions, forces

class World:
    def update(self, dt):
        physics.apply_gravity(self.particles, dt)
        physics.integrate(self.particles, dt)
        collisions.resolve_wall_collisions(self.particles)
