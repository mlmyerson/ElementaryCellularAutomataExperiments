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
    """Create a plot of the fractional coverage over time for specific window sizes"""
    # Read the coverage fractions file
    with open("numbers.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Parse header to get window sizes
    header_line = lines[0]
    if header_line.startswith("#"):
        window_sizes_str = header_line.split(": ")[1]
        window_sizes = [int(x) for x in window_sizes_str.split(",")]
        data_lines = lines[1:]
    else:
        # Fallback if no header
        window_sizes = [3, 4, 5, 8, 12]
        data_lines = lines
    
    # Parse coverage data
    coverage_data = {n: [] for n in window_sizes}
    time_steps = []
    
    for generation, line in enumerate(data_lines):
        if line:
            coverages = [float(x) for x in line.split(",")]
            time_steps.append(generation)
            for i, n in enumerate(window_sizes):
                if i < len(coverages):
                    coverage_data[n].append(coverages[i])
    
    return time_steps, coverage_data, window_sizes

def create_combined_visualization():
    """Create a combined visualization showing both the ECA pattern and coverage"""
    # Get data from files
    grid = create_eca_visualization()
    time_steps, coverage_data, window_sizes = create_fraction_plot()
    
    # Create combined plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Top plot: ECA visualization
    im = ax1.imshow(grid, cmap='binary', aspect='auto')
    ax1.set_title('Rule 110 Elementary Cellular Automaton Pattern')
    ax1.set_xlabel('Cell Position')
    ax1.set_ylabel('Generation')
    
    # Bottom plot: Coverage over time for each window size
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    for i, n in enumerate(window_sizes):
        if n in coverage_data and coverage_data[n]:
            color = colors[i % len(colors)]
            ax2.plot(time_steps[:len(coverage_data[n])], coverage_data[n], 
                    'o-', linewidth=1.5, markersize=2, color=color, 
                    label=f'n={n}', alpha=0.8)
    
    ax2.set_title('Pattern Coverage Over Time by Window Size')
    ax2.set_xlabel('Time Step (Generation)')
    ax2.set_ylabel('Fractional Coverage |S_n(t)| / 2^n')
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('combined_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("Creating Rule 110 visualizations...")
    create_combined_visualization()
    print("Visualization saved as 'combined_visualization.png'")