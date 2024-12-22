# Assignment 4: Agent-Based Model Documentation

## Table of Contents

- [Pseudo-Code](#pseudo-code)
- [Technical Explanation](#technical-explanation)
- [Design Variations](#design-variations)
- [Challenges and Solutions](#challenges-and-solutions)
- [References](#references)

---

## Pseudo-Code

1. **Class: `windparticle`**
- Represents a single particle.
- **Attributes**
  - `position`: Current position of the particle.
  - `velocity`: Current velocity vector.
  - `interaction_range`: Distance within which the particle interacts with the facade.
  - `attraction_strength`: Magnitude of attraction to the target point.
  - `trail`: List storing the particle's path.
- **Methods**
  - `move()`
    - Update `position` by adding `velocity`.
    - Append the updated `position` to the `trail`.
    - Ensure `velocity.X` remains positive.
  - `interact(facade)`
    - Find the closest point on the facade to the particle.
    - If within `interaction_range`, adjust `position` to push away from the facade.
    - Update `velocity` to smooth movement around the facade.
  - `attract_to_target(target)`
    - Calculate direction to the `target` point.
    - Adjust `velocity` to balance current direction and attraction.
    - Ensure `velocity.X` remains positive.
  - `get_trail_curve()`
    - Return `trail` as a curve object.
2. **Class: `Facade`**
- Represents a rectangular obstacle.
- **Attributes**
  - `base_point`: Bottom-left corner of the facade.
  - `width`, `height`: Dimensions of the facade.
  - `geometry`: Geometric representation of the facade.
- **Methods**
  - `closest_point(point)`
    - Calculate the closest point on the facade to the given `point`.
3. **Class: `Environment`**
- Simulates the interaction of particles within a bounded area.
- **Attributes**
  - `bounds`: Bounding box for the simulation.
  - `facade`: A single `Facade` object.
  - `particles`: List of `WindParticle` objects.
  - `attraction_target`: Target point for particle attraction.
- **Methods**
  - `generate_particles(num_particles)`
    - Create `num_particles` with random positions and uniform velocities.
    - Return the list of particles.
  - `update()`
    - For each particle
      - Call `move()`.
      - Call `interact(facade)`.
      - Call `attract_to_target(attraction_target)`.
      - Clamp the particle's position within `bounds`.
  - `clamp_particle_position(particle)`
    - Restrict the particle’s position to stay within the `bounds`.

**Initialization and Execution**
1. **Environment Setup**
- Define `bounding_box` to set simulation limits.
- Initialize a `Facade` object with specific dimensions.
- Initialize the `Environment` with
  - `bounding_box`.
  - Specified `num_particles`.
2. **Simulation Update Loop**
- Call `env.update()` to
  - Move particles.
  - Handle interactions with the facade.
  - Attract particles to the target point.
3. **Outputs**
- Particle positions.
- Facade geometry.
- Bounding box.
- Target point.
- Particle trails as curves.

---

## Technical Explanation

**Object-Oriented Design** The simulation is structured using three main classes: `WindParticle`, `Facade`, and `Environment`.

The `WindParticle` class models individual particles, encapsulating attributes such as position, velocity, interaction range, and attraction strength. Each particle manages its own behavior through methods for movement, obstacle interaction, and target attraction.

The `Facade` class represents a rectangular obstacle, encapsulating geometric properties and methods to find the closest point to a given particle, essential for managing spatial relationships.

The `Environment` class oversees the simulation, defining the bounding area, generating particles, and updating their states. It coordinates interactions between particles and the facade while enforcing constraints to keep particles within defined bounds.

Key OOP principles include encapsulation, as each class encapsulates specific responsibilities, and interaction through well-defined interfaces, such as the `WindParticle` class calling the `Facade.closest_point()` method for interactions.

**Agent Behaviors and Interactions** Agent behaviors are governed by rules that dictate how particles move and interact with the environment. Each particle moves according to its velocity and adjusts its position when near the facade to avoid collisions. Additionally, particles are attracted to a predefined target point, using directional vectors to guide their movement.

When approaching the facade, particles detect proximity using geometric calculations to find the closest point and apply a repulsive force to avoid crossing the boundary. Simultaneously, they calculate direction vectors toward the target and adjust their velocities accordingly.

The decision-making processes include collision avoidance and target attraction, where particles’ velocities gradually align with the target direction through vector normalization and scaling.

**Simulation Loop** The simulation evolves through iterative updates, with each iteration calling the `update()` method in the `Environment` class to manage all particles. Each particle calls its movement, interaction, and attraction methods to simulate dynamic behavior.

Time-stepping is achieved by repeatedly invoking the `update()` method, allowing the simulation to progress frame by frame. Performance considerations ensure efficiency by limiting interactions to only necessary calculations, with a fixed number of particles and simple geometric operations.

**Visualization** The data generated by the agents is visualized through trails, which are stored as series of points and converted into curves. The geometry of the facade and particle positions are also output for real-time display.

A trigger mechanism is employed to initiate the simulation, allowing for controlled visualization of particle dynamics. Visualization techniques utilize Rhino.Geometry to represent the 3D positions of particles, facade, and trails. Final outputs include particle positions, facade geometry, bounding box dimensions, the target point for attraction, and particle trails.

---

## Design Variations

*(Include images and descriptions of your generated design variations. For each variation, discuss the parameters or rules changed and the impact on the resulting patterns.)*

### Variation Examples

1. **Variation 1: [Name/Description]**

   ![Variation 1](images/variation1.jpg)

   - **Parameters Changed**:
     - interaction_radius: [Value]
     - alignment_strength: [Value]
   - **Description**:
     - Describe how these changes affected agent behaviors and the final pattern.

2. **Variation 2: [Name/Description]**

   ![Variation 2](images/variation2.jpg)

   - **Parameters Changed**:
     - cohesion_factor: [Value]
     - separation_distance: [Value]
   - **Description**:
     - Discuss the observed changes in the model.

3. **Variation 3: [Name/Description]**

   ![Variation 3](images/variation3.jpg)

   - **Parameters Changed**:
     - randomness: [Value]
     - environmental_influence: [Value]
   - **Description**:
     - Explain how the introduction of randomness or environmental factors impacted the results.

*(Add more variations as needed.)*

---

## Challenges and Solutions

- **Challenge**: Balancing Avoidance and Attraction. 
  - **Solution**: I fine-tuned the attraction and repulsion forces to balance navigation around the facade while progressing toward the target. A blended force algorithm based on distance and velocity allowed particles to dynamically adapt without getting stuck.

- **Challenge**: Agents getting stuck or clustering unnaturally.
  - **Solution**: I implemented a mechanism that modified particle velocities when they were too close to the facade, allowing them to move away more effectively. Additionally, I introduced a random perturbation factor in their movement to encourage exploration and reduce clustering.

- **Challenge**: Visualizing the simulation in real-time.
  - **Solution**: I used spatial partitioning to reduce calculations for particle-facade interactions, enhancing simulation responsiveness. Optimizing the rendering pipeline ensured only essential elements were drawn, improving real-time visualization.

- **Challenge**: Handling Edge Cases in Particle Movement.
  - **Solution**: I added boundary clamping logic in the `clamp_particle_position()` method to keep particles within bounds, ensuring smoother movement and reducing erratic behavior.

- **Challenge**: Issues with Bounding Box Constraints.
  - **Solution**: I refined the bounding box logic by enforcing consistent clamping of particle positions and re-evaluating the conditions for boundary checks. Debug outputs were added to monitor particle positions, enabling quick identification and correction of boundary issues.

- **Challenge**: Reuniting Particles After Avoiding the Facade.
  - **Solution**: I implemented a "reorientation" mechanism to adjust particle trajectories after avoiding the facade. This recalibrated their velocity toward the target, ensuring a smooth return to their path and improving overall flow in the simulation.

---

## References

*(List any resources you used or found helpful during the assignment.)*

- **Object-Oriented Programming**

  - [Python Official Documentation](https://docs.python.org/3/tutorial/classes.html)
  - [Real Python - OOP in Python](https://realpython.com/python3-object-oriented-programming/)

- **Agent-Based Modeling**

  - [Mesa: Agent-Based Modeling in Python](https://mesa.readthedocs.io/en/master/)
  - [Agent-Based Models in Architecture](https://www.researchgate.net/publication/279218265_Agent-based_models_in_architecture_new_possibilities_of_interscalar_design)

- **Visualization Tools**

  - [Rhino.Python Guides](https://developer.rhino3d.com/guides/rhinopython/)
  - [matplotlib](https://matplotlib.org/)
  - [Blender Python API](https://docs.blender.org/api/current/)

---

*(Feel free to expand upon these sections to fully capture your work and learning process.)*

---