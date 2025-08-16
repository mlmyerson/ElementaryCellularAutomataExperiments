import matplotlib.pyplot as plt
import numpy as np

def create_eca_visualization():
    """Create a black and white visualization of the Elementary Cellular Automaton"""
    # Read the picture file
    with open("picture.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Convert to 2D array
    max_width = max(len(line) for line in lines)
    grid = np.zeros((len(lines), max_width))
    
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            grid[i, j] = int(char)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.imshow(grid, cmap='binary', aspect='auto')
    plt.title('Rule 110 Elementary Cellular Automaton')
    plt.xlabel('Cell Position')
    plt.ylabel('Generation')
    plt.tight_layout()
    plt.savefig('eca_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()

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
    

create_eca_visualization()
create_number_plot()

