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
from src.Image import imageFactory
from src.Logger import logger
from src.CSV import reader
from src.Clients import client
from src.Requests import POST_data_canvas
from src.Config import config

def check_python_version() -> None:
    '''
    Checks the installed python version and exits the program if it's below the
    required version: 3:9:x (major=3, minor=9, micro=0)
    '''
    
    # Python version
    version: tuple[int, int, int] = (3, 9, 0)
    
    if ( sys.version_info < version ):
        
        # Print out error message to console
        # Logger is not initialised at this point,
        # so no log is produced
        print(
            f'{"#" * 10} ERROR {"#" * 10}',
            "The currently installed version of python is insufficient to run this program.",
            f'''CURRENT VERSION: {sys.version_info} is less than required Version:
            {version[0]}.{version[1]}.x(major={version[0]}, minor={version[1]}, micro=0)''',
            sep='\n \t'
        )
        
        # Close the program if the python
        # version is below the required value
        exit()


##############################
# FUNCTIONS
##############################
class main():
    '''
        This is the main entry for the program
    '''
    # Class variables
    log: logger = None
    settings: config = None

    def get_settings(self, dir: str):
        ''' Load the settings object '''
        
        '''
            TODO: #18 variable is always taken from the first element of the ./Settings directory.
            It would be better to iterate over all files in the directory and try to load each 
            one until a valid file is found.
        '''

        # Variables
        settings_fileList: list[str] = os.listdir(dir)
        factory: config.abstract_settings_factory = None

        # for all files in the directory
        #   check each file for json or yaml
        for setting_file in settings_fileList:
            # Determine the settings file format
            if ".json" in setting_file:
                # if settings is json format create json parser
                factory = config.json_factory()
                break

        if factory is None:
            # if settings is yaml format create yaml parser
            factory = config.yaml_factory()

        # Create new parser from the instantiated factory
        conf_parser = factory.create_parser()

        # read the settings file using the new parser
        with open(file=f'./Settings/{settings_fileList[0]}') as settingsFile:
            if not(conf_parser.read_file(settingsFile)):
                print('Failed to load settings: Exiting application')
                exit()

        # return the config object to the program
        return conf_parser.load_config()

    def check_directories(self, *directories ) -> bool:
        '''
        Make sure that CSV and images directories exist.
        Then ensure that there are files contained within.
        '''
        
        '''
            TODO: #19 function always returns True if all directories exist. 
            However, it would be better to return False if any directory is missing or empty.
        '''
        
        # For all directories passed into function 
        # Check if they exist
        for arg in directories:
            if not(os.path.exists(arg)):
                self.log.write_error(FileNotFoundError(f'FILE: File or directory MISSING: {arg}'))
                return False
            else:
                self.log.write_log(f'File: "{arg}" found.')

        # If all directories exist return true
        return True

    def Create_student_list(self, client_list: list[client], img_location:str) -> list[client]:
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
            TODO: Main is too busy. This needs to be a more single responsibility function. rewrite this so
            that main is only responsible for working with the controllers. This may mean creating
            some controllers.
            '''

            self.log.write_log(f'Current Student: {student}')

            # confirm user's image exists in directory
            try:
                # Create an image factory object and validate image creation.
                imgFactory: imageFactory = imageFactory(img_location, student['image_filename'])
            except OSError as e:
                # if error raised by factory, image does not exits.
                self.log.write_error(FileNotFoundError(f'FILE: {e} {student["image_filename"]}'))
                self.log.write_log(f'USER: user, {student["client_id"]} Skipped as no image could be found')
                continue

            # Create user object
            try:
                user: client = client(
                    student['client_id'],
                    imgFactory.open_image()
                    )
            except Exception as userError:
                # Catch error creating user
                # Write this to log
                self.log.write_error(f'USER: Could not create user {student["client_id"]} : {userError}')
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
        self.log.write_log(
            f'Total of {len(userList)} users created'
        )
        print(
            f'Total of {len(userList)} users created'
        )

        # Return list of user objects
        return userList

    def process_user(self, user: client, connector: POST_data_canvas):
        ''' upload a user to canvas '''
        #Step 0: Get canvas user ID via SIS ID
        if not connector.get_canvas_id(user):
            # If connector cannot get user id skip user
            self.log.write_log(f"CANVAS: Skipping user: {user.client_id}")
            return

        # Step 1: Start upload file to user's file storage
        if not connector.upload_user_data(user):
            # if no upload happened log and next student
            self.log.write_log(f'CANVAS: Skipping user: {user.client_id} File could not be uploaded')
            return

        # Step 2: Make API call to set avatar image
        if not connector.set_image_as_avatar(user):
            self.log.write_error(f'CANVAS: Error changing profile picture for: {user.client_id}')
            return

    # Main function
    def main(self):
        ''' Main function for controlling application flow'''
        # Variables

        list_of_clients: list[client] = []

        #######################################
        # Initalise settings for the program
        #######################################
        # Get the settings config from the file
        self.settings = self.get_settings('Settings/')

        #######################################
        # Initalise the log
        #######################################
        self.log = logger(self.settings)

        #########################################
        # Verify that directories exist
        #########################################

        # Check that files and directories exist
        if not(self.check_directories(
            self.settings.working_path,
            self.settings.log_filename,
            self.settings.images_path,
            self.settings.csv_directory,
            f'{self.settings.csv_directory}{self.settings.csv_filename}'
            )):
            # If directories don't exist then warn user
            print('Program cannot continue due to fatal error processing files')
            return

        self.log.write_log("File: Checks Complete. Starting Client Generation")

        ######################################
        # Create CSV reader
        ######################################

        file_reader: reader.Reader = reader.csv_reader(f'{self.settings.csv_directory}{self.settings.csv_filename}')
        list_of_clients = file_reader.get_clients()

        ######################################
        # Create users
        #####################################
        # For each dictionary in the list
        # log details and create a user object
        user_list = self.Create_student_list(
            list_of_clients,
            self.settings.images_path
            )

        # Now that users have been created upload them to canvas
        # if no users have been created. Then EXIT the program
        if (len(user_list)):
            self.log.write_log(f'All possible users have been created. A total of {len(user_list)}')
            self.log.write_log(f'Creating canvas object...')
        else:
            print("No users were created. Closing application")
            self.log.write_error("USER: no users were found. Exiting..")
            exit()

        #########################################
        # Create and initialise canvas connector
        #########################################
        try:
            #  Attempt to connect to canvas
            connector = POST_data_canvas(self.settings.access_token, self.settings.domain, self.log)
            pass
        except:
            # If error is reported in connecting to canvas
            self.log.write_error(Exception(f'CONNECTOR: Error connecting to canvas. Exiting application.'))
            print(Exception('Error connecting to canvas, Quitting application'))
            exit()
        self.log.write_log("Successfully created canvas connection. Commencing upload.")

        ########################################
        # For each user Start upload process
        ########################################
        count_of_uploaded_users:int = 1
        for user in user_list:
            ''' For each student in user list upload data to canvas '''

            # Call function to process a user
            self.process_user(user, connector)

            # Confirm in the console that user has been uploaded...
            # Increment after upload is completed
            print(f'Finished {count_of_uploaded_users} of {len(user_list)} users')
            count_of_uploaded_users += 1

if __name__ == '__main__':
    '''
        Sets up the program and runs the canvas uploader
        Checks the program state first, then sets up the 
        main object to be used.
    '''
    
    # Check python state
    check_python_version()
    
    
    # If module is run by itself then run main
    main = main()       # Create main object
    main.main()         # Run main from object
