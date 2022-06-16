'''
    Author:     Hayden Foxwell
    Date:       16/06/2022
    Purpose:
        Test the user class
'''
# External imports
import pytest
import random
from pytest import MonkeyPatch

# Internal import
from src.Clients import user
from src.ImageHandler import image

def test_client(monkeypatch: MonkeyPatch):
    ''' Test creating client '''

    

    u1 = user.client(random.randint(1, 10000), image)