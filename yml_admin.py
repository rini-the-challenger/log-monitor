import yaml
import os


class YmlAdmin:

    def __init__(self):
        self.settings = None
        self.file_path = os.curdir + "/cfg/application.yml"

    def read_yaml(self):
        with open(self.file_path, "r", encoding='utf-8') as f:
            self.settings = yaml.safe_load(f)
        print(self.settings['APP']['ROOT-DIR'])
