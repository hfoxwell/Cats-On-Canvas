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
    image: image.image = image.image

    def get_image(self):
        ''' returns image file '''
        #TODO: return image from file specified