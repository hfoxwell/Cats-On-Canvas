"""
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        Class representing an image
    Updated: (hayden foxwell - 21/03/24)
"""

# External imports
from dataclasses import dataclass, field
from pathlib import Path

# File Class
@dataclass
class Image:
    '''Represents a profile picture'''
    image_file: bytes = field(compare=False)
    image_name: str = field(compare=True)
    image_path: str = field(compare=False)
    file_type: str = field(compare=False)
    image_size: int = field(init=False)
    image_canvas_id: str = field(init=False)

    def __post_init__(self):
        self.image_size = self.image_file.__sizeof__()


# File module
class ImageFactory:
    """Handles all images for the app"""

    def open_image(self, image_path: Path) -> Image:
        """Open an image file"""
        # Variables
        img_bytes: bytes
        
        try:
            # Open file as byte file
            with open(image_path, "rb") as img_file:
                img_bytes = img_file.read()
        except FileNotFoundError as FNFE:
            raise FileNotFoundError from FNFE
        
        # create image file object and return
        return Image(
            image_file = img_bytes,
            image_name = image_path.name,
            image_path = str(image_path),
            file_type = image_path.suffix.strip().replace('.', '')
        )
