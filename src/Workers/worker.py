'''
    Author: Hayden Foxwell
    Date:   21/03/24
    Purpose:
        To create workers which produce and consume clients
'''

# Imports
import threading
from queue import Queue
import logging
from requests.exceptions import HTTPError

# Internal imports
from src import Clients,Image,Canvas, custom_errors

# ===================
# Classes
class Worker(threading.Thread):

    def __init__(self, user_queue:Queue[Clients.Client]) -> None:
        super().__init__(daemon=True)
        self.log = logging.getLogger(__name__)
        self.queue = user_queue
        self.client = None
        self.working = False
        self.progress = 0

    @property
    def state(self):
        if self.working:
            return f"{self.client.client_id} ({self.progress}%)"
        return ":zzz: Idle"

    def run(self):
        '''Completes the work assigned'''

########################
# SubClasses
########################
class Producer(Worker):
    '''Produces clients from the queue of available client identifiers'''
    def __init__(self, user_queue: Queue, available_users: Queue[Clients.ClientIdentifier], image_factory:Image.ImageFactory) -> None:
        super().__init__(user_queue)
        self.available_users = available_users
        self.image_factory = image_factory

    def _create_user(self, user_id: str, image: Image.Image) -> Clients.Client:
        ''' Creates a client '''
        self.log.debug(
            'Creating user of: %s', user_id
        )
        
        # Variables
        client: Clients.Client

        client = Clients.Client(
            client_id=user_id,
            client_image=image
        )

        return client

    def _get_image(self, img_path) -> Image.Image:
        '''Creates an image object'''
        # Variables
        image: Image.Image

        image = self.image_factory.open_image(img_path)

        return image

    def run(self):
        # Complete work provided
        # Variables
        current_client: Clients.Client
        current_image: Image.Image

        while True:
            # Variables
            self.progress = 0
            
            # Get next client from list
            self.client = self.available_users.get()
            self.working = True

            try: 
                # Create a client from a client_identifier
                current_image = self._get_image(self.client.profile_picture_path)
                self.progress = 50
                current_client = self._create_user(
                    self.client.client_id,
                    current_image
                )
                
                self.progress = 100
                self.log.info('Enqueuing user: %s', current_client.client_id)
                self.queue.put(current_client)
                self.available_users.task_done()
            except FileNotFoundError as e:
                self.log.error(
                    'Failed to create user: %s \t %s', self.client.client_id, e
                )
                continue
            
            self.working = False

class Consumer(Worker):
    '''Submits clients to canvas'''
    def __init__(self, user_queue: Queue[Clients.Client], canvas_connector) -> None:
        super().__init__(user_queue)
        self.canvas_connector:Canvas.Canvas_connector = canvas_connector

    def run(self):
        steps = 4
        while True:
            self.progress = 0
            self.client = self.queue.get()
            self.working = True
            try:
                # Step 1 set user to modify
                self.canvas_connector.set_user(self.client)
                self.progress += 100 // steps
                # Step 2 get the user's canvas id
                self.canvas_connector.get_canvas_id()
                self.progress += 100 // steps
                # Step 3 Upload user data
                self.canvas_connector.upload_user_data()
                self.progress += 100 // steps
                # Step 4 set uploaded photo to avatar
                self.canvas_connector.set_image_as_avatar()
                self.progress += 100 // steps
            
            except HTTPError as e:
                self.log.error(
                    'Could not process user: %s \t %s', self.client.client_id, e
                )
            except custom_errors.CanvasError as CE:
                self.log.error(
                    'Could not process user: %s \t %s', self.client.client_id, CE
                )
            except custom_errors.CanvasAvatarSetError as CASE:
                self.log.error(
                    'Could not process user: %s \t %s', self.client.client_id, CASE
                )
            
            self.queue.task_done()
            self.working = False