'''
    Author: Hayden Foxwell
    Date:   16/10/2022
    Purpose:
        Define a set of helper functions for testing
        the Cats on Canvas program.
'''

# Imports
import os, sys
import string, random

# Internal Imports

# Constants

# Functions

def generate_random_string(length: int, charset: str = string.ascii_letters) -> str:
    ''' Generates a random string of a given length '''
    # Verify parameters
    if length < 0:
        raise AttributeError("Length must be greater than 0.")
    if charset == None:
        raise AttributeError("charset cannot be None.")
    # Variables
    output: str = ""
    # Get random string
    output = ''.join(random.choice(charset) for i in range(length))
    return output
    
    