'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        To mass import and export the avatar pictures of students/clients
        within a canvas platform and apply them to the correct accounts
'''

# External imports
import json, os

from requests import JSONDecodeError



# Internal imports


def check_directories():
    ''' 
    Make sure that CSV and images directories exist.
    Then ensure that there are files contained within.
    '''



# Main function
def main():
    ''' Main function for controlling application flow'''
    # initalise program log
    
    # Initalise settings for the program
    try:
        settings = json.load(open(file='./Settings/settings.json', encoding='utf-8'))
    except:
        print("JSONDecodeError()
        return
    
    # Check that files and directories exist
    check_directories(
        settings['working_path'], 
        settings['csv_filename'],
        settings['images_path']
        )

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