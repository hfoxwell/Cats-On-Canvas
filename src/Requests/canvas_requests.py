'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for handling the requests to the remote 
        server and the canvas API.
'''

# External imports
from abc import ABC, abstractmethod
import requests, json, collections

# Internal imports
from src.Clients.user import client
from src.Logger.log import write_error, write_log


class Canvas_connector(ABC):
    '''Abstract base class for canvas connector'''

    def __init__(self) -> None:
        self.settings = json.load(open(file='./Settings/settings.json', encoding='utf-8'))
        self.Auth_token: str = self.settings['access_token']
        self.domain: str = f'https://{self.settings["domain"]}/api/v1/users'
        self.header: str = ""
        self.params: tuple = {}

    @abstractmethod
    def get_canvas_id(self, user:client) -> bool:
        ''' Gets internal canvas ID from student ID in SIS. Returns bool (true) on success '''

    @abstractmethod
    def upload_user_data(self, user:client) -> bool:
        ''' Uploads user data to canvas. Returns bool (true) on success'''

class POST_data_canvas(Canvas_connector):
    
    def __init__(self) -> None:
        super().__init__()
        # ''' For passing information to canvas '''
        # settings = json.load(open(file='./Settings/settings.json', encoding='utf-8'))
        # Auth_token: str = settings['access_token']
        # domain: str = f'https://{settings["domain"]}/api/v1/users'
        # header: str = ""
        # params: tuple = {}

    def get_canvas_user_id(self, user:client) -> bool:
        ''' Gets a user ID from Canvas '''
        
        write_log(
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
            write_error(f'USER: {user.client_id} cannot be found in canvas')
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
        files = user.image.image_file

        _data = json_res.items()
        _data[1] = ('upload_params',_data[1][1].items())

        upload_file_response = requests.post(json_res['upload_url'],data=_data[1][1],files=files,allow_redirects=False)
    

