import sys
import os

__version__ = "1.0.0"
__author__ = "Alan Nardo"

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory to sys.path
sys.path.append(parent_dir)
