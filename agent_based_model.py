"""
Assignment 4: Agent-Based Model for wind simulation

Author: Rie Pilgaard Christiansen

Description:
This script simulates wind particles interacting with a facade in a bounded environment using OOP. 
Particles move, interact with obstacles, and are attracted to a target point, creating trails that form emergent patterns. 
Outputs include particle positions, facade geometry, bounding box, target point, and trails.

Note: This script is intended to be used within Grasshopper's Python scripting component.
"""

# Import necessary libraries
import Rhino.Geometry as rg
import random

# Set a random seed for reproducibility
random.seed(42)

# Check if the environment exists and the restart flag is False
if 'env' not in globals() or restart:
    # Class representing a wind particle
    class WindParticle:
        def __init__(self, position, velocity, interaction_range=2.0, attraction_strength=0.05):
            """
            Initialize a wind particle with position, velocity, interaction range, and attraction strength.

            Args:
            position: Tuple of initial coordinates (x, y, z).
            velocity: Tuple of initial velocity components (vx, vy, vz).
            interaction_range: Range for interaction with the facade.
            attraction_strength: Strength of attraction to the target point.
            """
            self.position = rg.Point3d(*position)  # Initialize position
            self.velocity = rg.Vector3d(*velocity)  # Initialize velocity
            self.interaction_range = interaction_range  # Range for facade interaction
            self.attraction_strength = attraction_strength  # Attraction strength to the target
            self.trail = [rg.Point3d(*position)]  # Initialize trail with the starting position

        def move(self):
            """Move the particle based on its velocity and update its trail."""
            self.position += self.velocity
            self.trail.append(rg.Point3d(self.position))
            if self.velocity.X < 0:
                self.velocity.X = 0.1  # Ensure positive X movement

        def interact(self, facade):
            """
            Interact with the facade to prevent the particle from crossing it.

            Args:
            facade: An instance of the Facade class.
            """
            closest = facade.closest_point(self.position)
            distance_to_facade = self.position.DistanceTo(closest)

            if distance_to_facade < self.interaction_range:
                # Compute a direction away from the facade
                direction_away = self.position - closest
                direction_away.Unitize()

                # Push the particle away based on the distance
                push_strength = (self.interaction_range - distance_to_facade) * 0.5
                self.position += direction_away * push_strength

                # Calculate a tangent vector for movement around the facade
                tangent = rg.Vector3d(-direction_away.Y, direction_away.X, 0)
                tangent.Unitize()
                self.velocity = (tangent * self.velocity.Length) + (direction_away * 0.1)

                # Ensure positive X velocity
                if self.velocity.X < 0:
                    self.velocity.X = 0.1

        def attract_to_target(self, target):
            """
            Attract the particle toward a target point.

            Args:
            target: The target point as an rg.Point3d object.
            """
            direction_to_target = target - self.position
            direction_to_target.Unitize()

            # Balance attraction with current direction
            self.velocity = (self.velocity * 0.9) + (direction_to_target * self.attraction_strength)

            # Ensure positive X velocity
            if self.velocity.X < 0:
                self.velocity.X = 0.1

        def get_trail_curve(self):
            """Return the particle's trail as a polyline curve."""
            return rg.PolylineCurve(self.trail)

    # Class representing the facade
    class Facade:
        def __init__(self, base_point, width, height):
            """
            Initialize a rectangular facade.

            Args:
            base_point: The bottom-left corner of the rectangle.
            width: The width of the facade.
            height: The height of the facade.
            """
            self.base_point = base_point
            self.width = width
            self.height = height
            self.plane = rg.Plane(base_point, rg.Vector3d.ZAxis)
            self.geometry = rg.Rectangle3d(self.plane, width, height)

        def closest_point(self, point):
            """
            Find the closest point on the facade to a given point.

            Args:
            point: The point to check against the facade.

            Returns:
            Closest point on the facade as an rg.Point3d object.
            """
            facade_x = min(max(point.X, self.base_point.X), self.base_point.X + self.width)
            facade_y = min(max(point.Y, self.base_point.Y), self.base_point.Y + self.height)
            return rg.Point3d(facade_x, facade_y, self.base_point.Z)

    # Class for the environment
    class Environment:
        def __init__(self, bounds, num_particles):
            """
            Initialize the environment with a bounding box, particles, and a facade.

            Args:
            bounds: Bounding box defining the simulation area.
            num_particles: Number of particles to generate.
            """
            self.bounds = bounds
            self.facade = Facade(rg.Point3d(-5, -5, 0), 15, 10)
            self.particles = self.generate_particles(num_particles)
            self.attraction_target = rg.Point3d(bounds.Max.X, (bounds.Max.Y + bounds.Min.Y) / 2, 0)

        def generate_particles(self, num_particles):
            """
            Generate particles with random starting positions and uniform velocity.

            Args:
            num_particles: Number of particles to generate.

            Returns:
            A list of WindParticle objects.
            """
            particles = []
            for _ in range(num_particles):
                start_pos = rg.Point3d(
                    self.bounds.Min.X - 5,
                    random.uniform(self.bounds.Min.Y, self.bounds.Max.Y),
                    0
                )
                velocity = [0.3, 0, 0]
                particles.append(WindParticle(start_pos, velocity))
            return particles

        def update(self):
            """Update the environment by moving and interacting particles."""
            for particle in self.particles:
                particle.move()
                particle.interact(self.facade)
                particle.attract_to_target(self.attraction_target)
                self.clamp_particle_position(particle)

        def clamp_particle_position(self, particle):
            """
            Clamp the particle's position within the bounding box.

            Args:
            particle: An instance of WindParticle.
            """
            particle.position.X = max(self.bounds.Min.X, min(particle.position.X, self.bounds.Max.X))
            particle.position.Y = max(self.bounds.Min.Y, min(particle.position.Y, self.bounds.Max.Y))

    # Define a bounding box
    bounding_box = rg.BoundingBox(rg.Point3d(-30, -20, -5), rg.Point3d(30, 20, 5))

    # Initialize the environment with user-defined number of particles
    env = Environment(bounds=bounding_box, num_particles=num_particles)

# Update the environment for the next frame
env.update()

# Grasshopper outputs
particles = [particle.position for particle in env.particles]  # Particle positions
facade = env.facade.geometry  # Facade geometry
bounds = env.bounds  # Bounding box
target_point = env.attraction_target  # Target point for particles
agent_trails = [particle.get_trail_curve() for particle in env.particles]  # Trails as curves