'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        Class for reading the CSV file
'''

# TODO: The reader objects are not single purpose.
#   These objects should be renamed to parser.
#   So as to parse sourceFile to objects

# External imports
from abc import ABC, abstractmethod
import csv

# Internal Imports
from src.File import sourceFile, csv_Source

##########
'''
    TODO: This needs to be Dependency injected.
    It currently is too coupled on CSV_source
'''
##########


# File Class
class Reader(ABC):
    '''Reader for csv files'''
    @abstractmethod
    def __init__(self, source: sourceFile) -> None:
        '''Initialise Reader'''

    @abstractmethod
    def get_clients(self) -> list:
        ''' Returns list of clients from file'''


class csv_reader(Reader):
    ''' read CSV files '''

    def __init__(self, sourceFile: sourceFile) -> None:
        ''' Initialise a reader with a source '''

        # Verify that sourcefile is CSV filetype
        # if (issubclass(sourceFile, csv_Source)):
        #     raise TypeError(f"Incorrect source file type: {sourceFile}")

        # Assign source file
        self.source_file = sourceFile.open_file

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
