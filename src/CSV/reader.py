'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:    
        Class for reading the CSV file
'''

# External imports
import csv

# Internal Imports
from src.Clients.user import client
from src.File.sourceFile import csv_Source

#File Class
# TODO: Make this an abstact method for different files 
class reader():
    '''Reader for csv files'''

    def __init__(self, fd:str) -> None:
        self.file_directory = fd
        self.client_dictionary = None
        self.source_file = None


    def get_clients(self) -> dict:
        ''' Returns a dictionary of items from a csv file '''
        #TODO: Iterate through csv file and create clients
        
        # Create source file object for reading
        self.source_file = csv_Source(self.file_directory)

        self.client_dictionary = csv.reader(self.source_file.file)

        # TODO: change the test
        for line in self.client_dictionary:
            print(f'ROW CONTAINS: {line[0]} {line[1]} {line[2]}')
