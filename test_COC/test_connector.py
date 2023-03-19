'''
    Author: H Foxwell
    Date:   26/06/2022
    Purpose:    
        Test the connection to canvas and how the logic works for sending files
'''

# External imports
import requests, json, pytest, string, random

# Internal imports
from src.Requests import canvas_requests
from src.Clients import client

###################
## Tests
###################

######
# Utility
######

def mock_request_get():
    ''' patch the connection '''

    class mock_response_get(object):
        ''' mock response '''

        status_code = 200
        url = 'http://httpbin.org/get'
        headers = {}
        params = {}

        def __init__(self, addr, headers=None, params=None):
            self.status_code = 200
            self.url = 'http://httpbin.org/get'
            self.headers = headers
            self.params = params

        def json():
            return {'id': '5678',
                    'url': 'http://www.testurl.com'}

    return mock_response_get


class mock_log(object):
    ''' mock logger '''
    def __init__(self) -> None:
        self.log_file_path = "./"
        self.log_file_name = "log.txt"
        self.log_file = None

    def write_log(self, *content):
        pass

    def write_error(self, error):
        pass

##
# 1
##
def test_get_canvas_id(monkeypatch: pytest.MonkeyPatch):
    ''' Test the getting and returning of a canvas id '''
    ### This function should get a canvas user id
    ###     and overwrite the existing user id for that user

    # Variables 
    user_ID = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    img = None

    # Create test user
    test_user: client = client(user_ID, img)
    log = mock_log()

    # Create new connection
    def mock_get(url, params, headers):
        return mock_request_get()

    ## Monkeypatch the requests GET module
    monkeypatch.setattr(requests, "get", mock_get)

    # Create canvas connector
    conn = canvas_requests.POST_data_canvas("", "", log) #BUG: this fails with 4 pos arguments instead of 3

    # Get canvas id
    res = conn.get_canvas_id(test_user)

    ## Assert that the result of the function is true ( success state )
    ## Assert that client id has been changed to new number
    assert res == True
    assert test_user.client_id == '5678'


def test_upload_user_data(monkeypatch: pytest.MonkeyPatch):
    ''' Test the upload of user data '''

    ### Process ###
    # 1. the parameters and headers are set 
    # 2. Post a request to a file    



    # assert res == True