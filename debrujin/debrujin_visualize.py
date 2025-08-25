import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import json
import sys
import os

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

def parse_debruijn_data(numbers_file):
    """Parse the de Bruijn graph data from the numbers file"""
    graphs_data = {}
    
    with open(numbers_file, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    current_window_size = None
    i = 1  # Skip header line
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith("Window size "):
            current_window_size = int(line.split()[2].rstrip(':'))
            graphs_data[current_window_size] = {
                'nodes': 0,
                'edges': 0,
                'transitions': []
            }
            i += 1
            
        elif line.startswith("  Nodes: "):
            graphs_data[current_window_size]['nodes'] = int(line.split()[1])
            i += 1
            
        elif line.startswith("  Edges: "):
            graphs_data[current_window_size]['edges'] = int(line.split()[1])
            i += 1
            
        elif line.startswith("  Edge transitions:"):
            i += 1
            # Parse transitions
            while i < len(lines) and lines[i].startswith("    "):
                transition_line = lines[i].strip()
                # Parse: "source -> target (weight: X, pattern: Y)"
                parts = transition_line.split(" -> ")
                source = parts[0]
                rest = parts[1].split(" (weight: ")
                target = rest[0]
                weight_and_pattern = rest[1].rstrip(')')
                weight_part, pattern_part = weight_and_pattern.split(", pattern: ")
                weight = int(weight_part)
                pattern = pattern_part
                
                graphs_data[current_window_size]['transitions'].append({
                    'source': source,
                    'target': target,
                    'weight': weight,
                    'pattern': pattern
                })
                i += 1
        else:
            i += 1
    
    return graphs_data

def create_networkx_graph(transitions):
    """Create a NetworkX graph from transition data"""
    G = nx.DiGraph()
    
    for trans in transitions:
        G.add_edge(trans['source'], trans['target'], 
                  weight=trans['weight'], 
                  label=trans['pattern'])
    
    return G

def visualize_single_graph(G, window_size, ax):
    """Visualize a single de Bruijn graph"""
    if G.number_of_nodes() == 0:
        ax.text(0.5, 0.5, f"No data for n={window_size}", 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f"de Bruijn Graph (n={window_size})")
        return
    
    # Use different layouts based on graph size
    if G.number_of_nodes() <= 8:
        pos = nx.spring_layout(G, k=2, iterations=50)
    else:
        pos = nx.circular_layout(G)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', 
                          node_size=800, alpha=0.7)
    
    # Draw edges with weights affecting thickness
    edges = G.edges(data=True)
    weights = [d['weight'] for u, v, d in edges]
    max_weight = max(weights) if weights else 1
    
    for (u, v, d) in edges:
        weight = d['weight']
        width = 1 + 3 * (weight / max_weight)  # Scale line width
        nx.draw_networkx_edges(G, pos, [(u, v)], ax=ax, 
                             width=width, alpha=0.6, 
                             edge_color='gray', arrows=True,
                             arrowsize=15)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)
    
    # Add title with statistics
    ax.set_title(f"de Bruijn Graph (n={window_size})\n"
                f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    ax.axis('off')

def create_combined_visualization(settings_file="settings.json", numbers_file=None):
    """Create a combined visualization showing ECA pattern and de Bruijn graphs"""
    settings = load_settings(settings_file)
    
    # Use provided numbers_file or get from settings
    num_filename = numbers_file or settings["output"]["numbers_file"]
    
    # Get ECA visualization
    grid = create_eca_visualization(settings_file)
    
    # Parse de Bruijn data
    graphs_data = parse_debruijn_data(num_filename)
    
    # Convert rules dictionary to rule number
    rule_binary = ''.join([settings['rules'][str(i)] for i in range(7, -1, -1)])
    rule_name = int(rule_binary, 2)
    
    # Determine layout based on number of window sizes
    window_sizes = list(graphs_data.keys())
    num_graphs = len(window_sizes)
    
    if num_graphs <= 4:
        fig = plt.figure(figsize=(16, 12))
        # Top plot: ECA pattern (spans full width)
        ax_eca = plt.subplot2grid((3, 4), (0, 0), colspan=4)
        
        # Bottom plots: de Bruijn graphs
        graph_axes = []
        for i in range(num_graphs):
            ax = plt.subplot2grid((3, 4), (1 + i//2, (i%2)*2), colspan=2)
            graph_axes.append(ax)
    else:
        # For more graphs, use a larger grid
        rows = 2 + (num_graphs + 3) // 4  # ECA + graph rows
        fig = plt.figure(figsize=(20, 4 * rows))
        
        # Top plot: ECA pattern
        ax_eca = plt.subplot2grid((rows, 4), (0, 0), colspan=4)
        
        # Graph plots
        graph_axes = []
        for i in range(num_graphs):
            row = 1 + i // 4
            col = i % 4
            ax = plt.subplot2grid((rows, 4), (row, col))
            graph_axes.append(ax)
    
    # Plot ECA pattern
    ax_eca.imshow(grid, cmap='binary', aspect='auto')
    ax_eca.set_title(f'Elementary Cellular Automaton Pattern - Rule {rule_name}')
    ax_eca.set_xlabel('Cell Position')
    ax_eca.set_ylabel('Generation')
    
    # Plot de Bruijn graphs
    for i, window_size in enumerate(sorted(window_sizes)):
        if i < len(graph_axes):
            transitions = graphs_data[window_size]['transitions']
            G = create_networkx_graph(transitions)
            visualize_single_graph(G, window_size, graph_axes[i])
    
    plt.tight_layout()
    
    # Save with descriptive filename
    output_filename = f"debrujin_{rule_name}_visualization.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    return output_filename

if __name__ == "__main__":
    # Get settings file from command line argument or use default
    if len(sys.argv) > 1:
        settings_file = sys.argv[1]
    else:
        settings_file = "settings.json"
    
    # Parse optional args
    tail_args = sys.argv[2:]
    numbers_file_override = next((a for a in tail_args if not a.startswith("--")), None)
    no_show = any(a == "--no-show" for a in tail_args)
    
    # Create visualization
    output_file = create_combined_visualization(settings_file, numbers_file_override)
    print(f"Visualization saved as '{output_file}'")
    
    if not no_show:
        plt.show()
