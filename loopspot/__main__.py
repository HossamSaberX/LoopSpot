#!/usr/bin/env python3
"""
Main entry point for LoopSpot CLI.
"""
import sys
from .cli import LoopSpotCLI

def main():
    """Run the LoopSpot CLI application."""
    cli = LoopSpotCLI()
    try:
        success = cli.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        if cli.loop_controller and cli.loop_controller.active:
            cli.loop_controller.stop_loop()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 