'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for handling the requests to the remote 
        server and the canvas API.
'''

# External imports
import requests, json, collections

# Internal imports
from src.Clients.user import client
from src.Logger.log import logger

# File Class
class Canvas_requester():
    ''' For passing information to canvas '''

    def __init__(self, auth: str, domain: str, log:logger) -> None:
        self.Auth_token: str = auth
        self.domain: str = f'https://{domain}/api/v1/users'
        self.header: str = ""
        self.params: tuple = {}

        # Import Logger
        self.logger = log
    
    def get_canvas_user_id(self, user:client) -> bool:
        ''' Gets a user ID from Canvas '''
        
        logger.write_log(
            f'USER: Getting Canvas ID for: {user.client_id}'
        )

        user_Details = requests.get(
            f'{self.domain}/sis_user_id:{user.client_id}',
            headers=self.header,
            params=self.params
        )

        if 'id' in user_Details.json:
            user.client_id = user_Details.json()['id']
            return True
        else:
            logger.write_error(f'USER: {user.client_id} cannot be found in canvas')
            return False

    def upload_image(self, user: client) -> bool:
        ''' Upload image to users files '''
        # Variables
        url: str = self.domain + '/self/files'
        inform_parameters = {
            'name':user.image.image_name,
            'size':user.image.image_size, # read the filesize
            'content_type':user.image.file_type,
            'parent_folder_path':'profile pictures',
            'as_user_id': user.client_id
            }
        
        # Prepare Canvas for upload
        responese = requests.post(url,headers=self.header,data=inform_parameters)

        # Get response and send data
        json_res = json.loads(responese.text,object_pairs_hook=collections.OrderedDict)

        # Prepare data

