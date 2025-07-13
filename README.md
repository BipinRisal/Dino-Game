Dino Game Documentation

Overview
This is a 2D endless runner game inspired by the Chrome offline Dino game. The player controls a dinosaur that runs, ducks, and jumps to avoid obstacles (cacti and birds). The game records high scores and death counts using an SQLite leaderboard database and features sound effects and animations.

Project Structure
- Audio files: stored in audio/ folder (jump.mp3, die.mp3, point.mp3)
- Images: stored in images/ folder (Dino sprites, cacti, bird, cloud, track, game over screen, reset button)
- SQLite DB: leaderboard.db created/updated automatically

Main Modules and Classes

1. Database Functions
- init_db():
  Creates SQLite database file leaderboard.db and table leaderboard if not exists.
  Table columns: id (primary key), name (text), score (integer)

- save_score_sqlite(name, score):
  Saves a player's name and their score into the leaderboard table.

- load_leaderboard_sqlite(limit=5):
  Loads top limit scores from the leaderboard ordered by score descending.

2. Dinosaur Class
Represents the player-controlled dinosaur.

- Attributes:
  - Position constants for standing and ducking
  - Jump velocity and jump physics variables
  - Sprite images for running, ducking, jumping, and dead states
  - Collision rectangle (dino_rect)

- Methods:
  - update(userInput): Updates dino state (run, duck, jump) based on keyboard input
  - duck(), run(), jump(): Handles animation and physics for each state
  - dead(): Triggers dead animation and stops movement
  - draw(SCREEN): Draws current sprite on screen

3. Cloud Class
Background cloud that moves across the screen.

- Attributes: position, image, width
- Methods:
  - update(): Moves cloud leftwards with game speed, resets position if off screen
  - draw(SCREEN): Draws cloud sprite on screen

4. Obstacle Classes
Base class and subclasses for different obstacles:

- Obstacle (base):
  Holds image, position (rect), and update/draw logic

- SmallCactus and LargeCactus:
  Randomly selects cactus type and sets vertical position

- Bird:
  Animated bird obstacle with flapping wing animation

5. Game Functions
- main():
  Core game loop
  - Handles player, obstacles, background, score, collisions
  - Updates game speed and points
  - Plays sounds for jumping, scoring, and death
  - Saves score on death and returns to menu

- menu():
  Start and restart menu
  - Allows player name input (only before first game)
  - Shows instructions, death count, high score, and leaderboard
  - Handles quitting and restarting the game

Gameplay Controls
- Up arrow key: Jump
- Down arrow key: Duck
- Escape key or quit button: Exit game
- Up arrow key or reset button (in menu after death): Restart game

Gameplay Features
- Increasing speed as player scores points (every 100 points)
- Sound effects for jump, point milestones, and death
- Animated sprites for dinosaur and bird obstacles
- Leaderboard persists scores across sessions using SQLite
- Death count and high score tracked and displayed
- Cloud background and track scrolling for visual effect

Variables and Constants

| Variable              | Purpose                                    |
|-----------------------|--------------------------------------------|
| player_name           | Stores player’s name                       |
| HIGH_SCORE            | Highest score achieved                     |
| DEATH_COUNT           | Number of times player has died            |
| SCREEN_WIDTH/HEIGHT   | Dimensions of game window                  |
| game_speed            | Controls game scrolling and obstacle speed |
| points                | Player's current score                     |
| obstacles             | List of current obstacles on screen        |

Sound Files
- jump.mp3: Played when the dino jumps
- die.mp3: Played on collision
- point.mp3: Played every 100 points

Notes for Running
- Make sure Pygame is installed (pip install pygame)
- Audio and image folders must be structured exactly as in the code
- The SQLite database file leaderboard.db will be created automatically
- The game runs at 30 FPS
