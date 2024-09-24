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
from src.Clients import client


class Canvas_connector(ABC):
    """Abstract base class for canvas connector"""

    @abstractmethod
    def get_canvas_id(self, user: client) -> bool:
        """Gets internal canvas ID from student ID in SIS. Returns bool (true) on success"""

    @abstractmethod
    def upload_user_data(self, user: client) -> bool:
        """Uploads user data to canvas. Returns bool (true) on success"""

    @abstractmethod
    def set_image_as_avatar(self, user: client) -> bool:
        """Sets and image to be a users PFP"""


class POST_data_canvas(Canvas_connector):
    """Posts data to canvas"""

    def __init__(self, Token: str, domain: str) -> None:
        """For passing information to canvas"""
        self.Session = requests.Session()
        # TODO: implement the sessions system from requests, to save on request information
        self.Auth_token: str = Token
        self.domain: str = f"https://{domain}/api/v1"
        self.header: dict = {"Authorization": f"Bearer {self.Auth_token}"}
        self.params: dict = {}
        self.upload_params: dict = {}

        self.Session.headers.update()

        # Logger instance
        self.log: logging.Logger = logging.getLogger(__name__)

        # Log initialised values
        self.log.info(
            "CANVAS: initialised values:\n" +
            f"Auth Token:\t {self.Auth_token}\n" +
            f"Domain:\t {self.domain}\n" +
            f"Header:\t {self.header}\n" +
            f"Params:\t {self.params}\n"
        )
        # Call Canvas Test function
        self.test_canvas_connection()

    def test_canvas_connection(self):
        """Validates that connection to canvas can be made"""
        # Variables
        desired_result: int = 200

        res: requests.Response = requests.get(
            f"{self.domain}/accounts", self.params, headers=self.header
        )
        res.raise_for_status()

        if res.status_code == desired_result:
            # If result 200 then return true
            self.log.info("CANVAS: Connection Successfully Tested")
            return True
        

    def get_canvas_id(self, user: client) -> bool:
        """Gets a user ID from Canvas"""
        # Write log with user ID
        self.log.info(f"USER: Getting Canvas ID for: {user.client_id}")

        # Send get request for a user's canvas id. This is
        # different from their SIS id
        user_Details: requests.Response = requests.get(
            f"{self.domain}/users/sis_user_id:{user.client_id}",
            headers=self.header,
            params=self.params,
        )

        # Check if id is in the json response.
        if "id" in user_Details.json():
            # User ID found then change the users SIS id to match
            user.client_id = user_Details.json()["id"]
            return True
        else:
            # If not found, return an error to the log with the SIS id
            self.log.exception(f"USER: {user.client_id} cannot be found in canvas")
            user_Details.raise_for_status()

    def upload_user_data(self, user: client) -> bool:
        """Upload image to users files"""
        # Variables
        self.upload_params = {}
        url: str = self.domain + "/users/self/files"
        inform_parameters = {
            "name": user.image.image_name,
            "size": user.image.image_size,  # read the filesize
            "content_type": user.image.file_type,
            "parent_folder_path": "profile pictures",
            "as_user_id": user.client_id,
        }

        # Prepare Canvas for upload
        response: requests.Response = requests.post(
            url, headers=self.header, data=inform_parameters
        )

        response.raise_for_status()

        # json_res = json.loads(response.text)
        # # Get response and send data
        json_res = json.loads(response.text)

        # Prepare data
        # Get file data from image object
        files = {"file": user.image.image_file}

        # Set the params to the params based on the response from canvas
        # These must be identical to the params received from canvas.
        # Else this will fail
        try:
            self.upload_params = json_res["upload_params"]
        except KeyError as e:
            self.log.error(
                "Upload Parameters could not be set: %s. The following response was returned %s".format(e, response.text)
            )
            return False
        # Send the file to canvas
        # Get upload confirmation
        upload_file_response = requests.post(
            json_res["upload_url"], data=self.upload_params, files=files, allow_redirects=False
        )

        status_code: int = upload_file_response.status_code

        # The response from canvas can either be 201 or 3XX
        # A 300+ response requires a confirmation from the app
        # A 201 is a confirmation and a get will return the file id
        if status_code == 201 or status_code >= 300:
            # Get file upload confirmation and file ID
            confirmation = requests.get(
                upload_file_response.headers["location"], headers=self.header
            )

        else:
            # If another value returns then there was an issue
            # Exit the application
            self.log.error("CANVAS: File upload Failed")
            return False

        # Get file ID From canvas
        if "id" in confirmation.json():
            # If file ID is found then set it for the image
            user.image.image_canvas_id = confirmation.json()["id"]
        else:
            self.log.error("CANVAS: No file ID found for uploaded file")

        # Successfully uploaded file
        return True
    
    def set_image_as_avatar(self, user: client) -> bool:
        """Sets an image to be a user's PFP"""

        # Ensure the upload parameters are correctly set
        if not self.upload_params:
            self.log.error("Upload params is empty, cannot set image avatar.")
            return False

        # Log that Canvas avatar is being updated
        self.log.info(f"Setting canvas Avatar for: {user.client_id} To: {user.image.image_name}")

        # Fetch the avatar options for the user (without using as_user_id unnecessarily)
        avatar_options = requests.get(
            f"{self.domain}/users/{user.client_id}/avatars",
            headers=self.header,
        )
        
        avatar_options.raise_for_status()

        # Iterate through the avatars to find the matching uploaded image
        token = None
        for avatar_opt in avatar_options.json():
            if avatar_opt.get("display_name") == user.image.image_name:
                token = avatar_opt.get("token")
                break

        # If the token is found, proceed to update the avatar
        if token:
            self.log.info(f"Avatar token found for: {user.client_id}, setting image as avatar.")
            # Update the avatar for the specific user
            set_avatar_user = requests.put(
                f"{self.domain}/users/{user.client_id}",
                headers=self.header,
                params={"user[avatar][token]": token},
            )
            set_avatar_user.raise_for_status()

            if set_avatar_user.status_code == 200:
                self.log.info(f"Success updating user avatar for: {user.client_id}")
                return True
        else:
            self.log.error(f"No matching avatar found for image: {user.image.image_name} for user {user.client_id}")

        # Log and return false if the avatar was not updated
        self.log.error(f"Failed to update avatar for user {user.client_id}")
        return False