'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        Class that handles client information
    Modified: (hayden foxwell - 21/03/24)
'''

# External imports
from pathlib import Path
from datetime import date
from dataclasses import dataclass

# Internal Imports
from src.Image import Image

# Unprocessed client
@dataclass
class ClientIdentifier():
    '''Represents clients before they are turned into a client object'''
    client_id: str
    profile_picture_path: Path
    file_type: str
    date_uploaded: date

# Client Class
class Client():
    ''' Represents a client '''

    def __init__(self, client_id: str, client_image: Image) -> None:

        if (len(client_id) < 1):
            raise ValueError("No value for Client ID has been passed")

        self.client_id: str = str(client_id)
        self.image: Image = client_image
