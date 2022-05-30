'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class representing an image
'''
# Exernal imports
from dataclasses import dataclass
from pathlib import Path


# Internal Imports

# File Class
@dataclass
class image():
    image_path: str
    file_type:str