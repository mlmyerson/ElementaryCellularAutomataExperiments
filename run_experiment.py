#!/usr/bin/env python3
"""
Experiment runner for Rule Cellular Automata analysis.
Usage: python run_experiment.py [settings_file]
"""
import sys
import subprocess

def run_experiment(settings_file="settings.json"):
    """Run an experiment with the specified settings file."""
    
    print(f"Using settings from: {settings_file}")
    
    print("Running cellular automaton simulation...")
    subprocess.run([sys.executable, "simulation.py", settings_file], check=True)
    
    print("Creating visualizations...")
    subprocess.run([sys.executable, "visualize.py", settings_file], check=True)
    
    print("Experiment complete!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        settings_file = sys.argv[1]
    else:
        settings_file = "settings.json"
    
    try:
        run_experiment(settings_file)
    except subprocess.CalledProcessError as e:
        print(f"Error running experiment: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Settings file not found: {e}")
        print("Available settings files:")
        import glob
        for f in glob.glob("settings*.json"):
            print(f"  - {f}")
        sys.exit(1)
