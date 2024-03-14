'''
    Author: H Foxwell
    Date:   26/05/2022
    Purpose:
        Class for logging to file
'''
# External imports
import json

# internal imports

import logging
import logging.config
import atexit

def open_log_config(config_path: str):
    '''Opens the logging config file'''
    with open(config_path, 'r', encoding='utf-8') as conf_file:
        log_config = json.load(conf_file)

        return log_config

def configure_logging(log_config_path: str, name: str) -> logging.Logger:
    '''Creates logger and configures the logger with dict_config'''
    logger = logging.getLogger(name)
    
    # Load logging configuration from file
    logging.config.dictConfig(
        open_log_config(log_config_path)
    )
    
    # Retrieve the queue handler
    queue_handler = None
    for handler in logger.handlers:
        if isinstance(handler, logging.handlers.QueueHandler):
            queue_handler = handler
            break

    # Start the queue handler listener if found
    if queue_handler:
        queue_handler.start()
        atexit.register(queue_handler.stop)

    return logger
