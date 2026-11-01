import math
from geometry import Vector
from entities import Particle
from simulation import SimulationSpace

def run_test():
    # 1. Initialize our universe with a custom Gravitational Constant G
    space = SimulationSpace(G=1.0)

    # 2. Create Particle 1: A heavy stationary "planet" at the origin (0, 0)
    planet = Particle(
        mass=1000.0,
        pos=Vector(x=0.0, y=0.0),
        velo=Vector(x=0.0, y=0.0)
    )

    # 3. Create Particle 2: A lighter "moon" placed at x=10, y=0
    # Adjusted velocity to 10.0 m/s for a perfectly balanced circular orbit!
    moon = Particle(
        mass=10.0,
        pos=Vector(x=10.0, y=0.0),
        velo=Vector(x=0.0, y=10.0)
    )

    # 4. Add them to our simulation space
    space.add_particle(planet)
    space.add_particle(moon)

    print("--- SIMULATION STARTING ---")
    print(f"Initial Planet: {planet}")
    print(f"Initial Moon:   {moon}\n")

    # 5. Setup physics loop constants
    total_seconds = 5.0
    dt = 0.01  # 10 millisecond steps prevent overshoot bugs
    steps_per_second = int(1.0 / dt)

    # 6. Run the simulation loop
    for second in range(1, int(total_seconds) + 1):
        # Sub-step through 1 full second worth of tiny physics increments
        for _ in range(steps_per_second):
            space.update(dt)
            
        # Print status updates once every real-time second
        print(f"--- Time: {second}.0s ---")
        print(f"Planet: {planet}")
        print(f"Moon:   {moon}")
        
        # Calculate the direct distance between them to verify stable orbit bounds
        distance = (moon.pos - planet.pos).magnitude
        print(f"Distance between them: {distance:.2f} meters\n")

if __name__ == "__main__":
    run_test()
