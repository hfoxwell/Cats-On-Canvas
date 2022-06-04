'''
    Author: H Foxwell
    Date:   29/05/2022
    Purpose:    
        Class for opening files for reading or writing
'''

# Extrnal imports
from abc import ABC,abstractmethod

# Internal imports

class sourceFile(ABC):
    '''Abstract class for opening a file type'''
    @abstractmethod
    def __init__(self, dir: str) -> None:
        '''Initalises the source file'''
    
    @abstractmethod
    def close_file(self):
        ''' Closes the file '''

class csv_Source(sourceFile):
    '''Opens CSV files for reading'''

    def __init__(self, dir: str) -> None:
        '''initalises a file opener'''
        self.file = None
        fileOpened = open(dir)
        self.file = fileOpened        

    def close_file(self):
        ''' closes the file '''
        self.file.close()
