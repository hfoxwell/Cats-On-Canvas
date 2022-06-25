'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class that handles client information
'''

# External inports

# Internal Imports
from src.Image.image import image

# File Class
class client():
    ''' Represents a client '''
    
    def __init__(self, client_id: int, image: image) -> None:
        self.client_id: int = int(client_id)
        self.image: image = image