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
    
    return grid

def create_fraction_plot():
    """Create a plot of the fractional coverage over time"""
    # Read the coverage fractions file
    with open("numbers.txt", "r") as f:
        coverage_fractions = [float(line.strip()) for line in f.readlines() if line.strip()]
    
    # Create time steps (x-axis)
    time_steps = list(range(len(coverage_fractions)))
    
    return time_steps, coverage_fractions

def create_combined_visualization():
    """Create a combined visualization showing both the ECA pattern and coverage"""
    # Get data from files
    grid = create_eca_visualization()
    time_steps, coverage_fractions = create_fraction_plot()
    
    # Create combined plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Top plot: ECA visualization
    im = ax1.imshow(grid, cmap='binary', aspect='auto')
    ax1.set_title('Rule 110 Elementary Cellular Automaton Pattern')
    ax1.set_xlabel('Cell Position')
    ax1.set_ylabel('Generation')
    
    # Bottom plot: Coverage over time
    ax2.plot(time_steps, coverage_fractions, 'bo-', linewidth=1.5, markersize=3)
    ax2.set_title('Number Space Coverage Over Time')
    ax2.set_xlabel('Time Step (Generation)')
    ax2.set_ylabel('Fractional Coverage (0 to 1)')
    ax2.set_xlim(0, len(coverage_fractions))
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('combined_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Creating Rule 110 visualizations...")
    create_combined_visualization()
    print("Visualization saved as 'combined_visualization.png'")