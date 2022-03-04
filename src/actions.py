
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
        from src.actions import Actions
        from src.bcoins import Bcoins
        from src.config import Config
        from src.log import Log
        from src.recognition import Recognition
        from src.treasure_hunt import TreasureHunt
        from src.services.telegram import Telegram
        self.actions = Actions()
        self.bcoins = Bcoins()
        self.config = Config().read()
        self.log = Log()
        self.recognition = Recognition()
        self.treasure_hunt = TreasureHunt()
        self.telegram = Telegram()

    def click(self):
      humanClicker.click()
      return True

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
            self.move((int(random.uniform(x, x+w)),
                      int(random.uniform(y, y+h))), 1)
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

    def move(self, coords, movementInSeconds, forceTime=False):
        self.importLibs()
        speed = self.config['app']['speed']
        if speed == 'fast' and forceTime == False:
            movementInSeconds = 0.5
        humanClicker.move(coords, movementInSeconds)

    def moveTo(self, coords, movementInSeconds, forceTime=False):
        self.importLibs()
        speed = self.config['app']['speed']
        if speed == 'fast' and forceTime == False:
            movementInSeconds = 0.5
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

    def sleep(self, min, max, randomMouseMovement=True, forceTime=False):
        self.importLibs()
        sleep = random.uniform(min, max)
        if randomMouseMovement == True:
            self.randomMouseMovement()

        speed = self.config['app']['speed']
        if speed == 'fast' and forceTime == False:
            sleep = 0
        return time.sleep(sleep)

    def clickNewMap(self):
        self.log.console('New map', emoji='🗺️', color='magenta')
        self.actions.sleep(2, 2, forceTime=True)
        # checkCaptcha()
        self.treasure_hunt.goToMap()
        self.treasure_hunt.generateMapImage()
        self.telegram.sendMapReport(callTreasureHuntMethods=False)
        self.treasure_hunt.chestEstimate()

        self.bcoins.openYourChestWindow()
        self.telegram.sendBCoinReport(callTreasureHuntMethods=False)
        self.bcoins.getBcoins()

    def refreshPage(self):
        self.importLibs()
        self.log.console('Refreshing page', services=True,
                         emoji='🔃', color='green')
        pyautogui.hotkey('ctrl', 'shift', 'r')

    def show(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)
