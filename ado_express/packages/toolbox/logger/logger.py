import logging
import sys
from datetime import datetime

from pytz import timezone

from ado_express.packages.shared.constants import Constants


class Logger:

    def __init__(self, is_running_as_executable):
        if is_running_as_executable: self.log_to_console_only()
        else: self.log_to_file_and_console()
        
    def log_to_console_only():
        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s:%(asctime)s \t%(pathname)s:line:%(lineno)d \t%(message)s')

    def log_to_file_and_console():
        file_handler = logging.FileHandler(Constants.LOG_FILE_PATH, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(levelname)s:%(asctime)s \t%(pathname)s:line:%(lineno)d \t%(message)s')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
        logging.info('Starting application')
        
    def log_the_start_of_application(self, is_search_only: bool):
        if is_search_only:
            time_format = '%Y-%m-%d %H:%M:%S'
            datetime_now = datetime.now(timezone('US/Eastern'))
            logging.info('Starting the search...')
            logging.info(f"Search Date & Time:{datetime_now.strftime(time_format)}\nResults:\n")
        else:
            logging.info('Starting the update...')