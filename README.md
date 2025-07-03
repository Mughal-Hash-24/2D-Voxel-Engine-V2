# 🌍 2D Voxel Engine V2 – Infinite Terrain, Enemies & Combat

**Created:** Late 2023  
**Language:** Python (Pygame)  
**Developer:** Ibtasaam Amjad  
**Episode 8 of the Series:** *Lines of Code, Chapters of Me*

---

## 📜 Overview

In this project, I expanded upon my previous voxel engine, evolving it into a procedurally generated 2D world complete with infinite terrain, perlin noise-based generation, real-time enemy AI, boss mechanics, and directional combat.  

Inspired by the foundational sandbox elements of *Minecraft* and driven by a passion for creating dynamic environments, this project represented a major technical and creative leap from static tiles to living systems.

---

## ✨ Key Features

### 🌍 World Generation
- **Perlin Noise-Based Terrain:**  
  Procedural 2D tile generation using `perlin_noise` for natural elevation variation.
- **Chunk Loading System:**  
  Optimized world streaming using chunk-based generation (`8x8` blocks per chunk).
- **Block Types:**  
  Grass, dirt, and plant layers determined by elevation thresholds.

---

### 🕹️ Core Mechanics
- **Infinite Side-Scrolling:**  
  The world scrolls seamlessly as the player moves, loading new chunks as needed.
- **Smooth Camera Tracking:**  
  Camera scrolls smoothly using interpolation to follow the player.

---

### 🧱 Gameplay Systems
- **Block Interaction:**  
  Place and break tiles within the environment (extensible via the `engine.py` module).
- **Enemy AI:**  
  Enemy entities spawn and navigate terrain, follow the player, and attack on contact.
- **Boss Entity:**  
  Bosses are spawned after achieving certain kill thresholds, with unique behavior, speed, and HP.

---

### 🔥 Combat & Effects
- **Player Attacks:**  
  Mouse click-based melee attack with cooldown, animation, and knockback physics.
- **Projectile System:**  
  Directional fireballs launched by right-clicking; collisions remove the entity.
- **Entity Animation:**  
  Entities feature state-based animations (`idle`, `run`, `attack`) with directional flipping.

---

### 🎧 Sound & Visuals
- **Sound Effects:**  
  - Jump sounds
  - Ambient music
  - Kill sounds
  - Footstep variations
- **Custom Sprites:**  
  Entity sprite sheets and terrain textures loaded via custom animation system.

---

## ▶️ How to Run

1. **Install Dependencies:**
   ```bash
   pip install pygame perlin_noise
   ```

2. **Ensure the following project structure:**
   ```
   ├── main.py
   ├── data/
       ├── engine.py
       ├── images/
       │   ├── player.png
       │   ├── enemy.png
       │   ├── boss.png
       │   ├── grass.png
       │   ├── dirt.png
       │   └── ...
       └── audio/
           ├── jump.wav
           ├── music.wav
           ├── kill_sound.mp3
           └── grass_0.wav
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

---

## ⚙️ Controls

| Action             | Key/Mouse         |
|--------------------|------------------|
| Move Left/Right    | `←` / `→`         |
| Jump               | `↑`              |
| Attack             | `Left Click`     |
| Fireball           | `Right Click`    |

---

## 🧠 What This Project Showcased

- Modular chunk-based world generation  
- Perlin noise terrain shaping  
- Custom animation systems for sprite-based entities  
- Real-time enemy movement, AI behavior, and attack logic  
- Health and collision systems for combat mechanics  
- Sound design integration with visual feedback  
- Scaled rendering surface with camera smoothing

---

## 📦 External Modules

- `perlin_noise` for terrain randomness  
- Custom `engine.py` system for handling entities, animation, movement, and collision

---

## 🧱 Status

This version served as a major turning point in the developer’s progression — blending creative freedom with technical structure. It laid the foundation for future developments like inventory systems, crafting, or fully interactive voxel environments.

---

## 🗺️ Episode Context

This was **Episode 8** in the *Lines of Code, Chapters of Me* series — and a sequel to **Episode 7: I Made the Ground I Walked On**.

In this chapter, the ground wasn’t just created.  
It stretched endlessly.  
And it **fought back.**

---
