"""
    Author:     Hayden Foxwell
    Date:       16/10/2022
    Purpose:
        Test the new source file system for cats on canvas
"""
# imports
from io import StringIO

# local imports
from src.File import sourceFile

in_mem_csv = StringIO("""\
col1,col2,col3
1,3,foo
2,5,bar
-1,7,baz""")  # in python 2.7, put a 'u' before the test string
test_reader = sourceFile.csv_Source(in_mem_csv)
for line in test_reader:
    print(line)
    # whatever you need to test to make sure the csv reader works correctly