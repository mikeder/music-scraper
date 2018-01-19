import json
import yaml
from exception import ConfigLoadError


class Config(object):
    def __init__(self, a_file_path):
        """
        Initialize a config file into a usable object
        :param a_file_path: path to a json or yaml formatted config file
        """
        self.keys = None
        with open(a_file_path) as self.file:
            self.keys = self.__load(self.file)

    def __load(self, a_file):
        try:
            return json.load(a_file)
        except:
            pass
        try:
            return yaml.load(a_file)
        except:
            raise ConfigLoadError(
                status_code=1000,
                platform_code=1000,
                error_string="Unable to load viable config from {}".format(
                    a_file
                ))

    def get_all(self):
        return self.__dict__
