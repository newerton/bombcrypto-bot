from pyclick import HumanClicker

import os
import sys
import time

import src.external.pygetwindow as botMultiAccount
from src.external.pygetwindow import PyGetWindowException

humanClicker = HumanClicker()


class MultiAccount:
    def __init__(self):
        from src.config import Config
        from src.log import Log
        self.config = Config().read()
        self.log = Log()
        self.accounts = None
        self.check_for_updates = 60
        self.next_refresh_heroes = self.config['time_intervals']['send_heroes_for_work'][0]
        self.next_refresh_heroes_positions = self.config['time_intervals']['refresh_heroes_positions'][0]

    def importLibs(self):
        from src.actions import Actions
        from src.application import Application
        from src.auth import Auth
        from src.captcha import Captcha
        from src.error import Errors
        from src.heroes import Heroes
        from src.images import Images
        from src.recognition import Recognition
        from src.treasure_hunt import TreasureHunt
        self.actions = Actions()
        self.application = Application()
        self.auth = Auth()
        self.captcha = Captcha()
        self.errors = Errors()
        self.heroes = Heroes()
        self.images = Images()
        self.recognition = Recognition()
        self.treasure_hunt = TreasureHunt()

    def start(self):
        self.importLibs()
        multiAccount = self.config['app']['multi_account']['enable']
        if multiAccount != True:
            self.log.console('Multi account disabled', emoji='🧾', color='cyan')
            self.botSingle()

        if multiAccount == True and os.name == 'nt':
            self.log.console('Multi account enabled', emoji='🧾', color='cyan')
            self.botMultiAccount()

        if multiAccount == True and os.name == 'posix':
            self.log.console('Multi account enabled', emoji='🧾', color='cyan')
            self.botMultiAccount()

    def startOnlyMapAction(self):
        self.importLibs()
        self.log.console('Multi account disabled', emoji='🧾', color='cyan')
        self.botSingleOnlyMap()

    def botSingle(self):

        last = {
            "account": 1,
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "refresh_heroes": 0,
            "check_updates": 0
        }

        while True:
            self.steps(last)

    def botSingleOnlyMap(self):

        last = {
            "new_map": 0,
        }

        while True:
            self.stepsOnlyMap(last)

    def botMultiAccount(self):
        title = self.config['app']['multi_account']['window_title']
        total_accounts = len(self.accounts)

        try:
            windows = []
            count = 1
            for w in botMultiAccount.getAllWindows():
                browserTitle = self.browserTitle(w.title)
                lowerTitle = browserTitle.lower().startswith(title)
                if lowerTitle == True and count <= total_accounts:
                    windows.append({
                        "account": (count),
                        "window": w,
                        "login": 0,
                        "heroes": 0,
                        "new_map": 0,
                        "refresh_heroes": 0,
                        "check_updates": 0
                    })
                    count += 1

            while True:
                for last in windows:
                    window = last["window"]
                    self.activeWindow(last, window)

        except PyGetWindowException:
            self.log.console(
                'Error: Multi Account (PyGetWindow): Trying to resolve, check your farm.', emoji='💥', color='cyan')
            self.botMultiAccount()

    def steps(self, last):
        os.environ['ACTIVE_BROWSER'] = str(last['account'])

        new_map_button = self.images.image('new_map_button')
        run_time_app = self.config['app']['run_time_app']

        currentScreen = self.recognition.currentScreen()

        if currentScreen == "login":
            self.auth.login()

        self.errors.verify()

        now = time.time()

        if now - last["heroes"] > self.next_refresh_heroes * 60:
            last["heroes"] = now
            last["refresh_heroes"] = now
            self.heroes.getMoreHeroes()

        if currentScreen == "main":
            self.treasure_hunt.goToMap()

        if currentScreen == "treasure_hunt":
            if self.actions.clickButton(new_map_button):
                last["new_map"] = now
                self.actions.clickNewMap()

        if now - last["refresh_heroes"] > self.next_refresh_heroes_positions * 60:
            last["refresh_heroes"] = now
            self.heroes.refreshHeroesPositions()

        if now - last["check_updates"] > self.check_for_updates * 60:
            last["check_updates"] = now
            self.application.checkUpdate()

        self.auth.checkLogout()
        sys.stdout.flush()
        self.actions.sleep(run_time_app, run_time_app,
                           randomMouseMovement=False)
        self.application.checkThreshold()

    def stepsOnlyMap(self, last):
        new_map_button = self.images.image('new_map_button')
        run_time_app = self.config['app']['run_time_app']

        currentScreen = self.recognition.currentScreen()

        self.errors.verify()

        now = time.time()

        if currentScreen == "treasure_hunt":
            if self.actions.clickButton(new_map_button):
                last["new_map"] = now
                self.actions.clickNewMap()

        sys.stdout.flush()
        self.actions.sleep(run_time_app, run_time_app,
                           randomMouseMovement=False)
        self.application.checkThreshold()

    def activeWindow(self, last, window):
        window_fullscreen = self.config['app']['multi_account']['window_fullscreen']
        browserTitle = self.browserTitle(window.title)

        window = last["window"]
        windowLeft = window.left
        windowTop = window.top
        windowWidth = window.width
        windowHeight = window.height
        window.maximize()
        if window_fullscreen is not True:
            self.actions.move(window.center, 0)
            humanClicker.click()
            self.actions.sleep(1, 1, forceTime=True)
        window.activate()
        self.log.console('Browser Active: ' + browserTitle,
                         emoji='🪟', color='cyan')
        self.actions.sleep(2, 2, forceTime=True)
        self.steps(last)
        if window_fullscreen is not True:
            window.restore()
            window.resizeTo(windowWidth, windowHeight)
            window.moveTo(windowLeft, windowTop)
            self.actions.sleep(1, 1, forceTime=True)

    def browserTitle(self, title):
        titleFormatter = self.unicodeToAscii(title)
        if(titleFormatter.startswith("b'") and titleFormatter.endswith("'")):
            titleFormatter = titleFormatter[2:-1]
        return titleFormatter.strip()

    def unicodeToAscii(self, text):
        return (
            str(text)
            .replace('\\xc3\\xa9', 'e')
            .replace('\\xc2\\xb7', '·')
            .replace('\\xe2\\x80\\x99', "'")
            .replace('\\xe2\\x80\\x9c', '"')
            .replace('\\xe2\\x80\\x9d', '"')
            .replace('\\xe2\\x80\\x9e', '"')
            .replace('\\xe2\\x80\\x9f', '"')
            .replace('\\xe2\\x80\\x9c', '"')
            .replace('\\xe2\\x80\\x93', '-')
            .replace('\\xe2\\x80\\x92', '-')
            .replace('\\xe2\\x80\\x94', '-')
            .replace('\\xe2\\x80\\x94', '-')
            .replace('\\xe2\\x80\\x98', "'")
            .replace('\\xe2\\x80\\x9b', "'")
            .replace('\\xe2\\x80\\x90', '-')
            .replace('\\xe2\\x80\\x91', '-')
            .replace('\\xe2\\x80\\xb2', "'")
            .replace('\\xe2\\x80\\xb3', "'")
            .replace('\\xe2\\x80\\xb4', "'")
            .replace('\\xe2\\x80\\xb5', "'")
            .replace('\\xe2\\x80\\xb6', "'")
            .replace('\\xe2\\x80\\xb7', "'")
            .replace('\\xe2\\x81\\xba', " ")
            .replace('\\xe2\\x81\\xbb', "-")
            .replace('\\xe2\\x81\\xbc', "=")
            .replace('\\xe2\\x81\\xbd', "(")
            .replace('\\xe2\\x81\\xbe', ")")
        )
