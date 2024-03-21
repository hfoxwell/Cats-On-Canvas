'''
    Author:     Hayden Foxwell
    Date:       03/06/2023
    Purpose:
        Custom error types which are used throughout 
        the program
'''

###############################
## File handling Errors
###############################

class DirectoriesCheckError(Exception):
    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)
        
class SettingsLoadError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)
        
class CanvasError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)