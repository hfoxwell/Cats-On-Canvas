"""
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        To mass import and export the avatar pictures of students/clients
        within a canvas platform and apply them to the correct accounts
"""

# External imports
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from queue import Queue

# Internal imports
from src import CSV, Canvas, Clients, Config
from src import File as SourceFile
from src import Image, Logger, Settings, Workers, custom_errors


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

    def __init__(self, args: argparse.Namespace) -> None:
        # Constants
        self.SETTINGS_DIRECTORY = "./Settings/"
        self.LOGGING_CONFIG = "log_config.json"
        self.DRY_RUN = args.dry_run
        self.PRODUCERS = args.producers
        self.CONSUMERS = args.consumers
        self.REQUEST_TIMEOUT = args.timeout

        # Variables
        self.settings: Config.Configuration
        self.settings_loader = Settings.SettingsLoader()
        self.settings_parser = Config.YAMLParser()
        self.skipped_users: list[Clients.Client] = []
        self.producers = []
        self.consumers = []

        #######################################
        # Initalise the log
        #######################################
        self.log = Logger.configure_logging("Settings/log_config.json", __name__)

    def check_directories(self, *directory_list) -> None:
        """
        Make sure that CSV and images directories exist.
        Then ensure that there are files contained within.
        """

        # log start of function
        self.log.debug("FILE: Verifying directories {}".format(directory_list))

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
            
            self.log.info('File: "%s" found.', directory)

            # If folder empty, then raise value error
            if not os.listdir(directory):
                self.log.exception(ValueError(f"FILE: Directory EMPTY: {directory}"))
                raise custom_errors.DirectoriesCheckError(
                    f"Directory is empty: {directory}"
                )

    # Main function
    def main(self):
        """Main function for controlling application flow"""
        # Variables
        list_of_clients: list[dict[str, str]] = []
        client_identifier_buffer: Queue[Clients.ClientIdentifier] = Queue()
        client_buffer: Queue[Clients.Client] = Queue()

        #######################################
        ## Debug log current config
        #######################################
        self.log.debug(
            '''
            Configuration:
            \tDry_run: %s| 
            \tSettings_dir: %s|
            \tLogging_config: %s|
            \tProducer_count: %s|
            \tConsumer_count: %s|
            \tRequest_timeout: %s|
            ''',
            self.DRY_RUN,
            self.SETTINGS_DIRECTORY,
            self.LOGGING_CONFIG,
            self.PRODUCERS,
            self.CONSUMERS,
            self.REQUEST_TIMEOUT
        )
        if self.DRY_RUN:
            self.log.info(
                '######### DRY RUN #########'
            )
        
        #######################################
        # Initalise settings for the program
        #######################################
        # Get the settings config from the file
        settings_file_path = self.settings_loader.find_settings_file(
            self.SETTINGS_DIRECTORY
        )
        self.settings: Config.CSVConfig = self.settings_loader.load_settings(
            settings_file_path, self.settings_parser, Config.CSVConfig
        )
        
        #########################################
        # Debug settings file configuration
        #########################################
        self.log.debug(
            '''
            Settings file confgiuration:
            \tWorking_path: %s|
            \tCSV_directory: %s|
            \tImages_directory: %s|
            ''',
            self.settings.working_path,
            self.settings.csv_directory,
            self.settings.images_directory
        )

        #########################################
        # Verify that directories exist
        #########################################

        # Check that files and directories exist
        # Raise custom error 'DirectoriesCheckError'
        # if the directories are not valid
        try:
            self.check_directories(
                self.settings.images_directory, self.settings.csv_directory
            )

        except custom_errors.DirectoriesCheckError:
            message: str = (
                "FILE: Unable to continue without critical directories. Exiting program"
            )
            # Log the error
            self.log.exception(message)

            # exiting program
            sys.exit()

        except ValueError:
            message: str = (
                "FILE: Critical directories do not contain any files. Exiting program"
            )
            # Log error
            self.log.exception(message)

            # Exiting program
            sys.exit()

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
        file_reader: CSV.CSVReader = CSV.CSVReader(source_file=source)
        list_of_clients = file_reader.get_clients()

        ######################################
        # Create users
        #####################################
        # Enqueue all client identifiers
        for client in list_of_clients:
            temp_client = Clients.ClientIdentifier(
                client_id=client["client_id"],
                profile_picture_path=Path(
                    self.settings.images_directory, client["image_filename"]
                ),
                file_type=client["image_filetype"],
                date_uploaded=datetime.now(),
            )
            client_identifier_buffer.put(temp_client)

        # Now that users have been created upload them to canvas
        # if no users have been created. Then EXIT the program
        if client_identifier_buffer.qsize():
            self.log.info(
                "All possible users have been created. A total of %i",
                client_identifier_buffer.qsize(),
            )
            self.log.info("Creating workers.")
        else:
            self.log.warning("USER: no users were found. Exiting..")
            sys.exit(1)

        ########################################
        # Create Producers and Consumers
        ########################################
        self.log.info("Creating %i producers", self.PRODUCERS)
        self.producers = [
            Workers.Producer(
                user_queue=client_buffer,
                available_users=client_identifier_buffer,
                image_factory=Image.ImageFactory(),
            )
            for _ in range(self.PRODUCERS)
        ]

        self.log.info("Creating %i consumers", self.CONSUMERS)
        self.consumers = [
            Workers.Consumer(
                user_queue=client_buffer,
                canvas_connector=Canvas.POST_data_canvas(
                    self.settings.access_token,
                    self.settings.domain,
                    timeout=self.REQUEST_TIMEOUT,
                    dry_run=self.DRY_RUN,
                ),
            )
            for _ in range(self.CONSUMERS)
        ]

        #########################################
        # Start producers and consumers
        #########################################
        self.log.info("Starting Production/Consumption")

        for producer in self.producers:
            producer.start()

        for consumer in self.consumers:
            consumer.start()

        client_identifier_buffer.join()
        client_buffer.join()
        self.log.info("Finished")


def arg_parse():
    """Parse command line arguments"""
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-d", "--dry-run", type=bool, default=False)
    argument_parser.add_argument("-p", "--producers", type=int, default=2)
    argument_parser.add_argument("-c", "--consumers", type=int, default=5)
    argument_parser.add_argument("-t", "--timeout", type=int, default=2)

    return argument_parser.parse_args()


if __name__ == "__main__":
    # Sets up the program and runs the canvas uploader
    # Checks the program state first, then sets up the
    # main object to be used.

    # Check python state
    check_python_version()

    # If module is run by itself then run main
    main_object: object = Main(arg_parse())  # Create main object
    main_object.main()  # Run main from object
