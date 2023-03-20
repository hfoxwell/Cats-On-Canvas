'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        Class that handles client information
'''

# External imports
import numpy as np

# Internal Imports
from src.Image import image


# File Class
class client():
    ''' Represents a client '''

    def __init__(self, client_id: str, image: image) -> None:

        if client_id == np.nan :
            raise ValueError("Nan value for Client ID has been passed")
        else:
            if client_id.isdigit():
                print('Yes client_id is string representation of int ')
            pass

        self.client_id: str = str(client_id)
        self.image: image = image
