'''
    Author:     Hayden Foxwell
    Date:       16/06/2022
    Purpose:
        Test the user class
'''
# External imports
import pytest
from pytest import MonkeyPatch


# Internal import
from src.Clients.user import client
from src.ImageHandler import image

def test_client(monkeypatch: MonkeyPatch):
    ''' Test client Creation'''
    # Provide function to patch image init
    def patch_image():
        return object()

    # Monkey Patch the initaliser
    monkeypatch.setattr(image,'image',  patch_image)

    # Create new user
    newuser = client(12345, image.image())

    # New user should not be null 
    #   and new user should have user id
    assert newuser != None
    assert newuser.client_id == 12345


def test_no_client(monkeypatch: MonkeyPatch):
    ''' Test client failure'''
    
    # Provide function to patch image init
    def patch_image():
        return object()

    # Monkey Patch the initaliser
    monkeypatch.setattr(image,'image',  patch_image)

    with pytest.raises(ValueError):
        newuser = client("Hello", image.image())