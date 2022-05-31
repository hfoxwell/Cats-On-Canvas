'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class representing an image
'''
# Exernal imports
from dataclasses import dataclass, field
import os


# Internal Imports

# File Class
@dataclass
class image:
    image_file: bytes = field(compare=False)
    image_name:str = field(compare=True)
    image_path: str = field(compare=False)
    file_type:str = field(compare=False)
    image_size:int = field(init=False)

    def __post_init__(self):
        self.image_size = os.path.getsize(self.image_file)
