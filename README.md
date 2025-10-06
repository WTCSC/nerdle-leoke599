<!-- 
   Assignment Notes:
   - To run the game, execute `python3 nerdle.py` in the terminal.
   - Your task is to implement the equation generation functions in `equation_generator.py` and the solution validator in `game_engine.py`.
   - Don't forget to import your modules.
   - PAY ATTENTION TO THE TODO COMMENTS IN THE CODE.
   - Each function has comments detailing its purpose and requirements.
   - Code is automatically tested *every time* you push changes to GitHub.
-->

# Nerdle

Nerdle is a small Python implementation of a Wordle-like game where the
player must guess an 8-character mathematical equation (for example `12+3=15`).
This repository contains a playable CLI, an equation generator, and unit tests
used for automated grading.

![Nerdle screenshot](images/nerdle.png)

## Key features

- CLI play mode (`nerdle.py`)
- Equation generation utilities (`equation_generator.py`)
- Game validation and feedback (`game_engine.py`)

## Requirements

- Python 3.8+ (3.12 tested in CI)
- No external packages required — uses only the Python standard library

## Installation

1. Clone the repository and change into the project directory:

```bash
git clone <repo-url>
cd nerdle-leoke599
```

2. (Optional) Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Run the game:

```bash
python3 nerdle.py
```

On systems where `python` points to Python 3 you can use `python nerdle.py`.

## How to play (CLI)

- The program will pick a random valid 8-character equation.
- Enter guesses in the terminal in the same 8-character format.
- The game will provide feedback (correct/incorrect positions or characters).