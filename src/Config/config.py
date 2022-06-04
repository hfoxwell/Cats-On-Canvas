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
@dataclass
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

    def __init__(self, filename:str, directory: str ) -> None:
        self.settings_name: str = filename
        self.settings_dir: str = directory

    @abstractmethod
    def read_file(self) -> bool:
        ''' Read the file '''

    @abstractmethod
    def load_config(self, config:config) -> config:
        ''' Load config with data'''

class json_parser(Settings_parser):
    '''Parses json settings'''
    def __init__(self, filename: str, directory: str) -> None:
        super().__init__(filename, directory)

    def read_file(self) -> bool:
        return super().read_file()

    def load_config(self, config: config) -> config:
        return super().load_config(config)

class yaml_parser(Settings_parser):
    '''Parses yaml settings'''

    def __init__(self, filename: str, directory: str) -> None:
        super().__init__(filename, directory)

    def read_file(self) -> bool:
        return super().read_file()

    def load_config(self, config: config) -> config:
        return super().load_config(config)