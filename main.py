import matplotlib.pyplot as plt
import numpy as np


def apply_rules(input_string):
    left = int(input_string[0], 2)
    center = int(input_string[1], 2)
    right = int(input_string[2], 2)
    rule_key = (left << 2) | (center << 1) | right
    return rules[rule_key]

def iterate_lattice(lattice):
    new_lattice = []
    new_lattice.append("0")
    
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

rules = {
    0: "0",
    1: "1",
    2: "1",
    3: "1",
    4: "0",
    5: "1",
    6: "1",
    7: "0"
}

found_numbers = set()
# Track coverage for specific window sizes
window_sizes = [3, 4, 5, 8, 12]  # Specific n values to track
cumulative_sets = {n: set() for n in window_sizes}  # S_n(t) for each window size
coverage_history = {n: [] for n in window_sizes}  # Coverage over time for each n

lattice = "010"
picFile = open("picture.txt", "w")
numFile = open("numbers.txt", "w")

for generation in range(50):
    picFile.write(lattice + "\n")
    
    # For each specific window size, find new patterns and update cumulative set
    for n in window_sizes:
        if n <= len(lattice):  # Only process if window fits in lattice
            # Slide window of size n across the current lattice
            for i in range(len(lattice) - n + 1):
                window_bits = lattice[i:i + n]
                if len(window_bits) == n:  # Ensure we have a complete window
                    cumulative_sets[n].add(window_bits)  # Add pattern to S_n(t)
        
        # Calculate coverage for this window size: |S_n(t)| / 2^n
        total_possible = 2 ** n
        coverage = len(cumulative_sets[n]) / total_possible
        coverage_history[n].append(coverage)
    
    lattice = iterate_lattice(lattice)

# Write coverage data to file
# Format: each line has coverage for all window sizes at that generation
numFile.write("# Generation coverage for window sizes: " + ",".join(map(str, window_sizes)) + "\n")
for generation in range(50):
    coverage_line = []
    for n in window_sizes:
        if generation < len(coverage_history[n]):
            coverage_line.append(str(coverage_history[n][generation]))
        else:
            coverage_line.append("0")  # If window size was too large for early generations
    numFile.write(",".join(coverage_line) + "\n")

picFile.close()
numFile.close()