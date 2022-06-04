'''
    Author: H Foxwell
    Date:   04/06/2022
    Purpose:    
        Class for parsing and storing settings. 
        Settings shifting from json to YAML.
'''

# External imports
from dataclasses import dataclass
import yaml

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


class Settings_parser():
    '''Parse the settings'''

    def __init__(self, filename:str, directory: str ) -> None:
        self.settings_name: str = filename
        self.settings_dir: str = directory

    def read_file(self):
        ''' Read the file '''
        with open(f'{self.settings_dir}{self.settings_name}', 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

    def load_config(self, config:config):
        ''' Load config with data'''



