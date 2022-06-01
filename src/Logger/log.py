'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for logging to file
'''
# External imports
from datetime import datetime
import os, json

# internal imports

# File module
# Global variables
settings = json.load(open(file='./Settings/settings.json', encoding='utf-8'))
log_file_name:str = settings['log_filename']
log_file_path:str = f'{settings["working_path"]}{settings["log_filename"]}'


# Check if logfile exitsts
file_exits = os.path.exists(log_file_path)

try:
    if file_exits:
        # If file exists open file for append
        log_file = open(log_file_path,'a')
        log_file.write("#" * 10)
        log_file.write(f'Log file opened @ {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        log_file.write("#" * 10)
        log_file.write('\n')
    else:
        # If file does not exist, create file for writing
        log_file = open(log_file_path,'x')
        
        # Write log created
        log_file.write('#' * 20)
        log_file.write("log file Created @ {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        log_file.write(f'{"#" * 20}\n')

except OSError:
    print(f'Error creating/accessing log file {log_file_name}, Error: {OSError}')
    exit()

def write_log(*content) -> int:
    ''' Writes to the log file automatically appends time'''
    try:
        for item in content:
            log_file.write(f'{item} @ {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
    except OSError:
        print(f'Error writing to log file {log_file_name}, Error: {OSError}\n')
    
def write_error(error):
    ''' Writes an error to log '''
    write_log(f'The following error occured: {error}\n')

def close_log():
    ''' Closes the log file '''
    write_log(f'Closing Log file {log_file_name}')
    log_file.close()
