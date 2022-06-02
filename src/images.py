from cv2 import cv2


class Images:
    def __init__(self, theme='default'):
        from src.config import Config
        self.config = Config().read()

        if self.config['app']['theme']:
            self.theme = self.config['app']['theme']
        else:
            self.theme = theme

    def image(self, image, theme=False, path=None):
        themePath = './images/themes/default/'
        if theme == True:
            themePath = './images/themes/' + self.theme + '/'

        if path != None:
            themePath = path

        return cv2.imread(themePath + image + '.png')
