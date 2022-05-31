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
from src.Logger.log import write_error, write_log
from src.ImageHandler.image_handler import open_image


# Module Functions

''' For passing information to canvas '''
settings = json.load(open(file='./Settings/settings.json', encoding='utf-8'))
Auth_token: str = settings['access_token']
domain: str = f'https://{settings["domain"]}/api/v1/users'
header: str = ""
params: tuple = {}

def get_canvas_user_id(user:client) -> bool:
    ''' Gets a user ID from Canvas '''
    
    write_log(
        f'USER: Getting Canvas ID for: {user.client_id}'
    )

    user_Details = requests.get(
        f'{domain}/sis_user_id:{user.client_id}',
        headers=header,
        params=params
    )

    if 'id' in user_Details.json:
        user.client_id = user_Details.json()['id']
        return True
    else:
        write_error(f'USER: {user.client_id} cannot be found in canvas')
        return False

def upload_image(user: client) -> bool:
    ''' Upload image to users files '''
    # Variables
    url: str = domain + '/self/files'
    inform_parameters = {
        'name':user.image.image_name,
        'size':user.image.image_size, # read the filesize
        'content_type':user.image.file_type,
        'parent_folder_path':'profile pictures',
        'as_user_id': user.client_id
        }
    
    # Prepare Canvas for upload
    responese = requests.post(url,headers=header,data=inform_parameters)

    # Get response and send data
    json_res = json.loads(responese.text,object_pairs_hook=collections.OrderedDict)

    # Prepare data
    files = user.image.image_file

    _data = json_res.items()
    _data[1] = ('upload_params',_data[1][1].items())

    upload_file_response = requests.post(json_res['upload_url'],data=_data[1][1],files=files,allow_redirects=False)
   

