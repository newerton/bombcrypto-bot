from cv2 import cv2


class Images:
    def __init__(self, theme='default'):
        from src.config import Config
        self.config = Config().read()

        if self.config['app']['theme']:
            self.theme = self.config['app']['theme']
        else:
            self.theme = theme

    def image(self, image, theme=False, newPath=None):
        path = './images/themes/default/'
        if theme == True:
            path = './images/themes/' + self.theme + '/'

        if newPath != None:
            path = newPath

        return cv2.imread(path + image + '.png')
