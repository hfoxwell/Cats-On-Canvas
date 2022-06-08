'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        To mass import and export the avatar pictures of students/clients
        within a canvas platform and apply them to the correct accounts
'''

# External imports
import os, sys

# Internal imports
from src.ImageHandler.image_handler import open_image
from src.Logger.log import write_log, write_error
from src.CSV import reader
from src.Clients.user import client
from src.Requests.canvas_requests import POST_data_canvas
from src.Config.config import yaml_factory, json_factory

# Assert python minimum version
assert sys.version_info >= (3,7)

##############################
# FUNCTIONS
##############################
def check_directories(*directories ) -> bool:
    ''' 
    Make sure that CSV and images directories exist.
    Then ensure that there are files contained within.
    '''
    # For all directories passed into funciton 
    # Check if they exist
    for arg in directories:
        if not(os.path.exists(arg)):
            write_error(FileNotFoundError(f'FILE: File or directory MISSING: {arg}'))
            return False
        else:
            write_log(f'File: "{arg}" found.')
    
    # If all directories exist return true
    return True

def Create_student_list(client_list: list[client], img_location:str) -> list[client]:
    ''' Returns a list of user objects'''
    # Variables
    userList: list[client] = []
    
    # Iterate through list from Csv
    for student in client_list:
        
        '''
        TODO: Find a way to create the user object so that MAIN does not need to be aware of clients. 
        This may need a controller or something along those lines. 
        '''
        '''
        TODO: Main is too busy. This needs to be a more single responsiblity function. rewrite this so
        that main is only responsible for working with the controlers. This may mean creating 
        some controllers. 
        '''
        
        write_log(f'Current Student: {student}')

        # confirm user's image exists in directory
        img = open_image(
            img_location,
            student['image_filename']
        )
        # Check if image is null
        # If image is null, no image exists so raise error
        if img == None:
            write_error(FileNotFoundError(f'FILE: {student["image_filename"]} cannot be found'))
            write_log(f'USER: user, {student["client_id"]} Skipped as no image could be found')
            continue
        else:
            # Create user object
            try:
                user: client = client(
                    student['client_id'], 
                    img
                    )
            except:
                # Catch error creating user
                # Write this to log
                write_error(Exception(f'USER: Could not create user {student["client_id"]}'))
                continue

        ###################
        # Print out created user details
        ###################
        print(
            f'Creating User: {user.client_id}',
            f'With Image: {user.image.image_name}',
            sep='\t'
        )

        # Add user object to list of users
        userList.append(user)
    
    ###############################
    # Console & log Number of users
    ###############################
    write_log(
        f'Total of {len(userList)} users created'
    )
    print(
        f'Total of {len(userList)} users created'
    )

    # Return list of user objects
    return userList

def process_user(user: client, connector: POST_data_canvas):
    ''' upload a user to canvas '''
    #Step 0: Get canvas user ID via SIS ID
    if not connector.get_canvas_id(user):
        # If connector cannot get user id skip user
        write_log(f"CANVAS: Skipping user: {user.client_id}")
        return

    # Step 1: Start upload file to user's file storage
    if not connector.upload_user_data(user):
        # if no upload happened log and next student
        write_log(f'CANVAS: Skipping user: {user.client_id} File could not be uploaded')
        return

    # Step 2: Make API call to set avatar image
    if not connector.set_image_as_avatar(user):
        write_error(f'CANVAS: Error changing profile picture for: {user.client_id}')
        return

# Main function
def main():
    ''' Main function for controlling application flow'''
    # Variables
   
    list_of_clients: list[client] = []

    #######################################
    # Initalise settings for the program
    #######################################
    if "json" in os.listdir('./Settings/'):
        conf_parser = json_factory.create_parser()
    else:
        conf_parser = yaml_factory.create_parser()

    conf_parser.read_file(open(file='./Settings/settings.json', encoding='utf-8'))
    settings = conf_parser.load_config()
    
    #########################################
    # Verify that directories exist
    #########################################

    # Check that files and directories exist
    if not(check_directories(
        settings.working_path,
        settings.log_filename,
        settings.images_path,
        settings.csv_directory,
        f'{settings.csv_directory}{settings.csv_filename}'
        )):
        # If directories don't exist then warn user
        print('Program cannot continue due to fatal error processing files')
        return

    write_log("File: Checks Complete. Starting Client Generation")

    ######################################
    # Create CSV reader
    ######################################
    
    file_reader: reader.Reader = reader.csv_reader(f'{settings.csv_directory}{settings.csv_filename}')
    list_of_clients = file_reader.get_clients()

    ######################################
    # Create users
    #####################################
    # For each dictionary in the list
    # log details and create a user object
    user_list = Create_student_list(
        list_of_clients,
        settings.images_path
        )

    # Now that users have been created upload them to canvas
    # if no users have been created. Then EXIT the program
    if (len(user_list)):
        write_log(f'All possible users have been created. A total of {len(user_list)}')
        write_log(f'Creating canvas object...')
    else:
        print("No users were created. Closing application")
        write_error("USER: no users were found. Exiting..")
        exit()
    
    #########################################
    # Create and initalise canvas connector
    #########################################
    try:
        #  Attempt to connect to canvas
        connector = POST_data_canvas(settings.access_token, settings.domain)
        pass
    except:
        # If error is reported in connecting to canvas
        write_error(Exception(f'CONNECTOR: Error connecting to canvas. Exiting application.'))
        print(Exception('Error connecting to canvas, Quitting application'))
        exit()
    write_log("Successfully created canvas connection. Commencing upload.")
    
    ########################################
    # For each user Start upload process
    ########################################
    count_of_uploaded_users:int = 1
    for user in user_list:
        ''' For each student in user list upload data to canvas '''
        
        # Call function to process a user
        process_user(user, connector)
        
        # Confirm in the console that user has been uploaded...
        # Increment after upload is completed
        print(f'Finished {count_of_uploaded_users} of {len(user_list)} users')
        count_of_uploaded_users += 1

if __name__ == '__main__':
    # If module is run by itself then run main
    main()
