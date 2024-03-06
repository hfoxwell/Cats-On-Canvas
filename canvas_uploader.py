"""
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        To mass import and export the avatar pictures of students/clients
        within a canvas platform and apply them to the correct accounts
"""

# External imports
import os, sys


# Internal imports
from src.Image import imageFactory
from src.Logger import configure_logging
from src.CSV import reader

import src.Clients as Clients
import src.File as SourceFile
import src.Canvas as Canvas
import src.custom_errors as custom_errors
import src.Config as Config
import src.Settings as Settings


def check_python_version() -> None:
    """
    Checks the installed python version and exits the program if it's below the
    required version: 3:9:x (major=3, minor=9, micro=0)
    """

    # Python version
    version: tuple[int, int, int] = (3, 9, 0)

    if sys.version_info < version:

        # Print out error message to console
        # Logger is not initialised at this point,
        # so no log is produced
        print(
            f'{"#" * 10} ERROR {"#" * 10}',
            "The currently installed version of python is insufficient to run this program.",
            f"""CURRENT VERSION: {sys.version_info} is less than required Version:
            {version[0]}.{version[1]}.x(major={version[0]}, minor={version[1]}, micro=0)""",
            sep="\n \t",
        )

        # Close the program if the python
        # version is below the required value
        exit()


