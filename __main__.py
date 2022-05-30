'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        To mass import and export the avatar pictures of students/clients
        within a canvas platform and apply them to the correct accounts
'''

# External imports
import json, os

# Internal imports
from src.Logger.log import logger
from src.CSV import reader

def check_directories(log:logger, *directories ) -> bool:
    ''' 
    Make sure that CSV and images directories exist.
    Then ensure that there are files contained within.
    '''
    # For all directories passed into funciton 
    # Check if they exist
    for arg in directories:
        if not(os.path.exists(arg)):
            log.write_error(FileNotFoundError(f'File or directory MISSING: {arg}'))
            return False
        else:
            log.write_log(f'File: "{arg}" found.')
    
    # If all directories exist return true
    return True

# Main function
def main():
    ''' Main function for controlling application flow'''

    # Initalise settings for the program
    try:
        # Open json file for settings
        settings = json.load(open(file='./Settings/settings.json', encoding='utf-8'))
    
    except:
        print("Error reading settings file! Please ensure file exists and is valid!")
        return

    # Iitalise program log
    log = logger(settings['log_filename'], '', settings['working_path'])
    
    # Check that files and directories exist
    if not(check_directories(
        log,
        settings['working_path'], 
        settings['csv_filename'],
        settings['images_path']
        )):
        print('Program cannot continue due to fatal error processing files')
        return

    log.write_log("File: Checks Complete. Starting Client Generation")


    # Create CSV reader
    file_reader: reader.Reader = reader.csv_reader(settings['csv_filename'])
    list_of_clients = file_reader.get_clients(log)

    for student in list_of_clients:
        log.write_log(f'Current Student: {student.client_id} {student.image_path} {student.image_type}')

        # confirm user's image exists in directory


        #Step 0: Get canvas user ID via SIS ID

        # Step 1: Start upload file to user's file storage

        # Step 2: Upload Data

        # Step 3: Confirm Upload

        # Step 4: Make API call to set avatar image
    pass

if __name__ == '__main__':
    # If module is run by itself then run main
    main()