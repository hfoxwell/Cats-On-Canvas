'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for logging to file
'''
# External imports
from datetime import date
import os

from matplotlib.pyplot import close
from prometheus_client import write_to_textfile

# internal imports

# File Class
class logger():

    def __init__(self,ln:str, p:str, wd:str) -> None:
        '''
            initalise the logger.
                ln - Log name
                p - path
                wd - working directory
        '''
        self.log_file_name:str = ln
        self.log_file_path:str = p
        self.working_dir:str = wd

        # Check if logfile exitsts
        file_exits = os.path.exists('{0}{1}'.format(self.working_dir, self.log_file_path))
        
        try:
            if file_exits:
                # If file exists open file for append
                self.log_file = open(self.log_file_name,'a')
                self.log_file.write("Log file opened @ {}".format(date.today()))
            else:
                # If file does not exist, create file for writing
                self.log_file = open(self.log_file_name,'x')
                
                # Write log created
                self.log_file.write("#" * 20)
                self.log_file.write("log file Created @ {}".format(date.today()))
                self.log_file.write("#" * 20)
        except OSError:
            print(f'Error creating log file {self.log_file_name}, Error: {OSError}')
            exit()

    def write_log(self, content:str) -> int:
        ''' Writes to the log file automatically appends time'''
        try:
            self.log_file.write(f'{content} @ {date.today()}')
        except OSError:
            print(f'Error writing to log file {self.log_file_name}, Error: {OSError}')

    def write_error(self, error):
        ''' Writes an error to log '''
        self.write_log(f'The following error occured: {error}')

    def close_log(self):
        ''' Closes the log file '''
        self.write_log(f'Closing Log file {self.log_file_name}')
        self.log_file.close()
