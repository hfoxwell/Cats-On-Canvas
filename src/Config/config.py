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
    import json
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
        ''' Initialises a parser with default values that can be overridden '''
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
        except Exception as e:
            print(e)
            print('An issue occurred with the settings.json')
            return False

        # On success. Return true
        print("SUCCESS: settings loaded")
        return True

    def load_config(self) -> config:
        '''Creates a config object'''

        conf: config = self.configuration(
            working_path=self.settings_contents['working_path'],
            access_token=self.settings_contents['access_token'],
            domain=self.settings_contents['domain'],
            csv_directory=self.settings_contents['csv_directory'],
            csv_filename=self.settings_contents['csv_filename'],
            images_path=self.settings_contents['images_path'],
            log_filename=self.settings_contents['log_filename']
        )

        return conf


class yaml_parser(Settings_parser):
    '''Parses yaml settings'''

    def __init__(self, config: config) -> None:
        super().__init__(config)

    def read_file(self, settings_file) -> bool:
        ''' Read the config from Yaml file '''
        # Variables

        try:
            # Read the yaml file
            self.Settings_contents = yaml.safe_load(settings_file)

        except yaml.YAMLError as exc:
            # if the error contains problem mark
            # then identify where the error was
            if hasattr(exc, 'problem_mark'):
                # Get the problem mark
                mark = exc.problem_mark
                # Print out to the user
                print(f'Error position: ({mark.line}:{mark.column})')

            # Indicate the failure of the function
            return False

        # If no error indicate function success
        print("SUCCESS: Settings Loaded")
        return True

    def load_config(self) -> config:
        ''' load a config'''
        # Variables
        conf: config = None

        conf = self.configuration(
            working_path=self.Settings_contents['Directories']['working_path'],
            access_token=self.Settings_contents['Canvas_data']['access_token'],
            domain=self.Settings_contents['Canvas_data']['domain'],
            csv_directory=self.Settings_contents['Directories']['csv_directory'],
            csv_filename=self.Settings_contents['File_names']['csv_filename'],
            images_path=self.Settings_contents['Directories']['images_directory'],
            log_filename=self.Settings_contents['File_names']['log_filename']
        )

        return conf


# Factories
class abstract_settings_factory(ABC):
    ''' Abstract factory class '''
    @abstractmethod
    def create_parser(self) -> Settings_parser:
        ''' Create a parser '''


class json_factory(abstract_settings_factory):
    ''' Returns a json parser '''

    def create_parser(self) -> Settings_parser:
        return json_parser(config)


class yaml_factory(abstract_settings_factory):
    ''' returns a yaml parser'''

    def create_parser(self) -> Settings_parser:
        return yaml_parser(config)
