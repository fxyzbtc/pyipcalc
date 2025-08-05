"""Entry point for python -m pyipcalc."""

import sys
import os

# Add the parent directory to sys.path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pyipcalc.cli import main
except ImportError:
    # Fallback for relative import
    from .cli import main

if __name__ == "__main__":
    main()
