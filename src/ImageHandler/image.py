'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class representing an image
'''
# Exernal imports
from dataclasses import dataclass
from pathlib import Path
from PIL.Image import Image

# Internal Imports

# File Class
@dataclass
class image():
    image:Image
    file_type:str