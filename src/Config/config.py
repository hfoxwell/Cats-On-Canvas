'''
    Author: H Foxwell
    Date:   04/06/2022
    Purpose:
        Class for parsing and storing settings.
'''

# External imports
import logging
from dataclasses import dataclass

try:
    import yaml
except ImportError as e:
    raise ImportError(f"Cannot import YAML parsing package: {e}")

# Create logger
log = logging.getLogger(__name__)

#Base Class configuration
@dataclass
class Configuration:
    '''Base class for configuration'''
    working_path: str = ""
    # Canvas access settings
    access_token: str = ""
    domain: str = ""


# Classes
@dataclass()
class CSVConfig(Configuration):
    '''Store the settings config'''
    # Directory settings
    csv_directory: str = ""
    images_directory: str = ""
    # File settings
    csv_filename: str = ""


class YAMLParser():
    '''Parses yaml settings'''

    def __init__(self) -> None:
        self.Settings_contents = None

    def read_file(self, settings_file) -> bool:
        ''' Read the config from Yaml file '''
        try:
            # Read the yaml file
            self.Settings_contents = yaml.safe_load(settings_file)

        except yaml.YAMLError as exc:
            # Handle YAML parsing errors
            log.error("Error reading YAML file: %s",exc)
            return False

        # Indicate successful reading of settings
        log.info("SUCCESS: Settings Loaded")
        return True

    def load_config(self, configuration_class) -> object:
        ''' Load a config '''
        # Initialize an empty configuration object
        conf = configuration_class()

        # Update configuration object with settings from YAML file
        for section, options in self.Settings_contents.items():
            for key, value in options.items():
                # Check if the attribute exists in the configuration class
                if hasattr(conf, key):
                    # Set the attribute value dynamically
                    setattr(conf, key, value)
                else:
                    log.warning("Warning: Ignoring unknown setting '%s'", key)

        return conf