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
all_coverage_fractions = []  # Store overall coverage fraction for each generation
lattice = "010"
picFile = open("picture.txt", "w")
numFile = open("numbers.txt", "w")

for generation in range(50):
    picFile.write(lattice + "\n")
    
    # Find ALL unique numbers across all window sizes for this generation
    all_unique_numbers = set()
    max_window = len(lattice)
    
    for window_size in range(1, max_window + 1):
        # Slide window across the lattice
        for i in range(len(lattice) - window_size + 1):
            window_bits = lattice[i:i + window_size]
            number = int(window_bits, 2)
            all_unique_numbers.add(number)
    
    # Calculate overall coverage: unique numbers found / total possible numbers
    total_possible = 2 ** len(lattice)
    overall_coverage = len(all_unique_numbers) / total_possible
    all_coverage_fractions.append(overall_coverage)
    
    lattice = iterate_lattice(lattice)

# Write overall coverage fractions to file
for coverage in all_coverage_fractions:
    numFile.write(str(coverage) + "\n")

picFile.close()
numFile.close()