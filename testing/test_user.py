'''
    Author:     Hayden Foxwell
    Date:       16/06/2022
    Purpose:
        Test the user class
'''
# External imports
import pytest, random, string
from pytest import MonkeyPatch


# Internal import
from src.Clients.user import client
from src.Image import image

def test_client(monkeypatch: MonkeyPatch):
    ''' Test client Creation'''
    # Variables
    user_ID: str = "".join(random.choices(string.ascii_letters + string.digits, k=10))

    # Provide function to patch image init
    def patch_image():
        return object()

    # Monkey Patch the initaliser
    monkeypatch.setattr(image,'image',  patch_image)

    # Create new user
    newuser = client(user_ID, image.image())

    # New user should not be null 
    #   and new user should have user id
    assert newuser != None
    assert newuser.client_id == user_ID


def test_no_client(monkeypatch: MonkeyPatch):
    ''' Test client failure'''

    user_ID = ""                # Test empty client ID
    
    # Provide function to patch image init
    def patch_image():
        return object()

    # Monkey Patch the initaliser
    monkeypatch.setattr(image,'image',  patch_image)

    with pytest.raises(ValueError):
        newuser = client(user_ID, image.image())