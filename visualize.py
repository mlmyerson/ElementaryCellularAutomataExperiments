import matplotlib.pyplot as plt
import numpy as np
import json
import sys

# Load settings from JSON file
def load_settings(settings_file="settings.json"):
    with open(settings_file, "r") as f:
        return json.load(f)

def create_eca_visualization(settings_file="settings.json"):
    """Create a black and white visualization of the Elementary Cellular Automaton"""
    settings = load_settings(settings_file)
    pic_filename = settings["output"]["picture_file"]
    
    # Read the picture file
    with open(pic_filename, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Convert to 2D array
    max_width = max(len(line) for line in lines)
    grid = np.zeros((len(lines), max_width))
    
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            grid[i, j] = int(char)
    
    return grid

def create_fraction_plot(settings_file="settings.json"):
    """Create a plot of the fractional coverage over time for specific window sizes"""
    settings = load_settings(settings_file)
    num_filename = settings["output"]["numbers_file"]
    
    # Read the coverage fractions file
    with open(num_filename, "r") as f:
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

def create_combined_visualization(settings_file="settings.json"):
    """Create a combined visualization showing both the ECA pattern and coverage"""
    settings = load_settings(settings_file)
    
    # Get data from files
    grid = create_eca_visualization(settings_file)
    time_steps, coverage_data, window_sizes = create_fraction_plot(settings_file)
    
    # Create combined plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Top plot: ECA visualization
    im = ax1.imshow(grid, cmap='binary', aspect='auto')
    # Convert rules dictionary to rule number (binary to decimal)
    rule_binary = ''.join([settings['rules'][str(i)] for i in range(7, -1, -1)])
    rule_name = int(rule_binary, 2)
    ax1.set_title(f'Elementary Cellular Automaton Pattern - Rule {rule_name}')
    ax1.set_xlabel('Cell Position')
    ax1.set_ylabel('Generation')
    
    # Bottom plot: Coverage over time for each window size
    # Use a color map to handle up to 10 window sizes nicely
    colors = plt.cm.tab10(np.linspace(0, 1, 10))
    
    for i, n in enumerate(window_sizes):
        if n in coverage_data and coverage_data[n]:
            color = colors[i % len(colors)]
            ax2.plot(time_steps[:len(coverage_data[n])], coverage_data[n], 
                    'o-', linewidth=1.5, markersize=2, color=color, 
                    label=f'n={n}', alpha=0.8)
    
    window_range = f"n={min(window_sizes)} to {max(window_sizes)}"
    ax2.set_title(f'Pattern Coverage Over Time by Window Size ({window_range})')
    ax2.set_xlabel('Time Step (Generation)')
    ax2.set_ylabel('Fractional Coverage of 2^n')
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('combined_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Get settings file from command line argument or use default
    if len(sys.argv) > 1:
        settings_file = sys.argv[1]
    else:
        settings_file = "settings.json"
    
    create_combined_visualization(settings_file)
    print("Visualization saved as 'combined_visualization.png'")