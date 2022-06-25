"""
    Author:     Hayden Foxwell
    Date:       26/06/2022
    Purpose:
        Test the creation of images and the image factory
"""

# External imports
import pytest
import os
import random

# Internal imports
from src.Image.image import image, imageFactory

##############
# Tests
##############

def test_image(monkeypatch: pytest.MonkeyPatch):
    ''' Test the creation of an image object '''

    byte: bytearray = bytes([random.randint(0, 256) for x in range(1000)])
    name = "test.jpg"
    path = "Images/"
    filety = ".jpg"

    # Create image object
    img: image = image(byte, name, path, filety)

    print(byte.__sizeof__)

    ## Assert statements
    assert byte == img.image_file
    assert name == img.image_name
    assert path == img.image_file
    assert filety == img.file_type
    assert img.image_size == byte.__sizeof__

    