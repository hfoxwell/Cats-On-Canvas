'''
Author: H Foxwell
Date: 25/02/2024
Purpose:
    Class used to separate some respnsibility from the main file regarding the
    processing of the config.
'''
# External imports
import os
import mimetypes


class SettingsLoader:
    ''' Class used to create configuration object'''

    def find_settings_file(self, directory: str) -> str:
        ''' Finds the settings file in the given directory'''

        # Variables
        settings_file_list: list[str] = os.listdir(directory)

        # For all files in the given directory
        for setting_file in settings_file_list:
            # If a Yaml file is found in directory
            # return the filepath of the settings file
            if ".yaml" in setting_file:
                return f"./Settings/{setting_file}"
        # If the file cannot be found, raise and error
        raise FileNotFoundError("Settings file cannot be found.")

    def load_settings(self, file_path: str, parser):
        ''' Creates the settings parser object using the file path from 'find_settings_file'''
        # Open file path
        with open(file=file_path, encoding="utf-8") as settings_file:
            # If file cannot be opened or processed
            if not (parser.read_file(settings_file)):
                raise FileNotFoundError("Settings file cannot be found.")
        return parser.load_config()