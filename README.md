# 2D Roguelike Gacha Game

A simple 2D roguelike game built with **Pygame**, featuring:
- Player movement
- Sword swinging and punching attacks
- Enemy spawning and health system
- Gacha system for obtaining new items
- Player leveling and experience system
- Shield mechanics

---

## 📜 How to Run

1. **Install dependencies**  
   Make sure you have [Python](https://www.python.org/) and [Pygame](https://www.pygame.org/) installed:

   ```bash
   pip install pygame
   ```
   
2. **Run the game**

   ```bash
   python holocurek.py
   ```

---

## 🎮 Controls

| Key | Action |
| --- | --- |
| `W/A/S/D` | Move Up/Left/Down/Right |
| `G` | Perform a Gacha pull (costs 10 coins) |
| `SPACE` | Attack (swing sword if available, otherwise punch) |
| `ENTER` | Confirm level up |

---

## 🛡️ Game Features

- **Movement**: Move freely around the 800x600 window.
- **Attacks**:
  - **Sword Attack**: If you have pulled a sword via gacha, you can swing it.
  - **Punch Attack**: If you don't have a sword, you'll punch enemies.
- **Enemy Spawning**: Enemies spawn every few frames.
- **Leveling Up**: Gain experience from defeating enemies. Every level up increases your max health.
- **Gacha System**:
  - Spend coins to pull random items like Sword, Shield, Bow, or Fireball.
  - Shields absorb a portion of damage.
- **Coin Drops**: Enemies drop coins upon defeat.
- **Health and Shield Bars**: Displayed at the top left.
- **Inventory**: Displays your last 3 gacha pulls.

---

## 🤔 Why Pygame?

I chose **Pygame** because I'm still learning and prefer something simple, lightweight, and easy to set up without installing heavy software or full game engines. 

**Pygame** is a great tool for beginners and prototyping because:
- It only requires Python and a simple library installation.
- It allows full control over your game's logic and graphics.
- It's lightweight and fast for 2D game development.
- The documentation and community examples make learning very approachable.

If you're new to making games, **Pygame** is a fantastic place to start!

---

## 📢 Contact

For any questions, suggestions, or collaborations, feel free to reach out:

**Email:** reach.kinghavemine@gmail.com

---

> Made with passion using Python and Pygame ❤️

