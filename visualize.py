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
    
    return grid

def create_number_plot():
    """Create a plot of the binary numbers over time"""
    # Read the numbers file
    with open("numbers.txt", "r") as f:
        numbers = [int(line.strip()) for line in f.readlines() if line.strip()]
    
    generations = list(range(len(numbers)))
    max_value = 2 ** len(numbers)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(generations, numbers, 'b-', linewidth=1.5, alpha=0.8)
    plt.fill_between(generations, numbers, alpha=0.3)
    
    plt.title('Rule 110 - Binary Values Over Time')
    plt.xlabel('Generation')
    plt.ylabel('Binary Value (Base 10)')
    plt.ylim(0, max_value)
    plt.grid(True, alpha=0.3)
    
    # Add some statistics
    plt.text(0.02, 0.98, f'Max possible value: {max_value:,}\nActual max: {max(numbers):,}\nGenerations: {len(numbers)}', 
             transform=plt.gca().transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('numbers_plot.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return numbers, max_value

def create_combined_visualization():
    """Create a combined visualization showing both the ECA pattern and the numbers"""
    # Get data
    grid = create_eca_visualization()
    numbers, max_value = create_number_plot()
    
    # Create combined plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Top plot: ECA visualization
    im = ax1.imshow(grid, cmap='binary', aspect='auto')
    ax1.set_title('Rule 110 Elementary Cellular Automaton Pattern')
    ax1.set_xlabel('Cell Position')
    ax1.set_ylabel('Generation')
    
    # Bottom plot: Numbers over time
    generations = list(range(len(numbers)))
    ax2.plot(generations, numbers, 'b-', linewidth=1.5, alpha=0.8)
    ax2.fill_between(generations, numbers, alpha=0.3)
    ax2.set_title('Binary Values Over Time')
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('Binary Value (Base 10)')
    ax2.set_ylim(0, max_value)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('combined_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Creating Elementary Cellular Automaton visualization...")
    create_combined_visualization()
    print("Visualizations saved as:")
    print("- eca_visualization.png")
    print("- numbers_plot.png") 
    print("- combined_visualization.png")
