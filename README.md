# Q Maze Runner

![Main](/assets/image.png)

A simple 2D maze runner game built with PyGame where players navigate through increasingly difficult mazes while collecting tokens and avoiding obstacles.

![Q Maze Runner Game](assets/images/player.png)

## Features

- **Progressive Difficulty**: Three levels with increasing challenge
- **Token Collection**: Collect tokens to earn points
- **Moving Obstacles**: Avoid moving obstacles that reduce your lives
- **Lives System**: Three hearts that diminish when hitting obstacles
- **Automatic Level Progression**: Seamless transition between levels
- **Score Tracking**: Points for collecting tokens and completing levels
- **Visual Feedback**: Heart display, score counter, and level information

## How to Play

1. **Start the Game**: Run `python3 maze_game.py` to launch the game
2. **Controls**:
   - Arrow keys to move the player
   - ESC to quit the game
   - R to restart after game over
3. **Objective**: Collect all tokens in each level to advance
4. **Scoring**:
   - +10 points for each token collected
   - +10 points for completing a level

## Game Video (Find out what will there in level-3)

[Game Video](https://www.youtube.com/watch?v=cfSYiKgdmf0)

## Requirements

- Python 3.x
- PyGame

## Installation

```bash
# Clone the repository
git clone https://github.com/aquavis12/QCli-Maze-Game

# Navigate to the game directory
cd QCli-Maze-Game

# Install PyGame if you don't have it
pip install pygame

# Run the game
python3 maze_game.py
```

## Game Elements

- **Player**: Green character that you control
- **Walls**: Blue barriers that block movement
- **Tokens**: Gold coins to collect
- **Obstacles**: Red spiky balls that reduce lives
- **Hearts**: Visual representation of remaining lives

## Blog Posts

Read more about the development process and game design:

- [Dev.to Blog Post](https://dev.to/aws-builders/using-amazon-q-cli-pygame-to-build-a-3-level-maze-game-with-hearts-hazards-5an9)
- [Hashnode Article](https://technodiaryvishnu.hashnode.dev/using-amazon-q-cli-and-pygame-to-build-a-3-level-maze-game-with-hearts-and-hazards)

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- PyGame community for the excellent game development library
- Free game assets and inspiration from various open source projects
