## Pixelated Perry
A 2D pixel-art platformer built in Python using Pygame. Make your way through increasingly challenging levels and defeat enemies along the way.

### 📸 Screenshots
- Placeholder

### 🚀 Features
- Platform Mechanics (run, jump, wall-slide/jump, dash attack)
- Sprite-based animation system
- Enemy AI
- Multiple levels with enemy spawns and goal points
- Visual Effects (Projectiles, Level Transitions, Screenshake)
- Start and End Screens

## 🕹️ Run the Game

### Requirements
- Python 3.8+

### Installation Instructions
```
git clone https://github.com/AmanvirSamra/2D-cyberpunk-platformer.git
cd 2D-cyberpunk-platformer
python pip install -r requirements.text
```

### Start the game
```
python .\game.py
```

## 🎮 Controls

| Key      | Action                |
|----------|-----------------------|
| ← / →    | Move left / right     |
| ↑        | Jump                  |
| X        | Dash Attack           |
| R        | Restart (end screen)  |
| Any key  | Start game            |

## 📁 Project Structure
```
pixelated-perry/
├── main.py # Main game loop
├── scripts/
│ ├── entities.py # Player, Enemy Classes
│ ├── tilemap.py # Tilemap handling
│ └── utils.py # Helpers for loading images/animations and levels
├── data/
| └── maps/ # Level map JSON files
| └── images/
|    ├── tiles/ # Tile images
│    ├── entities/ # Player and enemy sprite sheets
│    ├── background/ # Background images
│    └── particles/ # Projectile assets
└── README.md # This file
```

## Future Improvements
- Sound effects and music (In Progress)
- Map Builder (Partially completed (See below))
- More Enemy types and behaviours
- Heath System
- Gamepad & Voice Support

## Acknowledgments
- [Chroma-Dave](https://chroma-dave.itch.io/neon-city-pixel-art-pack-main-character-1) - For player and enemy sprites
- [CraftPix](https://craftpix.net/) - For Tile and background images
- [Pygame Community](https://www.pygame.org/) - For helpful documentation and tools
