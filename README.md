# AI-Based Traffic Control System

A Python and Pygame simulation of a four-way road intersection featuring dynamically controlled traffic signals. Vehicles arrive from the north, south, east, and west approaches, while the controller estimates demand from waiting vehicles and dynamically adjusts green-light durations.

> **Note:** This is a rule-based traffic-management prototype simulation. The current implementation does not utilize a trained machine-learning model, computer vision, or live traffic-sensor data.

---

## ✨ Features

* **Four-Way Intersection:** Simultaneously simulates north, south, east, and west traffic approaches.
* **Dynamic Signal Timing:** Green duration scales automatically based on the number of currently waiting vehicles.
* **Opposite-Direction Phases:** North and south are served in tandem, followed by east and west.
* **Vehicle Generation:** Spawns vehicles at random intervals with varied speeds, colors, and movement behaviors.
* **Basic Vehicle Spacing:** Vehicles monitor the vehicle directly ahead to reduce overlap during approach.
* **Turning Behavior:** Each vehicle is randomly assigned a movement direction:
  * Straight: 70%
  * Left turn: 15%
  * Right turn: 15%
* **Live Visual Dashboard:** Displays per-lane vehicle counts, waiting counts, current signal states, assigned green time, and the active phase.
* **Quick Exit:** Press `Esc` or close the window anytime to exit the simulation.

---

## 🛠️ Tech Stack & Requirements

* **Language:** Python 3.8 or newer
* **Graphics & Animation:** [Pygame](https://www.pygame.org/) (Version `2.5.2` recommended)
* **Concurrency:** Python built-in `threading` and `time` modules for the signal-control loop
* **Environment:** A desktop environment with graphical display support (headless environments do not support Pygame windows).

---

## 📂 Project Structure

```text
AI-Based-Traffic-Control-System/
├── main.py                  # Application entry point
├── simulation.py            # Pygame window, intersection, spawning, updates, and UI
├── traffic_controller.py    # Demand calculation and signal-phase scheduling
├── traffic_signal.py        # Traffic-light state, timer, and drawing
├── vehicle.py               # Vehicle movement, turning behavior, and rendering
├── requirements.txt         # Python dependency list
└── README.md                # Project documentation
```

---

## 🚀 Setup and Run

### 1. Extract the Project
Extract the project archive and open your terminal inside the root project directory (where `main.py` is located).

### 2. Create a Virtual Environment (Recommended)
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Start the Simulation
```bash
python main.py
```
A window titled **AI-Based Traffic Management System** will launch. Press **Esc** or close the window to exit.

---

## 💡 How It Works

### Simulation Loop (`main.py` & `simulation.py`)
`main.py` initializes a `Simulation` instance with a 1200 × 800 window and enters the main game loop targeting 60 frames per second. `simulation.py` handles intersection rendering, lane setup, vehicle spawning, position updates, and UI statistics overlays.

### Vehicle Movement (`vehicle.py`)
Each vehicle tracks its lane, position, speed, color, and turn direction. Vehicles move along their approach, check spacing relative to the vehicle ahead, and are automatically removed once they exit the screen boundaries.

### Signal Control (`traffic_controller.py`)
A daemon thread executes the signal control loop, alternating between two primary phases:
1. **North + South**
2. **East + West**

The controller counts waiting vehicles for opposing pairs, calculates a dynamic green duration, and switches active signals while managing yellow transition states. 

| Setting | Value |
| :--- | ---: |
| **Minimum green time** | 15 seconds |
| **Maximum green time** | 45 seconds |
| **Yellow transition** | 2 seconds |

---

## 📊 On-Screen Statistics Dashboard

The live dashboard displays key metrics for each direction:
* **Vehicles:** Total vehicles currently tracked in the lane.
* **Waiting:** Vehicles flagged as stopped by movement logic.
* **Signal:** Current traffic-light state (`RED`, `YELLOW`, or `GREEN`).
* **Green Time:** Assigned green duration and approximate remaining countdown while green.
* **Active Lane:** The currently selected direction pair.

---

## ⚙️ Configuration Options

You can customize simulation parameters directly in the source files:
* **Window Size:** Modify `Simulation(width=1200, height=800)` in `main.py`.
* **Frame Rate:** Adjust `self.fps = 60` in `simulation.py`.
* **Spawn Rate:** Tweak `self.spawn_interval = 1.5` and `self.spawn_probability = 0.7`.
* **Vehicle Speed:** Range between `1.5` and `3` in `vehicle.py`.
* **Signal Timings:** Modify `min_green_time`, `max_green_time`, and `yellow_time` in `traffic_controller.py`.

---

## ⚠️ Limitations

* **Rule-Based Prototype:** The controller relies on heuristics rather than a trained machine-learning model or live camera feeds.
* **Demand Estimation:** Traffic demand is estimated via internal `stopped` flags rather than physical sensors.
* **Simplified Physics:** Intersection flow, turning paths, collision handling, and right-of-way rules are simplified for demonstration.
* **Strict Pairing:** Opposite approaches are always served as a pair; independent lane scheduling or pedestrian phases are not included.

---

## 🔍 Troubleshooting

* **`ModuleNotFoundError: No module named 'pygame'`:** Ensure your virtual environment is activated and run `python -m pip install -r requirements.txt`.
* **Window Fails to Open:** Run the script in a desktop session with graphical display support. Headless servers cannot render Pygame windows.
* **`python` Command Not Found:** Try running `python3 main.py` depending on your OS configuration.
* **Simulation Closes Immediately:** Run the script from a terminal window to inspect any runtime error traces.

---

## 🔮 Possible Improvements

* Add a configuration settings panel or command-line arguments for easy parameter tuning.
* Implement performance metrics recording (throughput, average wait time, queue lengths).
* Compare dynamic signal policies against a fixed-time baseline.
* Enhance turning paths, multi-lane geometry, and collision management.
* Integrate and evaluate a genuine machine-learning or reinforcement-learning model.