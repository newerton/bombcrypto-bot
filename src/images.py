from cv2 import cv2
from PIL import Image

class Images:
    def __init__(self, theme='default'):
        from src.config import Config
        self.config = Config().read()

        if self.config['app']['theme']:
            self.theme = self.config['app']['theme']
        else:
            self.theme = theme

    def image(self, image, theme=False, path=None, extension='.png'):
        themePath = './images/themes/default/'
        if theme == True:
            themePath = './images/themes/' + self.theme + '/'

        if path != None:
            themePath = path

        if(extension != '.gif'):
            return cv2.imread(themePath + image + extension)

        if(extension == '.gif'):
            im = Image.open(themePath + image + extension)
            return im
