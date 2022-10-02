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
   :type is_crucial: bool
   :param is_crucial:
   """

   def __init__(self, release_project_name=None, release_name=None, release_number=None, release_rollback=None, is_crucial=False):
      self.release_project_name = release_project_name
      self.release_name = release_name
      self.release_number = release_number
      self.release_rollback = release_rollback

      if is_crucial is None: 
         self.is_crucial = False
      else :
         try:
            self.is_crucial = bool(strtobool(is_crucial))
         except:
            logging.error(f'Message:Unable to read value of "Crucial" - At:{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

