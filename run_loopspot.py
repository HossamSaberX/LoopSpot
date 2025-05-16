#!/usr/bin/env python3
"""
Runner script for LoopSpot CLI.
"""
import sys
import os

# Add the parent directory to the path so we can import loopspot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import and run
from loopspot.__main__ import main

if __name__ == "__main__":
    main() 