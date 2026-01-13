# 🧠 OS Simulator

A Python-based Operating System (OS) simulation framework designed to model core operating system behaviors such as **CPU scheduling**, **process management**, and other system mechanisms. This project is intended for educational use, experimentation, and algorithm development.

---

## 📑 Table of Contents

- [About](#about)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [Testing](#testing)
- [Requirements](#requirements)


---

## 📖 About

**OS Simulator** is an open-source Python project that simulates core components and algorithms of an operating system. The simulator demonstrates how components like schedulers and process managers function in a controlled environment. It's a valuable tool for students, educators, and developers interested in operating system fundamentals.

---

## ✨ Features

- **Modular Architecture:** Clean, extensible design for OS components
- **CPU Scheduling Simulation:** Model various scheduling algorithms
- **Process Management:** Create, execute, and track process lifecycles
- **Unit Testing:** Comprehensive tests for validating simulator behavior
- **Example Outputs:** Demo materials showing simulator capabilities
- **Educational Focus:** Clear code structure ideal for learning OS concepts

---

## 📁 Repository Structure

```text
.
├── src/                       # Source code for OS simulator modules
├── tests/                     # Unit tests validating simulation behavior
├── Demo.mp4                   # Demonstration of the simulator in action
├── req.txt                    # Python dependency list
└── README.md                  # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/finddawood/os-simulator.git
cd os-simulator
```

### 2. Set Up a Python Environment

Python 3.8 or higher is recommended.

```bash
# Create virtual environment
python3 -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r req.txt
```

---

## 🚀 Usage

Use the modules inside the `src/` folder to initialize and run operating system simulations.

### Basic Example

```python
from src import scheduler, process_manager

# Create and configure your simulation
sim = scheduler.Scheduler(...)
sim.run()
```

### Running a Simulation

```bash
python main.py
```

*(Update the above examples with actual module names and usage from your codebase)*

---

## 🎥 Demo

A demonstration video `Demo.mp4` is included in the repository. You can play it using any standard video player to see the simulator in action.

### View the Demo

```bash
# On macOS
open Demo.mp4

# On Linux
xdg-open Demo.mp4

# On Windows
start Demo.mp4
```

Or simply open the file in your OS file explorer.

---

## 🧪 Testing

To run the test suite and validate simulator components:

```bash
pytest
```

This will execute all unit tests under the `tests/` directory and report any failures.

### Run Tests with Coverage

```bash
pytest --cov=src tests/
```

---

## 🛠️ Requirements

- **Python:** 3.8 or higher
- **Dependencies:** Listed in `req.txt`

Install all requirements with:

```bash
pip install -r req.txt
```


