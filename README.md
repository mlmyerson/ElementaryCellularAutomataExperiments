# Elementary Cellular Automata Experiments

A Python program for simulating and analyzing Elementary Cellular Automata (ECA) with pattern coverage analysis across different window sizes.

## Overview

This project implements a computational experiment to study how patterns emerge and spread in Elementary Cellular Automata. The program simulates ECA evolution over time and analyzes the coverage of all possible binary patterns within sliding windows of various sizes.

### What it does:

1. **Simulates** an Elementary Cellular Automaton based on configurable rules
2. **Tracks** pattern coverage for different window sizes over time
3. **Visualizes** both the automaton evolution and pattern coverage statistics
4. **Generates** data files for further analysis

## Files Description

- `run_experiment.py` - Main experiment runner that orchestrates the simulation and visualization
- `simulation.py` - Core ECA simulation engine that generates lattice evolution and coverage data
- `visualize.py` - Creates combined visualizations of the automaton pattern and coverage plots
- `settings.json` - Configuration file for experiment parameters
- `picture.txt` - Output file containing the lattice state for each generation (generated)
- `numbers.txt` - Output file containing coverage data over time (generated)
- `combined_visualization.png` - Generated visualization plot (generated)

## Requirements

- Python 3.x
- Required packages:
  - `matplotlib`
  - `numpy`

Install dependencies:
```bash
pip install matplotlib numpy
```
### Usage

Run the experiment with default settings:
```bash
python run_experiment.py
```

### Custom Settings

Run with a specific settings file:
```bash
python run_experiment.py my_settings.json
```

### Individual Components

You can also run components separately:

1. **Run simulation only:**
   ```bash
   python simulation.py [settings_file]
   ```

2. **Create visualization only:** (requires existing data files)
   ```bash
   python visualize.py [settings_file]
   ```

## Configuration

The `settings.json` file controls the experiment parameters:

```json
{
  "window_sizes": {
    "sizes": [1, 2, 3, 4, 7, 11, 18, 29],
    "description": "Window sizes to analyze for pattern coverage"
  },
  "generations": {
    "count": 50,
    "description": "Number of generations to simulate"
  },
  "rules": {
    "0": "0", "1": "1", "2": "1", "3": "1",
    "4": "0", "5": "1", "6": "1", "7": "0",
    "description": "ECA rule lookup table (0-7 neighborhood states)"
  },
  "initial_state": {
    "pattern": "1",
    "description": "Initial lattice pattern"
  },
  "output": {
    "picture_file": "picture.txt",
    "numbers_file": "numbers.txt",
    "description": "Output file names"
  }
}
```

### Key Parameters:

- **Window sizes**: Array of window sizes (n) to analyze pattern coverage for 2^n possible patterns
- **Generations**: Number of time steps to simulate
- **Rules**: The ECA rule table mapping 3-bit neighborhoods (000-111) to output states (0 or 1)
- **Initial pattern**: Starting configuration (e.g., "1" for single active cell, "101" for pattern)

## Output Files

### `picture.txt`
Contains the lattice state for each generation, one line per generation:
```
0000000001000000000
0000000011100000000
0000000110110000000
...
```

### `numbers.txt`
Contains coverage data with header line and comma-separated values:
```
# Generation coverage for window sizes: 1,2,3,4,7,11,18,29
0.5,0.25,0.125,0.0625,0.0078125,0.00048828125,0.0,0.0
1.0,0.75,0.375,0.1875,0.0234375,0.001953125,0.0,0.0
...
```

### `combined_visualization.png`
A two-panel plot showing:
- **Top**: Black and white visualization of the ECA evolution pattern
- **Bottom**: Line plots of fractional coverage over time for each window size

## Example Rules

The default settings implement **Rule 110** (01101110 in binary), a famous ECA rule known for being Turing complete. You can modify the rules in `settings.json` to experiment with other ECA rules:

- **Rule 30**: `{"0":"0","1":"1","2":"1","3":"1","4":"1","5":"0","6":"0","7":"0"}`
- **Rule 90**: `{"0":"0","1":"1","2":"0","3":"1","4":"1","5":"0","6":"1","7":"0"}`
- **Rule 184**: `{"0":"0","1":"0","2":"0","3":"1","4":"1","5":"1","6":"1","7":"1"}`

## Pattern Coverage Analysis

The program calculates **fractional coverage** for each window size n:
- Slides a window of size n across each generation
- Records all unique n-bit patterns encountered
- Calculates coverage as: (unique patterns found) / 2^n

This analysis helps understand:
- How quickly the automaton explores pattern space
- Differences in complexity across window sizes
- Long-term behavior and pattern saturation

## Research Applications

This tool is useful for:
- Studying computational complexity in cellular automata
- Analyzing pattern formation and propagation
- Comparing different ECA rules
- Understanding information-theoretic properties of cellular automata
- Educational demonstrations of emergent complexity

## License

This project is open source. Feel free to modify and extend for your research or educational purposes.
