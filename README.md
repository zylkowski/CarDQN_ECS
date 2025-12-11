<p align="center">
  <img src="vid/demo.gif" height="460">
</p>

# CarDQN

CarDQN is a reinforcement-learning project where a car learns to drive inside a custom-built environment using Q-learning with a neural-network approximation (DQN).  
The entire simulation — including physics, rendering, and the level editor — is implemented using an **Entity Component System (ECS)** architecture for modularity and performance.

This repository includes:
- A level editor for designing custom tracks  
- A PyTorch Q-learning agent  
- A full training & visualization loop  
- An ECS-based game/simulation engine

---

## Q-Learning Overview

### Q-Learning
Q-learning learns a function **Q(s, a)** that estimates the expected cumulative reward of taking action **a** in state **s**.  
In this project, a neural network approximates Q, which turns the algorithm into **Deep Q-Learning (DQN)**.

The core update rule:
```
Q(s, a) ← r + γ * maxₐ' Q(s', a')
```

Where:
- **s** – current state (sensor values, velocity, etc.)
- **a** – chosen action (steer, accelerate)
- **r** – reward received after the action
- **s'** – next state
- **γ (gamma)** – discount factor for future rewards

---

### Reward Function
The reward function guides the car toward safe, stable driving. Typical components include:

- **Positive reward** for reaching checkpoints
- **Negative reward** for wall collisions

The exact reward shaping lives inside the environment code and can be modified freely.

---

### Gamma (γ)
The discount factor **gamma** determines how far into the future the agent looks.

- **γ → 1.0** → long-term planning  
- **γ → 0.0** → short-term, greedy behavior  

Driving tasks usually perform well with values in the **0.80–0.99** range.

---

### Epsilon (ε)
Epsilon controls exploration in the ε-greedy strategy:

- With probability **ε** → take a random action  
- With probability **1 − ε** → take the best predicted action  

Typical setup:
- Start close to **1.0** (full exploration)
- Decay toward a small value like for exploitation

---

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
python src/main.py
```

2. Hit `F3` key to start learning or `F2` for level editor
