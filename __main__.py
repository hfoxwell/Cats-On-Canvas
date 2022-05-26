'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        To mass import and export the avatar pictures of students/clients
        within a canvas platform and apply them to the correct accounts
'''

# External imports
import json



# Internal imports


# Main function


def main():
    ''' Main function for controlling application flow'''
    # Initalise settings for the program
    settings = json.load(open(file='./Settings/settings.json', encoding='utf-8'))
    
    # Initalise objects

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