from colorama import Fore
import yaml


class Config:
    def read(self):
        try:
            file = open("./config/config.yaml", 'r', encoding='utf8')
        except FileNotFoundError:
            print(Fore.RED + 'Error: config.yaml file not found, rename EXAMPLE-config.yaml to config.yaml inside /config folder' + Fore.RESET)
            exit()

        with file as s:
            stream = s.read()
        return yaml.safe_load(stream)
