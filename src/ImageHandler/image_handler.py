'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for handling the getting and creation of image objects in the
        system.
'''

# External imports
import os

# Internal Imports\
from src.ImageHandler.image import image

# File module
''' Handles all images for the app '''    

def open_image(working_dir: str, image_path: str, image_name: str) -> image:
    '''Open an image file'''
    # Ensure image exists
    if (image_exists(working_dir, image_path, image_name)):
        # If image exists return opened file
        img_bytes = open(f'{working_dir}{image_path}{image_name}','rb').read()
        
        img = image(img_bytes, image_name, image_path, "")

        return img
    else:
        return None

def image_exists(working_dir: str, image_path: str, image_name: str) -> bool:
    ''' Check that an image exists'''
    return os.path.exists(f'{working_dir}{image_path}{image_name}')
