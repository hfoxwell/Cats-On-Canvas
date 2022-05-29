'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for reading the CSV file
'''

# External imports
from abc import ABC, abstractmethod
import csv

from werkzeug import Client

# Internal Imports
from src.Clients.user import client
from src.File.sourceFile import *

#File Class
class Reader(ABC):
    '''Reader for csv files'''

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
        csv_object = csv.reader(self.source_file)

        # Iterate through all rows in csv
        for row in csv_object:
            # append client to list
            new_client = client(row[0])
            clients.append(new_client)

        return clients
