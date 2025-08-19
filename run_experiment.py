#!/usr/bin/env python3
"""
Experiment runner for Rule Cellular Automata analysis.
Usage:
  python run_experiment.py [mode] [options]

Modes:
  help            Show this help message and exit (default)
  integer-count   Run the integer coverage simulation (current functionality)

Examples:
  python run_experiment.py                             # show help by default
  python run_experiment.py help                        # show help explicitly
  python run_experiment.py integer-count --graph       # also generate the graph
  python run_experiment.py -s custom_settings.json     # use a different settings file
  python run_experiment.py integer-count -s settings_a.json settings_b.json  # batch run
"""
import sys
import subprocess
import argparse
import os
import json


def run_experiment(settings_file: str = "settings.json", graph: bool = False) -> None:
    """Run an experiment with the specified settings file.

    Args:
        settings_file: Path to the JSON settings file.
        graph: When True, also generate the visualization after simulation.
    """
    # Validate settings file early for clearer errors
    if not os.path.exists(settings_file):
        raise FileNotFoundError(settings_file)

    print(f"Using settings from: {settings_file}")

    # Compute rule number up front for naming outputs
    with open(settings_file, "r") as f:
        s = json.load(f)
    rule_binary = ''.join([s['rules'][str(i)] for i in range(7, -1, -1)])
    rule_name = int(rule_binary, 2)

    numbers_out = f"integercount_{rule_name}.txt"

    print("Running cellular automaton simulation...")
    # Pass settings and numbers override to simulation
    subprocess.run([sys.executable, "simulation.py", settings_file, numbers_out], check=True)

    print(f"Results saved: {numbers_out} and {s['output']['picture_file']}")

    if graph:
        print("Creating visualizations (graph output)...")
        subprocess.run([sys.executable, "visualize.py", settings_file], check=True)
        print(f"Graph saved (see rule_{rule_name}_visualization.png)")
    else:
        print("Skipping graph generation (use --graph to enable)")

    print("Experiment complete!")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Elementary Cellular Automata experiments and optional visualization.",
    )

    # Positional mode allows future expansion; defaults to showing help for new users
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["help", "integer-count"],
        default="help",
        help="Operation mode. Use 'help' to see options or 'integer-count' to run the simulation.",
    )

    parser.add_argument(
        "-s",
        "--settings",
        nargs="+",
        default=["settings.json"],
        help="One or more settings JSON files (supports shell globs)",
    )

    parser.add_argument(
        "--graph",
        action="store_true",
        help="Also output a combined visualization graph (in addition to result files)",
    )

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.mode == "help":
            parser.print_help()
            sys.exit(0)
        elif args.mode == "integer-count":
            settings_list = args.settings if isinstance(args.settings, list) else [args.settings]
            for sfile in settings_list:
                run_experiment(settings_file=sfile, graph=bool(args.graph))
        else:
            # This branch should not be reachable due to choices constraint
            parser.error(f"Unknown mode: {args.mode}")
    except subprocess.CalledProcessError as e:
        print(f"Error running experiment: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Settings file not found: {e}")
        sys.exit(1)
