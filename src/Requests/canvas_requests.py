'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        Class for handling the requests to the remote
        server and the canvas API.
'''

'''
    - Use type annotations more consistently throughout the code to improve readability and maintainability.
    - Use requests.Session() to reduce the overhead of repeatedly sending authentication headers with every request.
    - Instead of raising an error when the connection test fails, return a boolean False value instead. This allows the caller to handle the error more gracefully.
    - Use more descriptive function names to make it easier to understand what each function does.
    - Add more error handling to the upload_user_data() function to handle potential errors that might occur during the file upload process.
    - Instead of using async and await keywords with get_canvas_id() and upload_user_data() functions, use the standard synchronous approach since there are no asynchronous operations in those functions.
    - Consider using f-strings or str.format() to format log messages more succinctly and consistently.
'''

# External imports
from abc import ABC, abstractmethod
import requests
import json
import logging

# Internal imports
from src.Clients import client


class Canvas_connector(ABC):
    '''Abstract base class for canvas connector'''

    def __init__(self, Token: str, domain: str) -> None:
        ''' Initialise a connector'''
        self.Session = requests.Session()
        # TODO: implement the sessions system from requests, to save on request information
        self.Auth_token: str = Token
        self.domain: str = f'https://{domain}/api/v1'
        self.header: dict = {'Authorization': f'Bearer {self.Auth_token}'}
        self.params: dict = {}
        
        self.Session.headers.update()

        # Logger instance
        self.log: logging.Logger = logging.getLogger(__name__)

        # Log initialised values
        self.log.write_log(
            'CANVAS: initialised values:',
            f'Auth Token:\t {self.Auth_token}',
            f'Domain:\t {self.domain}',
            f'Header:\t {self.header}',
            f'Params:\t {self.params}'
        )
        # Call Canvas Test function
        self.test_canvas_connection()

    def test_canvas_connection(self):
        '''Validates that connection to canvas can be made'''
        # Variables
        desired_result: int = 200

        res : requests.Response = requests.get(
            f'{self.domain}/accounts', self.params, headers=self.header)

        if res.status_code == desired_result:
            # If result 200 then return true
            self.log.write_log("CANVAS: Connection Successfully Tested")
            return True
        else:
            # If other result received return false
            self.log.write_error(ConnectionRefusedError(
                f"Canvas Refused the connection: {res.status_code}"))
            raise ConnectionRefusedError("Canvas Refused the connection")

    @abstractmethod
    def get_canvas_id(self, user: client) -> bool:
        ''' Gets internal canvas ID from student ID in SIS. Returns bool (true) on success '''

    @abstractmethod
    def upload_user_data(self, user: client) -> bool:
        ''' Uploads user data to canvas. Returns bool (true) on success'''

    @abstractmethod
    def set_image_as_avatar(self, user: client) -> bool:
        ''' Sets and image to be a users PFP'''


class POST_data_canvas(Canvas_connector):
    ''' Posts data to canvas'''

    def __init__(self, Token: str, domain: str) -> None:
        ''' For passing information to canvas '''
        super().__init__(Token, domain)

    async def get_canvas_id(self, user: client) -> bool:
        ''' Gets a user ID from Canvas '''
        # Write log with user ID
        self.log.write_log(
            f'USER: Getting Canvas ID for: {user.client_id}'
        )

        # Send get request for a user's canvas id. This is
        # different from their SIS id
        user_Details : requests.Response = requests.get(
            f'{self.domain}/users/sis_user_id:{user.client_id}',
            headers=self.header,
            params=self.params
        )

        # Check if id is in the json response.
        if 'id' in user_Details.json():
            # User ID found then change the users SIS id to match
            user.client_id = user_Details.json()['id']
            return True
        else:
            # If not found, return an error to the log with the SIS id
            self.log.write_error(
                f'USER: {user.client_id} cannot be found in canvas')
            return False

    async def upload_user_data(self, user: client) -> bool:
        ''' Upload image to users files '''
        # Variables
        url: str = self.domain + '/users/self/files'
        inform_parameters = {
            'name': user.image.image_name,
            'size': user.image.image_size,          # read the filesize
            'content_type': user.image.file_type,
            'parent_folder_path': 'profile pictures',
            'as_user_id': user.client_id
            }

        # Prepare Canvas for upload
        response : requests.Response = requests.post(
            url,
            headers=self.header,
            data=inform_parameters)

        # json_res = json.loads(response.text)
        # # Get response and send data
        json_res = json.loads(response.text)

        # Prepare data
        # Get file data from image object
        files = {'file': user.image.image_file}

        # Set the params to the params based on the response from canvas
        # These must be identical to the params received from canvas.
        # Else this will fail
        self.params = json_res['upload_params']

        # Send the file to canvas
        # Get upload confirmation
        upload_file_response = requests.post(
            json_res['upload_url'],
            data=self.params,
            files=files,
            allow_redirects=False)

        status_code: int = upload_file_response.status_code

        # The response from canvas can either be 201 or 3XX
        # A 300+ response requires a confirmation from the app
        # A 201 is a confirmation and a get will return the file id
        if status_code == 201 or status_code >= 300:
            # Get file upload confirmation and file ID
            confirmation = requests.get(
                upload_file_response.headers['location'],
                headers=self.header)

        else:
            # If another value returns then there was an issue
            # Exit the application
            self.log.write_error("CANVAS: File upload Failed")
            return False

        # Get file ID From canvas
        if 'id' in confirmation.json():
            # If file ID is found then set it for the image
            user.image.image_canvas_id = confirmation.json()['id']
        else:
            self.log.write_error('CANVAS: No file ID found for uploaded file')

        # Successfully uploaded file
        return True

    async def set_image_as_avatar(self, user: client) -> bool:
        ''' Sets and image to be a users PFP'''

        # Log that Canvas avatar is being updated
        self.log.write_log(
            f'Setting canvas Avatar for: {user.client_id} To: {user.image.image_name}'
            )

        # Set parameters as the user_id
        self.params = {'as_user_id': f'{user.client_id}'}

        # Get-Request the user avatars images, to get image id
        avatar_options = requests.get(
            f'{self.domain}/users/{user.client_id}/avatars',
            headers=self.header,
            params=self.params
            )

        # As there are multiple avatars that come stock with canvas
        # the program needs to iterate through the avatars to find
        # the image that was uploaded.
        for avatar_opts in avatar_options.json():

            # If the current avatar has the same name as the uploaded image
            # Set params to be 'user[avatar][token] = <token>.
            # The image token is unique to each request. So cannot be
            # relied on between sessions.
            if avatar_opts.get('display_name') == user.image.image_name:
                self.params['user[avatar][token]'] = avatar_opts.get('token')

            # Create put request to tell canvas to update pfp
            # This is done as a put to prevent POST from regenerating
            # outputs
            set_avatar_user = requests.put(
                f'{self.domain}/users/{user.client_id}',
                headers=self.header,
                params=self.params
            )

        # If the canvas response is 200, then the update has been successful
        if set_avatar_user.status_code == 200:
            self.log.write_log(
                f'success updating user avatar for: {user.client_id}')

            return True
        else:
            # If the update was not successful, log the result
            self.log.write_error(
                f'CANVAS: Error updating avatar for: {user.client_id},' +
                f' error: {set_avatar_user.status_code}'
                )
            return False