##############################
# FUNCTIONS
##############################
class Main:
    """
    This is the main entry for the program
    """
    # Constants
    SETTINGS_DIRECTORY = './Settings/'

    # Class variables
    settings: Config.Config
    
    def __init__(self) -> None:
        self.settings_loader = Settings.SettingsLoader()
        self.settings_parser = Config.YAML_Parser()

    def check_directories(self, *directory_list) -> None:
        """
        Make sure that CSV and images directories exist.
        Then ensure that there are files contained within.
        """

        # log start of function
        self.log.info("FILE: Verifying directories {}".format(directory_list))

        # Verify the folders
        for directory in directory_list:

            # If directory does not exist
            # raise error informing user that
            # directory is non-existant
            if not os.path.exists(directory):
                self.log.exception(
                    FileNotFoundError(f"FILE: Directory MISSING: {directory}")
                )
                raise custom_errors.DirectoriesCheckError(
                    f"Directory missing: {directory}"
                )
            else:
                self.log.info(f'File: "{directory}" found.')

            # If folder empty, then raise value error
            if not os.listdir(directory):
                self.log.exception(ValueError(f"FILE: Directory EMPTY: {directory}"))
                raise custom_errors.DirectoriesCheckError(
                    f"Directory is empty: {directory}"
                )

    def Create_student_list(
        self, client_list: list[dict[str, str]], img_location: str
    ) -> list[Clients.client]:
        """Returns a list of user objects"""
        # Variables
        userList: list[Clients.client] = []

        # Iterate through list from Csv
        for student in client_list:

            # Write to logfile the current student being processed
            self.log.info(f"Current Student: {student}")

            # confirm user's image exists in directory
            try:
                # Create an image factory object and validate image creation.
                imgFactory: imageFactory = imageFactory(
                    img_location, student["image_filename"]
                )
            except OSError as e:
                # if error raised by factory, image does not exits.
                self.log.exception(
                    FileNotFoundError(f'FILE: {e} {student["image_filename"]}')
                )
                self.log.info(
                    f'USER: user, {student["client_id"]} Skipped as no image could be found'
                )
                continue

            # Create user object
            try:
                user: Clients.client = Clients.client(
                    student["client_id"], imgFactory.open_image()
                )
            except Exception as user_error:
                # Catch error creating user
                # Write this to log
                self.log.exception(
                    f'USER: Could not create user {student["client_id"]} : {user_error}'
                )
                continue

            ###################
            # Print out created user details
            ###################
            self.log.info(
                f"Creating User: {user.client_id}\t\n" +
                f"With Image: {user.image.image_name}",
            )

            # Add user object to list of users
            userList.append(user)

        ###############################
        # Console & log Number of users
        ###############################
        self.log.info(f"Total of {len(userList)} users created")

        # Return list of user objects
        return userList

    def process_user(self, user: Clients.client, connector: Canvas.POST_data_canvas):
        """upload a user to canvas"""
        # Step 0: Get canvas user ID via SIS ID
        if not connector.get_canvas_id(user):
            # If connector cannot get user id skip user
            self.log.info(f"CANVAS: Skipping user: {user.client_id}")
            return

        # Step 1: Start upload file to user's file storage
        if not connector.upload_user_data(user):
            # if no upload happened log and next student
            self.log.info(
                f"CANVAS: Skipping user: {user.client_id} File could not be uploaded"
            )
            return

        # Step 2: Make API call to set avatar image
        if not connector.set_image_as_avatar(user):
            self.log.warning(
                f"CANVAS: Error changing profile picture for: {user.client_id}"
            )
            return

    # Main function
    def main(self):
        """Main function for controlling application flow"""
        # Variables

        list_of_clients: list[Clients.client] = []

        #######################################
        # Initalise settings for the program
        #######################################
        # Get the settings config from the file
        settings_file_path = self.settings_loader.find_settings_file(self.SETTINGS_DIRECTORY)
        self.settings = self.settings_loader.load_settings(settings_file_path, self.settings_parser)

        #######################################
        # Initalise the log
        #######################################
        self.log = configure_logging("Settings/log_config.json", __name__)

        #########################################
        # Verify that directories exist
        #########################################

        # Check that files and directories exist
        # Raise custom error 'DirectoriesCheckError'
        # if the directories are not valid
        try:
            self.check_directories(
                self.settings.images_path, self.settings.csv_directory
            )

        except custom_errors.DirectoriesCheckError:
            message: str = (
                f"FILE: Unable to continue without critical directories. Exiting program"
            )
            # Log the error
            self.log.exception(message)

            # exiting program
            exit()

        except ValueError:
            message: str = (
                f"FILE: Critical directories do not contain any files. Exiting program"
            )
            # Log error
            self.log.exception(message)

            # Exiting program
            exit()

        self.log.info("File: Checks Complete. Starting Client Generation")

        ######################################
        # Create sourcefile
        ######################################
        source: SourceFile.sourceFile = SourceFile.csv_Source(
            f"{self.settings.csv_directory}{self.settings.csv_filename}"
            )
        
        ######################################
        # Create reader
        ######################################
        file_reader: reader.Reader = reader.csv_reader(
            sourceFile=source
        )
        list_of_clients = file_reader.get_clients()

        ######################################
        # Create users
        #####################################
        # For each dictionary in the list
        # log details and create a user object
        user_list = self.Create_student_list(list_of_clients, self.settings.images_path)

        # Now that users have been created upload them to canvas
        # if no users have been created. Then EXIT the program
        if len(user_list) > 0:
            self.log.info(
                f"All possible users have been created. A total of {len(user_list)}"
            )
            self.log.info("Creating canvas object...")
        else:
            self.log.warning("USER: no users were found. Exiting..")
            exit()

        #########################################
        # Create and initialise canvas connector
        #########################################
        try:
            #  Attempt to connect to canvas
            connector = Canvas.POST_data_canvas(
                self.settings.access_token, self.settings.domain
            )

        except Exception as e:
            # If error is reported in connecting to canvas
            self.log.critical(
                    "CONNECTOR: Error connecting to canvas: {}".format(e)
                )
            exit()

        self.log.info("Successfully created canvas connection. Commencing upload.")

        ########################################
        # For each user Start upload process
        ########################################
        count_of_uploaded_users: int = 1
        for user in user_list:
            """For each student in user list upload data to canvas"""

            # Call function to process a user
            self.process_user(user, connector)

            # Confirm in the console that user has been uploaded...
            # Increment after upload is completed
            self.log.info(f"Finished {count_of_uploaded_users} of {len(user_list)} users")
            count_of_uploaded_users += 1


if __name__ == "__main__":
    """
    Sets up the program and runs the canvas uploader
    Checks the program state first, then sets up the
    main object to be used.
    """

    # Check python state
    check_python_version()

    # If module is run by itself then run main
    main_object: object = Main()  # Create main object
    main_object.main()  # Run main from object
