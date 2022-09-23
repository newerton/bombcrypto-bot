from cv2 import cv2

import numpy as np
import time


class Recognition:
    def importLibs(self):
        from src.actions import Actions
        from src.config import Config
        from src.desktop import Desktop
        from src.images import Images
        from src.recognition import Recognition
        self.actions = Actions()
        self.config = Config().read()
        self.desktop = Desktop()
        self.images = Images()
        self.recognition = Recognition()

    def positions(self, target, threshold=None, baseImage=None, returnArray=False):
        self.importLibs()
        if threshold == None:
            threshold = self.config['threshold']['default']

        if baseImage is None:
            img = self.desktop.printScreen()
        else:
            img = baseImage

        w = target.shape[1]
        h = target.shape[0]

        result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)

        yloc, xloc = np.where(result >= threshold)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])

        rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.2)

        if self.config['log']['show_print'] is not False:
            img2 = img.copy()
            for r in rectangles:
                cv2.rectangle(img2, (r[0], r[1]),
                              (r[0]+w, r[1]+h), (0, 0, 255), 2)
            cv2.imshow("detected", img2)
            cv2.waitKey(0)
            self.actions.sleep(1, 1, forceTime=True)

        if returnArray is False:
            if len(rectangles) > 0:
                return rectangles
            else:
                return False
        else:
            return rectangles

    def waitForImage(self, images, timeout=30, threshold=0.5, multiple=False):
        self.importLibs()
        start = time.time()
        while True:
            if multiple is not False:
                for img in images:
                    matches = self.recognition.positions(
                        img, threshold=threshold)
                    if matches is False:
                        hast_timed_out = time.time()-start > timeout
                        if hast_timed_out is not False:
                            return False
                        continue
                    return True
            else:
                matches = self.recognition.positions(
                    images, threshold=threshold)
                if matches is False:
                    hast_timed_out = time.time()-start > timeout
                    if hast_timed_out is not False:
                        return False
                    continue
                elif matches is not False:
                    return True
                else:
                    return False

    def currentScreen(self):
        self.importLibs()

        back_button = self.images.image('back_button')
        adventure = self.images.image('adventure')
        connect_wallet_button = self.images.image('connect_wallet_button')
        title_heroes_list = self.images.image('title_heroes_list', theme=True)
        title_login = self.images.image('title_login', theme=True)

        if self.recognition.positions(back_button) is not False:
            return "map"
        elif self.recognition.positions(adventure) is not False:
            return "main"
        elif self.recognition.positions(connect_wallet_button) is not False:
            return "login"
        elif self.recognition.positions(title_login) is not False:
            return "login"
        elif self.recognition.positions(title_heroes_list) is not False:
            return "character"
        else:
            return "unknown"
