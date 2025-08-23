import matplotlib.pyplot as plt
import numpy as np
import json
import sys

# Load settings from JSON file
def load_settings(settings_file="settings.json"):
    with open(settings_file, "r") as f:
        return json.load(f)

# Get settings file from command line argument or use default
if len(sys.argv) > 1:
    settings_file = sys.argv[1]
else:
    settings_file = "settings.json"

# Optional override for numbers output filename
numbers_output_override = sys.argv[2] if len(sys.argv) > 2 else None

settings = load_settings(settings_file)

def apply_rules(input_string):
    left = int(input_string[0], 2)
    center = int(input_string[1], 2)
    right = int(input_string[2], 2)
    rule_key = (left << 2) | (center << 1) | right
    return settings["rules"][str(rule_key)]

def iterate_lattice(lattice):
    new_lattice = []
    
    for i in range(len(lattice)):
        left = lattice[i - 1] if i > 0 else '0'
        center = lattice[i]
        right = lattice[i + 1] if i < len(lattice) - 1 else '0'
        neighborhood = left + center + right
        new_lattice.append(apply_rules(neighborhood))
    
    return ''.join(new_lattice)

# Get configuration from settings
window_sizes = settings["window_sizes"]["sizes"]
num_generations = settings["generations"]["count"]
initial_pattern = settings["initial_state"]["pattern"]
pic_filename = settings["output"]["picture_file"]
num_filename = numbers_output_override or settings["output"]["numbers_file"]

# Calculate lattice width needed for growth over all generations
pattern_length = len(initial_pattern)
padding_per_side = num_generations + 10  # Extra padding for safety
total_width = pattern_length + (2 * padding_per_side)

# Create initial lattice with pattern centered
padding_left = padding_per_side
padding_right = total_width - pattern_length - padding_left
initial_lattice = ('0' * padding_left) + initial_pattern + ('0' * padding_right)


lattice = initial_lattice
picFile = open(pic_filename, "w")
numFile = open(num_filename, "w")
states = {}

# Compute pattern
for generation in range(num_generations):
    picFile.write(lattice + "\n")

    # For each window size, find new patterns and update cumulative set
    for n in window_sizes:
        if n <= len(lattice):  # Only process if window fits in lattice
            # Add new window as key
            states[n] = {}
            # Slide window of size n across the current lattice
            for i in range(len(lattice) - n + 1):
                window_bits = lattice[i:i + n]
                # Add to the bit-pattern count
                states[n][window_bits] += 1
    lattice = iterate_lattice(lattice)

# Format: each line has states count for all window sizes
numFile.write("# State count for window sizes: " + ",".join(map(str, window_sizes)) + "\n")
for generation in range(num_generations):
    for window, states in states:
        numFile.write(",".join(states) + "\n")

picFile.close()
numFile.close()