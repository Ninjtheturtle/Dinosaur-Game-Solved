# Chrome Dinosaur Game with NEAT AI

A reinforcement learning implementation of the Chrome Dinosaur Game using the NEAT (NeuroEvolution of Augmating Topologies) algorithm. The AI learns to play the game through evolutionary neural networks.

## NEAT Framework

NEAT is a genetic algorithm that evolves both the weights and structure of neural networks. Key features include:

- **Topology Evolution**: Networks start simple and complexify over generations
- **Speciation**: Protects innovation by grouping similar network structures
- **Historical Markings**: Enables crossover between different topologies
- **Fitness-Based Selection**: Better performing networks are more likely to reproduce

### Network Architecture

**Input Layer (7 nodes):**
- Dinosaur Y position
- Dinosaur ducking state (binary)
- Nearest obstacle X position
- Nearest obstacle Y position
- Nearest obstacle width
- Current game speed
- Next obstacle X position

**Hidden Layer:**
- Initially 0 nodes, evolved during training
- Uses tanh activation function

**Output Layer (3 nodes):**
- Action 0: Run
- Action 1: Jump
- Action 2: Duck

The network outputs are evaluated, and the action with the highest activation is selected.

## Implementation

### Evolutionary Process

- **Population**: 50 dinosaurs per generation
- **Fitness Function**: Distance traveled divided by 50
- **Selection**: Top performers reproduce with mutation and crossover
- **Termination**: Generation ends when all dinosaurs die or 60 seconds elapse

### Game Mechanics

- **Jump Velocity**: 8.5 units, decreases by 0.8 per frame (gravity)
- **Ground Level**: Y = 310 pixels
- **Collision Detection**: Pixel-perfect rect collision with obstacles
- **Progressive Difficulty**: Game speed increases every 100 points
- **Jump Behavior**: Actions cannot interrupt mid-air jumps

## NEAT Configuration

Key parameters in `config.txt`:

- **Population Size**: 50 genomes per generation
- **Fitness Threshold**: 100,000 (effectively unlimited)
- **Mutation Rates**: Weight (0.8), Bias (0.7), Add connection (0.5), Add node (0.2)
- **Compatibility Threshold**: 3.0 for speciation
- **Elitism**: Top 3 genomes always survive

## Installation

### Requirements
```bash
pip install pygame neat-python
```

### Running the Simulation

```bash
python main.py
```

The simulation displays:
- Current generation number
- Number of dinosaurs still alive
- Current score
- All active dinosaurs on screen simultaneously

## Training Progression

- **Early generations**: Random jumping, immediate collisions
- **Mid generations**: Basic obstacle avoidance emerges
- **Late generations**: Timing improvements, strategic ducking
- **Typical convergence**: 50-200 generations for competent play

## Technical Notes

### Jump Mechanics

The implementation uses position-based landing detection (Y >= 310) rather than velocity-based detection. This ensures smooth jump arcs without teleporting artifacts. Actions are prevented from interrupting jumps mid-flight through guard clauses.

### Multi-Generation Support

Each generation receives a fresh pygame environment to prevent state pollution. The `run_simulation` function reinitializes pygame and creates a new screen for each evolutionary cycle.

## References

- NEAT Paper: Stanley & Miikkulainen (2002)
- NEAT-Python Library: https://neat-python.readthedocs.io/
- Original Game: Chrome Browser offline game
