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
    """Find coverage for each window size"""
    coverage_results = {}
    
    for window_size in range(1, max_window_size + 1):
        found_numbers = set()
        max_possible = 2 ** window_size
        
        # Slide window across the lattice
        for i in range(len(lattice) - window_size + 1):
            window_bits = lattice[i:i + window_size]
            number = int(window_bits, 2)
            found_numbers.add(number)
        
        coverage = len(found_numbers) / max_possible
        coverage_results[window_size] = {
            'coverage': coverage,
            'found': len(found_numbers),
            'possible': max_possible,
            'complete': len(found_numbers) == max_possible
        }
            
    return coverage_results

def create_fraction_plot():
    """Create a plot of the fractional coverage over time"""
    # Read the coverage fractions file
    with open("numbers.txt", "r") as f:
        coverage_fractions = [float(line.strip()) for line in f.readlines() if line.strip()]
    
    # Create time steps (x-axis)
    time_steps = list(range(len(coverage_fractions)))
    
    plt.figure(figsize=(12, 6))
    plt.plot(time_steps, coverage_fractions, 'bo-', linewidth=1.5, markersize=4)
    plt.title('Number Space Coverage Over Time in Rule 110 Patterns')
    plt.xlabel('Time Step (Generation)')
    plt.ylabel('Fractional Coverage (0 to 1)')
    plt.xlim(0, len(coverage_fractions))
    plt.ylim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('numbers_plot.png', dpi=300, bbox_inches='tight')
    plt.show()

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
create_fraction_plot()