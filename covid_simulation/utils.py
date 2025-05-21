"""
------------------------------------------------------------------------------
File        : utils.py
Description : Random number utilities for uniform distributions (int/float).
Authors     : Simon Haebenbrock, Jonathan Stengl, Nico Klose
Group       : Group 6
------------------------------------------------------------------------------
"""

import random

def uniform_int(low, high):
    """
    Returns a random integer from a uniform distribution between low and high.
    """
    return int(random.uniform(low, high))

def uniform_float(low, high):
    """
    Returns a random float from a uniform distribution between low and high.
    """
    return random.uniform(low, high)
