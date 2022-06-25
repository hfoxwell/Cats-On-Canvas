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
    image_canvas_id:str = field(init=False)

    def __post_init__(self):
        imgSize = self.image_file.__sizeof__
        print(imgSize)
        imgSize = os.path.getsize(f'{self.image_path}{self.image_name}')
        print(imgSize)
        self.image_size = imgSize


# File module
''' Handles all images for the app '''    
class imageFactory():

    def __init__(self, img_path: str, img_name: str) -> None:
        
        # Check that specified image exists
        if (self.image_exists(img_path, img_name)):
            raise OSError("File not Found")
        
        self.image_path: str = img_path
        self.image_name: str = img_name
        
    def open_image(self) -> image:
        '''Open an image file'''
        # Open file as byte file 
        img_bytes = open(f'{self.image_path}{self.image_name}','rb').read()
        
        # create image file object and return
        return image(img_bytes, self.image_name, self.image_path, "")

    def image_exists(self, image_path: str, image_name: str) -> bool:
        ''' Check that an image exists'''
        return os.path.exists(f'{image_path}{image_name}')
