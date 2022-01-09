
from cv2 import cv2
from pyclick import HumanClicker

import numpy as np
import pyautogui
import random
import time

heroe_clicks = 0
go_work_img = cv2.imread('./targets/go-work.png')
humanClicker = HumanClicker()


class Actions:
    def importLibs(self):
        from src.config import Config
        from src.recognition import Recognition
        from src.log import Log
        from src.services.telegram import Telegram
        self.config = Config().read()
        self.recognition = Recognition()
        self.log = Log()
        self.telegram = Telegram()

    def clickButton(self, image, name=None, timeout=3, threshold=None):
        self.importLibs()
        if(threshold == None):
            threshold = self.config['threshold']['default']

        if not name is None:
            pass

        start = time.time()
        clicked = False
        while(not clicked):
            matches = self.recognition.positions(image, threshold=threshold)
            if(matches is False):
                hast_timed_out = time.time()-start > timeout
                if(hast_timed_out):
                    if not name is None:
                        pass
                    return False
                continue

            x, y, w, h = matches[0]
            self.move((int(random.uniform(x, x+w)), int(random.uniform(y, y+h))), 1)
            humanClicker.click()
            return True

    def clickGoWork(self):
        self.importLibs()
        threshold = self.config['threshold']['go_to_work_btn']
        buttons = self.recognition.positions(go_work_img, threshold=threshold)
        for (x, y, w, h) in buttons:
            self.move((x+(w/2), y+(h/2)), 1)
            humanClicker.click()

            global heroe_clicks

            heroe_clicks = heroe_clicks + 1
            if heroe_clicks > 20:
                self.log.console(
                    'Too many hero clicks, try to increase the go_to_work_btn threshold', emoji='💥', color='red')
                return
        return len(buttons)

    def move(self, coords, movementInSeconds):
        self.importLibs()
        speed = self.config['app']['speed']
        if speed == 'fast':
            movementInSeconds = 0.1
        humanClicker.move(coords, movementInSeconds)

    def moveTo(self, coords, movementInSeconds):
        self.importLibs()
        print(coords[0])
        print(coords[1])
        speed = self.config['app']['speed']
        if speed == 'fast':
            movementInSeconds = 0.1
        humanClicker.moveTo(coords, movementInSeconds)

    def randomMouseMovement(self):
        self.importLibs()
        x, y = pyautogui.size()
        limit = 200
        x = np.random.randint(limit, x - limit)
        y = np.random.randint(limit, y - limit)

        speed = self.config['app']['speed']
        if speed != 'fast':
            self.move((int(x), int(y)), np.random.randint(1, 2))

    def sleep(self, min, max, randomMouseMovement=True):
        self.importLibs()
        sleep = random.uniform(min, max)
        if randomMouseMovement == True:
            self.randomMouseMovement()
        
        speed = self.config['app']['speed']
        if speed == 'fast':
            time.sleep(0)
        return time.sleep(sleep)

    def clickNewMap(self):
        self.log.console('New map', emoji='🗺️', color='magenta')
        # sleep(1, 2)
        # checkCaptcha()
        self.telegram.sendMapReport()
        self.telegram.sendBCoinReport()

    def show(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)
