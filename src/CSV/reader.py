'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for reading the CSV file
'''

# External imports
from abc import ABC, abstractmethod
import csv

# Internal Imports
from src.File.sourceFile import csv_Source

##########
'''
    TODO: This needs to be Dependancy injected. It currently is too coupled on CSV_source
'''
##########

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
        ''' Read clients from csv and return details'''
        # Variables
        clients_list = []                         # Create list of clients
        csv_object = csv.DictReader(self.source_file)

        # Iterate through all rows in csv
        for row in csv_object:
            # For each row in the dictionary create list of client details
            clients_list.append(row)

        return clients_list
