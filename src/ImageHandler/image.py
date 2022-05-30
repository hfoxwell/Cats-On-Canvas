'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class representing an image
'''
# Exernal imports
from dataclasses import dataclass
from PIL import Image
import os


# Internal Imports

# File Class
@dataclass
class image():
    image_file: Image
    image_name:str
    image_path: str
    file_type:str
    image_size = os.path.getsize(image_path)