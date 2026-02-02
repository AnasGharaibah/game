# Ninja Duel - Cloud9 x JetBrains Booth Mini-Game

## Setup
1. Install dependencies:
   ```bash
   pip install opencv-python ultralytics pygame numpy
   ```
2. Place your custom YOLO model in the root directory and name it `yolov8n.pt` (or update `main.py` with the correct path).
3. Ensure you have a camera connected.

## How to Play
- **Start Game**: Press `SPACE`
- **Player 1 (Left ROI)**: Perform hand signs or use keys `1`, `2`, `3`
- **Player 2 (Right ROI)**: Perform hand signs or use keys `8`, `9`, `0`
- **Restart**: Press `R` after Game Over
- **Exit**: Press `ESC`

## Abilities
- **Fireball**: Sign `tiger` (or key `1`/`8`)
- **Wall**: Sign `snake` (or key `2`/`9`)
- **Heavy Attack**: Sequence `dragon` -> `tiger` (or key `3`/`0`)

## Note
The game uses a time-based stabilizer for hand signs (300ms) and a 1.5s window for combos.
If the custom model is not found, it will default to a standard YOLOv8n model for testing.
