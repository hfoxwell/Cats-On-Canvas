'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class that handles client information
'''

# External inports
from dataclasses import dataclass

# Internal Imports
from src.ImageHandler.image import image
from src.ImageHandler.image_handler import image_handler

# File Class
@dataclass
class client():
    ''' Represents a client '''
    client_id: int
    image_path: str
    image_type: str

    def get_image(self) -> image:
        ''' returns image file '''
        #TODO: return image from file specified