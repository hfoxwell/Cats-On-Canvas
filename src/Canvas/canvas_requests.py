"""
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        Class for handling the requests to the remote
        server and the canvas API.
"""

# External imports
from abc import ABC, abstractmethod
import json
import logging
import requests

# Internal imports
from src.Clients import Client


class Canvas_connector(ABC):
    """Abstract base class for canvas connector"""

    @abstractmethod
    def set_user(self, user: Client):
        '''Sets the user for the object'''

    @abstractmethod
    def get_canvas_id(self) -> bool:
        """Gets internal canvas ID from student ID in SIS. Returns bool (true) on success"""

    @abstractmethod
    def upload_user_data(self) -> bool:
        """Uploads user data to canvas. Returns bool (true) on success"""

    @abstractmethod
    def set_image_as_avatar(self) -> bool:
        """Sets and image to be a users PFP"""


class POST_data_canvas(Canvas_connector):
    """Posts data to canvas"""

    def __init__(self, Token: str, domain: str, timeout: int, dry_run = False) -> None:
        """For passing information to canvas"""
        self.auth_token: str = Token
        self.domain: str = f"https://{domain}/api/v1"
        self.header: dict = {"Authorization": f"Bearer {self.auth_token}"}
        self.params: dict = {}
        self.upload_params: dict = {}
        self.user: Client = None
        self.timeout = timeout
        self.dry_run = dry_run

        # Logger instance
        self.log: logging.Logger = logging.getLogger(__name__)

        # Log initialised values
        self.log.debug(
            """
            CANVAS: initialised values:
            Auth Token:\t %s
            Domain:\t %s
            Header:\t %s
            Params:\t %s
            """,
            self.auth_token,
            self.domain,
            self.header,
            self.params,
        )
        # Call Canvas Test function
        self._test_canvas_connection()

    def _test_canvas_connection(self):
        """Validates that connection to canvas can be made"""
        # Variables
        desired_result: int = 200

        res: requests.Response = requests.get(
            f"{self.domain}/accounts",
            self.params, 
            headers=self.header,
            timeout=self.timeout
        )
        res.raise_for_status()

        # If result 200 then return true
        if res.status_code == desired_result:
            self.log.info("CANVAS: Connection Successfully Tested")
            
    def set_user(self, user: Client):
        '''sets the user'''
        self.user = user

    def get_canvas_id(self):
        """Gets a user ID from Canvas"""
        # Write log with user ID
        self.log.info(f"USER: Getting Canvas ID for: {self.user.client_id}")

        # Send get request for a user's canvas id. This is
        # different from their SIS id
        user_Details: requests.Response = requests.get(
            f"{self.domain}/users/sis_user_id:{self.user.client_id}",
            headers=self.header,
            params=self.params,
            timeout=self.timeout
        )

        # Check if id is in the json response.
        if "id" in user_Details.json():
            # User ID found then change the users SIS id to match
            self.user.client_id = user_Details.json()["id"]
            
        else:
            # If not found, return an error to the log with the SIS id
            self.log.exception(f"USER: {self.user.client_id} cannot be found in canvas")
            user_Details.raise_for_status()

    def upload_user_data(self):
        """Upload image to users files"""
        self.log.info('Starting upload of profile picture for: %s', self.user.client_id)
        
        # Account for dry run
        if self.dry_run:
            # Notify users that a dry run upload is occurring
            self.log.info(
                "######## DRY RUN UPLOAD ########"
            )
            # Exit function early
            return 
        
        # Variables
        self.upload_params = {}
        url: str = self.domain + "/users/self/files"
        inform_parameters = {
            "name": self.user.image.image_name,
            "size": self.user.image.image_size,  # read the filesize
            "content_type": self.user.image.file_type,
            "parent_folder_path": "profile pictures",
            "as_user_id": self.user.client_id,
        }

        # Prepare Canvas for upload
        response: requests.Response = requests.post(
            url, headers=self.header, 
            data=inform_parameters,
            timeout=self.timeout
        )
        response.raise_for_status()

        # Debug the response from prepare upload
        self.log.debug('Upload Preparation: %s', response.text)

        # Get response and send data
        json_res = json.loads(response.text)

        # Prepare data
        # Get file data from image object
        files = {"file": self.user.image.image_file}

        # Set the params to the params based on the response from canvas
        # These must be identical to the params received from canvas.
        # Else this will fail
        try:
            self.upload_params = json_res["upload_params"]
        except KeyError as e:
            self.log.error(
                "Upload Parameters could not be set: %s. The following response was returned %s",
                e,
                response.text
            )
            return False
        # Send the file to canvas
        # Get upload confirmation
        upload_file_response = requests.post(
            json_res["upload_url"], 
            data=self.upload_params, 
            files=files, 
            allow_redirects=False,
            timeout=self.timeout
        )
        upload_file_response.raise_for_status()

        self.log.debug('Upload file response: %s', upload_file_response.text)

        status_code: int = upload_file_response.status_code
        # The response from canvas can either be 201 or 3XX
        # A 300+ response requires a confirmation from the app
        # A 201 is a confirmation and a get will return the file id
        if status_code == 201 or status_code >= 300:
            # Get file upload confirmation and file ID
            confirmation = requests.get(
                upload_file_response.headers["location"], 
                headers=self.header,
                timeout=self.timeout
            )
            confirmation.raise_for_status()
            self.log.debug('Upload Confirmation: %s', confirmation.text)

        else:
            # If another value returns then there was an issue
            # Exit the application
            self.log.error("CANVAS: File upload Failed")
            return False

        # Get file ID From canvas
        if "id" in confirmation.json():
            # If file ID is found then set it for the image
            self.user.image.image_canvas_id = confirmation.json()["id"]
        else:
            self.log.error("CANVAS: No file ID found for uploaded file")

        # Successfully uploaded file
        self.log.info('Successfully uploaded file.')
        return True

    def set_image_as_avatar(self):
        """Sets and image to be a users PFP"""
        # Log that Canvas avatar is being updated
        self.log.info(
            "Setting canvas Avatar for: %s to: %s",
            self.user.client_id,
            self.user.image.image_name
        )
        
        # Notify user of dry run
        if self.dry_run:
            self.log.info(
                "######## DRY RUN SET OF AVATAR ########"
            )
            # Exit function early
            return

        # Check that upload params contains values
        if self.upload_params == {}:
            self.log.error(
                "Upload params is empty, cannot set image avatar."
            )
            return False


        # Set parameters as the user_id
        self.upload_params = {"as_user_id": f"{self.user.client_id}"}

        # Get-Request the user avatars images, to get image id
        avatar_options = requests.get(
            f"{self.domain}/users/{self.user.client_id}/avatars",
            headers=self.header,
            params=self.upload_params,
            timeout=self.timeout
        )
        avatar_options.raise_for_status()

        # Debug response
        self.log.debug('Avatar Options: %s',avatar_options.text)

        # As there are multiple avatars that come stock with canvas
        # the program needs to iterate through the avatars to find
        # the image that was uploaded.
        for avatar_opts in avatar_options.json():

            # If the current avatar has the same name as the uploaded image
            # Set params to be 'user[avatar][token] = <token>.
            # The image token is unique to each request. So cannot be
            # relied on between sessions.
            if avatar_opts.get("display_name") == self.user.image.image_name:
                self.upload_params["user[avatar][token]"] = avatar_opts.get("token")

            # Create put request to tell canvas to update pfp
            # This is done as a put to prevent POST from regenerating
            # outputs
            set_avatar_user = requests.put(
                f"{self.domain}/users/{self.user.client_id}",
                headers=self.header,
                params=self.upload_params,
                timeout=self.timeout
            )
            set_avatar_user.raise_for_status()
            self.log.debug('Set avatar: %s', set_avatar_user.text)

        # If the canvas response is 200, then the update has been successful
        if set_avatar_user.status_code == 200:
            self.log.info('success updating user avatar for: %s', {self.user.client_id})

            return True
        else:
            # If the update was not successful, log the result
            self.log.error(
                f"CANVAS: Error updating avatar for: {self.user.client_id},"
                + f" error: {set_avatar_user.status_code}"
            )
            return False
