'''
    Author: H Foxwell
    Date:   04/06/2022
    Purpose:    
        Class for parsing and storing settings. 
        Settings shifting from json to YAML.
'''

# External imports
from abc import ABC, abstractmethod
from dataclasses import dataclass

try:
    import yaml
except ImportError:
    print("YAML can't be loaded importing json")
    import json

# Internal Imports

# Classes
@dataclass()
class config():
    '''Store the settings config'''
    # Directory settings
    working_path: str
    csv_directory: str
    images_path: str

    # Canvas access settings
    access_token: str
    domain: str

    # File settings
    log_filename: str
    csv_filename: str



class Settings_parser(ABC):
    '''Base class for parsing settings to an object'''

    def __init__(self, config: config) -> None:
        ''' Initalises a parser with default values that can be overridden '''
        self.configuration: config = config
        self.Settings_contents = None

    @abstractmethod
    def read_file(self, settings_file) -> bool:
        ''' Read the file '''

    @abstractmethod
    def load_config(self) -> config:
        ''' Load config with data'''

class json_parser(Settings_parser):
    '''Parses json settings'''
    
    def __init__(self, config: config) -> None:
        super().__init__(config)

    def read_file(self, settings_file) -> bool:
        ''' Reads the settings file'''

        # Try to read json settings
        try:
            self.settings_contents = json.load(settings_file)
        
        # If decode of json file fails catch error and report
        except json.decoder.JSONDecodeError:
            print(json.decoder.JSONDecodeError('There was an error decoding the json file'))
            return False
        
        # On success. Return true
        return True

    def load_config(self) -> config:
        '''Creates a config object'''

        conf: config = self.configuration(
            working_path = self.settings_contents['working_path'],
            access_token = self.settings_contents['access_token'],
            domain = self.settings_contents['domain'],
            csv_directory = self.settings_contents['csv_directory'],
            csv_filename = self.settings_contents['csv_filename'],
            images_path = self.settings_contents['images_path'],
            log_filename = self.settings_contents['log_filename']
        )
    
        return conf

class yaml_parser(Settings_parser):
    '''Parses yaml settings'''

    def __init__(self, config: config) -> None:
        super().__init__(config)

    def read_file(self, settings_file) -> bool:
        try:
            self.Settings_contents = yaml.load(settings_file)
        
        except KeyError:
            print(KeyError("Key missing from yaml file"))
            return False

        return True

    def load_config(self) -> config:
        return super().load_config(config)