import yaml


class Config:
    def read(self):
        try:
            file = open("./config/config.yaml", 'r', encoding='utf8')
        except FileNotFoundError:
            print('Error: config.yaml file not found, rename EXAMPLE-config.yaml to config.yaml inside /config folder')
            exit()

        with file as s:
          stream = s.read()
        return yaml.safe_load(stream)
