'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for reading the CSV file
'''

# External imports
from abc import ABC, abstractmethod
import csv
from http.client import ImproperConnectionState

# Internal Imports
from src.Clients.user import client
from src.File.sourceFile import *
from src.Logger.log import logger

#File Class
class Reader(ABC):
    '''Reader for csv files'''
    @abstractmethod
    def __init__(self) -> None:
        '''Initalise Reader'''

    @abstractmethod
    def get_clients(self) -> list:
       ''' Returns list of clients from file'''

class csv_reader(Reader):

    def __init__(self, src: str) -> None:
        self.source_file = csv_Source(src).file

    def get_clients(self) -> list:
        ''' Read clients from csv'''
        # Variables
        clients:client = []                         # Create list of clients
        csv_object = csv.DictReader(self.source_file)

        # Iterate through all rows in csv
        for row in csv_object:
            # append client to list
            new_client = client(row['client_id'], row['image_filename'])
            clients.append(new_client)
        # BUG: csv.reader includes the first row as an object instead of headings
        return clients
