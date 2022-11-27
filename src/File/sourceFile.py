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
import os
from io import TextIOWrapper
from abc import ABC, abstractmethod

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

    @abstractmethod
    def _open_file(self, file: str, mode: str) -> TextIOWrapper:
        ''' Opens the file for reading'''
        pass

    @abstractmethod
    def __del__(self):
        ''' cleanup after the object '''
        pass


class csv_Source(sourceFile):
    '''Opens CSV files for reading'''

    def __init__(self, input_file: str) -> None:
        '''initialise a file opener'''
        # verify the file
        self._verify_file(input_file)

        # if no error was raised
        self.open_file: TextIOWrapper = self._open_file(
            input_file, "r")

    def _verify_file(self, file: str):
        # Variables
        file_extensions = ['.csv', '.txt']
        current_file_extension: str = os.path.splitext(file)

        # Verify the type of the file
        if not(current_file_extension in file_extensions):
            raise AttributeError(
                f"Expected CSV file: {current_file_extension}")

    def _open_file(self, file: str, mode: str) -> TextIOWrapper:
        # BUG: This function does not return internal variable
        #       instead it returns the file handle passed
        # open the file
        open_file: TextIOWrapper = None
        open_file = open(file, mode)
        # return file object to caller
        return file

    def __del__(self):
        # Close the open file
        self.open_file.close()
