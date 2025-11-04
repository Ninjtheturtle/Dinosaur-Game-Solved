# Chrome Dinosaur Game with NEAT AI

A reinforcement learning implementation of the Chrome Dinosaur Game using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to play the game through evolutionary neural networks.

## Overview

This project implements an autonomous agent that learns to play the Chrome Dinosaur Game using neuroevolution. Instead of traditional reinforcement learning methods like Q-learning or policy gradients, this implementation uses NEAT to evolve neural network topologies that control the dinosaur's actions.

## NEAT Framework

NEAT (NeuroEvolution of Augmenting Topologies) is a genetic algorithm that evolves both the weights and structure of neural networks. Key features include:

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

## Implementation Details

### Evolutionary Process

1. **Population**: 50 dinosaurs per generation
2. **Fitness Function**: Distance traveled divided by 50
3. **Genome Evaluation**: Each genome controls one dinosaur
4. **Selection**: Top performers reproduce with mutation and crossover
5. **Termination**: Generation ends when all dinosaurs die or 60 seconds elapse

### Physics and Game Mechanics

- **Jump Velocity**: 8.5 units, decreases by 0.8 per frame (gravity)
- **Ground Level**: Y = 310 pixels
- **Jump Prevention**: Actions cannot interrupt mid-air jumps
- **Collision Detection**: Pixel-perfect rect collision with obstacles
- **Progressive Difficulty**: Game speed increases every 100 points

### Key Modifications from Manual Play

- Removed keyboard input system
- Implemented AI action selection (run, jump, duck)
- Added sensor data collection for neural network input
- Integrated fitness calculation based on survival time
- Consolidated update logic to prevent state conflicts

## Installation

### Requirements
```bash
pip install pygame neat-python
```

### Files
- `main.py`: Main game loop and NEAT integration
- `config.txt`: NEAT algorithm configuration parameters

## Running the Simulation

```bash
python main.py
```

The simulation will display:
- Current generation number
- Number of dinosaurs still alive
- Current score
- All active dinosaurs on screen simultaneously

## NEAT Configuration

Key parameters in `config.txt`:

- **Population Size**: 50 genomes per generation
- **Fitness Threshold**: 100,000 (effectively unlimited)
- **Mutation Rates**:
  - Weight mutation: 0.8
  - Bias mutation: 0.7
  - Add connection: 0.5
  - Add node: 0.2
- **Compatibility Threshold**: 3.0 for speciation
- **Elitism**: Top 3 genomes always survive

## Training Observations

- Early generations: Random jumping, immediate collisions
- Mid generations: Basic obstacle avoidance emerges
- Late generations: Timing improvements, strategic ducking
- Typical convergence: 50-200 generations for competent play

## Architecture Comparison

This implementation follows the same pattern as NEAT car simulations:

**Similarities:**
- Population-based evaluation
- Radar-like distance sensing
- Fitness based on survival metrics
- Real-time visualization of all agents

**Differences:**
- Discrete actions (run/jump/duck) vs continuous steering
- 2D vertical movement vs 2D track navigation
- Simpler input space (7 vs 5 sensors)
- Time-limited generations (60s maximum)

## Technical Details

### Jump Mechanics Fix

The implementation includes critical fixes for jump physics:
- Position-based landing detection (Y >= 310) instead of velocity-based
- Guard clauses preventing action state changes during jumps
- Visual update ordering to prevent teleporting artifacts
- Dual-layer ground collision enforcement

### Multi-Generation Support

Each generation receives a fresh pygame environment to prevent state pollution between generations. The `run_simulation` function reinitializes pygame and creates a new screen for each evolutionary cycle.

## Project Structure

```
chrome-dinosaur-master/
├── main.py              # NEAT implementation and game logic
├── config.txt           # NEAT configuration parameters
├── Assets/              # Game sprites and images
│   ├── Dino/           # Dinosaur animations
│   ├── Cactus/         # Obstacle sprites
│   ├── Bird/           # Flying obstacle sprites
│   └── Other/          # Background and cloud assets
└── car_sim/            # Reference NEAT implementation
```

## References

- NEAT Paper: Stanley & Miikkulainen (2002)
- NEAT-Python Library: https://neat-python.readthedocs.io/
- Original Game: Chrome Browser offline game
