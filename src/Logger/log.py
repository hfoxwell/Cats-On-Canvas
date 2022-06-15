'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for logging to file
'''
# External imports
from datetime import datetime
import os

# internal imports
from src.Config.config import config

# Class for file
class logger:
    ''' Class for logging events '''
    
    def __init__(self,settings:config) -> None:
        ''' Initalise the logger'''

        # Variables 
        self.log_file_path = settings.working_path
        self.log_file_name = settings.log_filename
        self.log_file = None

        ''' Create the log file '''
        # Check if logfile exitsts
        log_path: str = f'{self.log_file_path}{self.log_file_name}'
        file_exits = os.path.exists(log_path)

        try:
            if file_exits:
                # If file exists open file for append
                self.log_file = open(log_path,'a')
                self.log_file.write("#" * 10)
                self.log_file.write(f'Log file opened @ {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
                self.log_file.write("#" * 10)
                self.log_file.write('\n')
            else:
                # If file does not exist, create file for writing
                self.log_file = open(log_path,'x')
                
                # Write log created
                self.log_file.write('#' * 20)
                self.log_file.write("log file Created @ {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
                self.log_file.write(f'{"#" * 20}\n')

        except OSError as e:
            print(f'Error creating/accessing log file {self.log_file_name}, Error: {e}')
            exit()

    @staticmethod
    def write_log(self, *content) -> bool:
        ''' Writes to the log file automatically appends time'''
        try:
            for item in content:
                self.log_file.write(f'{item} @ {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
        except OSError as e:
            print(f'Error writing to log file {self.log_file_name}, Error: {e}\n')
            return False
        return True
    
    def write_error(self, error):
        ''' Writes an error to log '''
        self.write_log(f'The following error occured: {error}\n')

    def close_log(self):
        ''' Closes the log file '''
        self.log_file.close()
