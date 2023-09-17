import logging
import sys

from ado_express.packages.common.constants import Constants


class Logger:

    def __init__(self, is_running_as_executable):
        if is_running_as_executable:
            # Log to console only when running as an executable
            logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s:%(asctime)s \t%(pathname)s:line:%(lineno)d \t%(message)s')
        else:
            # Log to a file when not running as an executable and also print to stdout
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
            logging.info('Starting the search...')
            logging.info(f"Search Date & Time:{self.datetime_now.strftime(self.time_format)}\nResults:\n")
        else:
            logging.info('Starting the update...')