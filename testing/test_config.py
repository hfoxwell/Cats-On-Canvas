'''
    Author:     Hayden Foxwell
    Date:       16/06/2022
    Purpose:
        Test creation of settings files
'''
# External imports
import json
import pytest
from pytest import MonkeyPatch

# Internal imports
from src.Config import config
from src.Config import json_factory
from src.Config import yaml_factory
from src.Config import json_parser

############################
# Test cases
############################

##
# 1
##

def test_factory_json():
    ''' Test the json factory '''
    newFactory = json_factory()

    assert type(newFactory) == json_factory


##
# 2
##

def test_factory_yaml():
    ''' Test the yaml factory '''
    newFactory = yaml_factory()

    assert type(newFactory) == yaml_factory

##
# 3
##

def test_json_parser(monkeypatch: MonkeyPatch):

    jParser = json_parser(config)

    assert jParser.configuration != None
    assert jParser.Settings_contents == None

    def fake_json(file):
        return {
            "working_path"      : "./",
            "access_token"      : "abcd1234",
            "domain"            : "test.instructure.com",
            "csv_directory"     : "test_dir/",
            "images_path"   : "test_dir2",
            "csv_filename"      : "csv.csv",
            "log_filename"      : "log.txt"
        }

    monkeypatch.setattr("json.load", fake_json)

    # No error should be raised
    # read a mocked file input
    assert jParser.read_file("test.file") == True

    assert jParser.settings_contents != None

    # Load the config file
    conf = jParser.load_config()

    # Asser that returned config should not be none
    assert conf != None

    