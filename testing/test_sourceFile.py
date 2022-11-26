"""
    Author:     Hayden Foxwell
    Date:       16/10/2022
    Purpose:
        Test the new source file system for cats on canvas
"""
# imports
import csv, pytest, string, random
from io import TextIOWrapper
from pytest import MonkeyPatch

# local imports
from src.File import sourceFile
from testing import Helper_functions

# TODO: Mock a file to open
class Test_sourcefile:
    
    def test_validFile(self, monkeypatch: MonkeyPatch):
        ''' Verify error is not thrown for valid csv files '''
        num_of_tests = 10
        valid_file_types = {
            'text'      : '.txt',
            'comma_sep' : '.csv'
        }
        
        # Mock the open Function
        def mock_open():
            return None
        
        # Monkeypatch the open file
        monkeypatch.setattr(sourceFile.csv_Source, 'open', mock_open)
        
        for test in range(num_of_tests):
            # Variables for filename
            filename: str = Helper_functions.generate_random_string(
                length=random.randint(1, 20),
                charset=string.ascii_letters
            )
            
            filename.join(random.choice(valid_file_types.items))
            
            print(f'{test} -- {filename}')
            sourceFile.csv_Source(input_file=filename)
            
        

    def test_invalidFile(self):
        ''' Verify that error is thrown for invalid csv files '''

# TODO: Mock use of a factory method to return correct file object