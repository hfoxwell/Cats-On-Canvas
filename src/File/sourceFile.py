'''
    Author: H Foxwell
    Date:   29/05/2022
    Purpose:    
        Collection of classes for opening and verifying
        the files to be passed to a reader. Each will 
        verify they are of the correct file type before
        presenting a file object for reading. Either 
        TextIOWrapper or ByteIOWrapper.
'''

# External imports
import os, sys
from abc import ABC,abstractmethod

# Internal imports

class sourceFile(ABC):
    '''Abstract class for opening a file type'''
    @abstractmethod
    def __init__(self, input_file: str) -> None:
        '''Initialise the source file'''
    
    @abstractmethod
    def _verify_file(self, file: str):
        ''' Verify the correct file type is passed in '''
        pass

class csv_Source(sourceFile):
    '''Opens CSV files for reading'''
    
    def __init__(self, input_file: str) -> None:
        '''initialise a file opener'''
        # verify the file
        self._verify_file(input_file)
        
        # if no error was raised
        self.csv_file = input_file    
        
    def _verify_file(self, file: str):
        # Variables
        file_extensions = ['.csv', '.txt']
        current_file_extension: str = os.path.splitext(file)
        
        # Verify the type of the file
        if not(current_file_extension in file_extensions):
            raise AttributeError(
                f"Expected CSV file: {current_file_extension}")