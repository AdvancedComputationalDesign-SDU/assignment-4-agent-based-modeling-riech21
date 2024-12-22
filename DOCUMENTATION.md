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

*(Provide a concise explanation of your code, focusing on how you implemented OOP principles and agent-based modeling. Discuss how your approach generates the final structural patterns and the mathematical or computational principles involved.)*

### Topics to Cover:

- **Object-Oriented Design**

  - Explain the classes you designed and why.
  - Discuss how you applied OOP principles like encapsulation, inheritance, and polymorphism.
  - Describe how the classes interact within the simulation.

- **Agent Behaviors and Interactions**

  - Describe the rules governing agent behaviors.
  - Explain how agents interact with each other and the environment.
  - Discuss any algorithms or decision-making processes implemented.

- **Simulation Loop**

  - Explain how the simulation evolves over time.
  - Describe how time-stepping or iteration is handled.
  - Discuss any performance considerations.

- **Visualization**

  - Explain how the agent data is used to generate the final models.
  - Discuss any visualization techniques or tools used.

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

*(Discuss any challenges you faced during the assignment and how you overcame them.)*

### Examples:

- **Challenge 1**: Managing large numbers of agents efficiently.
  - **Solution**: Implemented spatial partitioning to reduce computation time.

- **Challenge 2**: Agents getting stuck or clustering unnaturally.
  - **Solution**: Adjusted interaction rules and added collision avoidance behaviors.

- **Challenge 3**: Visualizing the simulation in real-time.
  - **Solution**: Used efficient data structures and optimized rendering techniques.

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