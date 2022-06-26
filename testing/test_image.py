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
##
# 1
##

def test_image():
    ''' Test the creation of a fake image object '''

    byte: bytes = [bytes(random.randint(0, 256)) for x in range(1000)]
    name = "1042800.jpeg"
    path = "Images/"
    filety = ".jpg"

    # Create image object
    img: image = image(byte, name, path, filety)

    ## Assert statements
    assert byte == img.image_file
    assert name == img.image_name
    assert path == img.image_path
    assert filety == img.file_type
    assert img.image_size == (byte.__sizeof__())

##
# 2
##

def test_image_real():
    ''' Test with real image '''
    
    # Variables
    byte: bytes = open("./testing/testFiles/catto.jpeg",'rb').read()
    sizeBytes = (byte.__sizeof__())
    name = "1042800.jpeg"
    path = "Images/"
    filety = ".jpg"

    # Create image object
    img: image = image(byte, name, path, filety)

    ## Assert statements
    assert byte == img.image_file
    assert name == img.image_name
    assert path == img.image_path
    assert filety == img.file_type
    assert img.image_size == sizeBytes

##
# 3
##

def test_factory(monkeypatch: pytest.MonkeyPatch):
    ''' Create factory and test object '''

    # Variables
    img_path = "testing/testFiles/"
    img_name = "test.jpeg"


    ## Monkey patching the functions of the factory
    # patching the open image file function
    def patchFile(_):
        ''' Patch file creation '''
        return image((bytes(random.randint(0, 256))),img_name,img_path, ".jpeg")
    # Patch the function into the factory
    monkeypatch.setattr(imageFactory, "open_image", patchFile)

    # Monkey patch the check file exists function
    def patchCheck(_, _1, _2):
        ''' Replace the file check '''
        return True
    # patch the function into the factory
    monkeypatch.setattr(imageFactory, "image_exists", patchCheck)

    # Create factory
    fact: imageFactory = imageFactory(img_path, img_name)

    # Asserts
    assert type(fact) != None
    assert isinstance(fact, imageFactory)
    assert fact.image_name == img_name
    assert fact.image_path == img_path
    assert isinstance(fact.open_image(), image)