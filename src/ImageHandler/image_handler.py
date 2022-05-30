'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for handling the getting and creation of image objects in the
        system.
'''

# External imports
import os

# Internal Imports

# File Class
class image_handler():
    ''' Handles all images for the app '''    

    def open_image(self, working_dir: str, image_path: str, image_name: str):
        '''Open an image file'''
        # Ensure image exists
        if (self.image_exists(working_dir, image_path)):
            # If image exists return opened file
            return open(f'{working_dir}{image_path}{image_name}')
        else:
            return None

    def image_exists(self, working_dir: str, image_path: str) -> bool:
        ''' Check that an image exists'''
        return os.path.exists(f'{working_dir}{image_path}')