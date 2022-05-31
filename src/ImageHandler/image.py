'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class representing an image
'''
# Exernal imports
from dataclasses import dataclass
import os


# Internal Imports

# File Class
@dataclass
class image:
    image_file: bytes
    image_name:str
    image_path: str
    file_type:str
    image_size = os.path.getsize(image_path)