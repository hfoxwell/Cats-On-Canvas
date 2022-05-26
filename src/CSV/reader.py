'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for reading the CSV file
'''

# External imports

# Internal Imports
from src.Clients.user import client

#File Class
class reader():
    '''Reader for csv files'''

    def __init__(self, fd:str) -> None:
        self.file_directory = fd


    def get_clients(self) -> list:
        ''' Returns a list of users '''
        #TODO: Iterate through csv file and create clients