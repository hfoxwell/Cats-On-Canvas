'''
    Author: H Foxwell
    Date:   04/06/2022
    Purpose:
        Class for parsing and storing settings.
'''

# External imports
from dataclasses import dataclass

try:
    import yaml
except ImportError as e:
    raise ImportError(f"Cannot import YAML parsing package: {e}")

# Internal Imports


# Classes
@dataclass()
class Config():
    '''Store the settings config'''
    # Directory settings
    working_path: str
    csv_directory: str
    images_path: str

    # Canvas access settings
    access_token: str
    domain: str

    # File settings
    csv_filename: str


class YAML_Parser():
    '''Parses yaml settings'''

    def __init__(self) -> None:
        self.configuration: Config = Config
        self.Settings_contents = None

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

    def load_config(self) -> Config:
        ''' load a config'''
        
        conf = self.configuration(
            working_path=self.Settings_contents['Directories']['working_path'],
            access_token=self.Settings_contents['Canvas_data']['access_token'],
            domain=self.Settings_contents['Canvas_data']['domain'],
            csv_directory=self.Settings_contents['Directories']['csv_directory'],
            csv_filename=self.Settings_contents['File_names']['csv_filename'],
            images_path=self.Settings_contents['Directories']['images_directory'],
        )

        return conf