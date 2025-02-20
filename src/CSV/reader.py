'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        Class for reading the CSV file
'''
import csv
# External imports
from abc import ABC, abstractmethod

# Internal Imports
from src.File import sourceFile


# File Class
class Reader(ABC):
    '''Reader for csv files'''
    @abstractmethod
    def __init__(self, source_file: sourceFile) -> None:
        '''Initialise Reader'''

    @abstractmethod
    def get_clients(self) -> list:
        ''' Returns list of clients from file'''


class CSVReader(Reader):
    ''' read CSV files '''

    def __init__(self, source_file: sourceFile) -> None:
        ''' Initialise a reader with a source '''

        # Verify that sourcefile is CSV filetype
        # if (issubclass(sourceFile, csv_Source)):
        #     raise TypeError(f"Incorrect source file type: {sourceFile}")

        # Assign source file
        self.source_file = source_file.open_file

    def get_clients(self) -> list[dict[str, str]]:
        ''' Read clients from csv and return details'''
        # Variables
        clients_list = []                         # Create list of clients
        csv_object = csv.DictReader(self.source_file)

        # Iterate through all rows in csv
        for row in csv_object:
            # For each row in the dictionary create list of client details
            clients_list.append(row)

        return clients_list
