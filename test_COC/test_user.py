'''
    Author:     Hayden Foxwell
    Date:       16/06/2022
    Purpose:
        Test the user class
'''
# External imports
import pytest
import random
import string
from pytest import MonkeyPatch

# Internal import
from src.Clients import client
from src.Image import image


# Provide function to patch image init
def patch_image(x):
        return None

def test_client_creation_with_valid_input(monkeypatch: MonkeyPatch):
    '''
    Test client creation with valid input.
    '''
    # Variables
    user_ID: str = "".join(random.choices(string.ascii_letters + string.digits, k=10))

    

    # Monkey Patch the initializer
    monkeypatch.setattr(image, '__init__', patch_image)

    # Create new user
    newuser = client(user_ID, image())

    # New user should not be null 
    #   and new user should have user id
    assert newuser is not None
    assert newuser.client_id == user_ID
    assert isinstance(newuser.image, image)


def test_client_creation_with_invalid_input(monkeypatch: MonkeyPatch):
    '''
    Test client creation with invalid input.
    '''
    # Variables
    user_ID: str = ""

    # Monkey Patch the initializer
    monkeypatch.setattr(image, '__init__', patch_image)

    # Ensure ValueError is raised with empty client ID
    with pytest.raises(ValueError):
        client(user_ID, image())


def test_client_creation_with_none_image_object(monkeypatch: MonkeyPatch):
    '''
    Test client creation with None image object.
    '''
    # Variables
    user_ID: str = "".join(random.choices(string.ascii_letters + string.digits, k=10))

    # Monkey Patch the initializer
    monkeypatch.setattr(image, '__init__', None)

    # Ensure ValueError is raised with None image object
    with pytest.raises(ValueError):
        client(user_ID, image())


def test_client_creation_with_non_image_object(monkeypatch: MonkeyPatch):
    '''
    Test client creation with non-image object.
    '''
    # Variables
    user_ID: str = "".join(random.choices(string.ascii_letters + string.digits, k=10))

    # Monkey Patch the initializer
    monkeypatch.setattr(image, '__init__', patch_image)

    # Ensure ValueError is raised with non-image object
    with pytest.raises(ValueError):
        client(user_ID, image())
