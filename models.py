import datetime
import logging

from distutils.util import strtobool

class Deployment_Details():
   """
   :param release_project_name:
   :type release_project_name: str
   :param release_name:
   :type release_name: str
   :param release_number:
   :type release_number: int
   :param release_rollback:
   :type release_rollback: int
   :type critical: bool
   :param critical:
   """

   def __init__(self, release_project_name=None, release_name=None, release_number=None, release_rollback=None, critical=False):
      self.release_project_name = release_project_name
      self.release_name = release_name
      self.release_number = release_number
      self.release_rollback = release_rollback

      if critical is None: 
         self.critical = False
      else :
         try:
            self.critical = bool(strtobool(critical))
         except:
            logging.error(f'Message:Unable to read value of "Critical" - At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

