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

def find_numbers(lattice):
    out = set()
    max_window = len(lattice)
    window = 0
    while window <= max_window:
        for i in range(window):
            bits = lattice[i:i + window]
            found = int(bits, 2)
            out.add(found)
        window += 1
    return out

def create_number_plot():
    """Create a plot of the binary numbers over time"""
    # Read the numbers file
    with open("numbers.txt", "r") as f:
        numbers = [int(line.strip()) for line in f.readlines() if line.strip()]
    
    # Create y-axis from 0 to n (generation numbers)
    numberSpace = [i**2 for i in range(len(numbers))]
    
    plt.figure(figsize=(12, 6))
    plt.plot(numbers, numberSpace, 'b-', linewidth=1.5)
    plt.title('Rule 110 - Integers computed over time')
    plt.xlabel('Integer Value')
    plt.ylabel('Possible Integers')
    plt.ylim(0, len(numbers) ** 2)
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
lattice = "010"
picFile = open("picture.txt", "w")
numFile = open("numbers.txt", "w")
for _ in range(50):
    # picFile.write(lattice + "\n")
    # the total integer each row makes
    # numFile.write(str(int(lattice, 2)) + "\n")
    found_numbers.update(find_numbers(lattice))
    lattice = iterate_lattice(lattice)

for num in found_numbers:
    numFile.write(str(num) + "\n")

picFile.close()
numFile.close()
create_number_plot()