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

def find_coverage_by_window_size(lattice, max_window_size):
    """Find coverage for each window size - keeping for potential future use"""
    pass

# Get configuration from settings
window_sizes = settings["window_sizes"]["sizes"]
num_generations = settings["generations"]["count"]
initial_pattern = settings["initial_state"]["pattern"]
pic_filename = settings["output"]["picture_file"]
num_filename = settings["output"]["numbers_file"]

# Calculate lattice width needed for growth over all generations
pattern_length = len(initial_pattern)
padding_per_side = num_generations + 10  # Extra padding for safety
total_width = pattern_length + (2 * padding_per_side)

# Create initial lattice with pattern centered
padding_left = padding_per_side
padding_right = total_width - pattern_length - padding_left
initial_lattice = ('0' * padding_left) + initial_pattern + ('0' * padding_right)

found_numbers = set()
cumulative_sets = {n: set() for n in window_sizes}  # S_n(t) for each window size
coverage_history = {n: [] for n in window_sizes}  # Coverage over time for each n

lattice = initial_lattice
picFile = open(pic_filename, "w")
numFile = open(num_filename, "w")

for generation in range(num_generations):
    picFile.write(lattice + "\n")
    
    # For each window size, find new patterns and update cumulative set
    for n in window_sizes:
        if n <= len(lattice):  # Only process if window fits in lattice
            # Slide window of size n across the current lattice
            for i in range(len(lattice) - n + 1):
                window_bits = lattice[i:i + n]
                if len(window_bits) == n:  # Ensure we have a complete window
                    cumulative_sets[n].add(window_bits)  # Add pattern to S_n(t)
        
        # Calculate integer coverage for this window size
        total_possible = 2 ** n
        coverage = len(cumulative_sets[n]) / total_possible
        coverage_history[n].append(coverage)
    
    lattice = iterate_lattice(lattice)

# Write coverage data to file
# Format: each line has coverage for all window sizes at that generation
numFile.write("# Generation coverage for window sizes: " + ",".join(map(str, window_sizes)) + "\n")
for generation in range(num_generations):
    coverage_line = []
    for n in window_sizes:
        if generation < len(coverage_history[n]):
            coverage_line.append(str(coverage_history[n][generation]))
        else:
            coverage_line.append("0")  # If window size was too large for early generations
    numFile.write(",".join(coverage_line) + "\n")

picFile.close()
numFile.close()