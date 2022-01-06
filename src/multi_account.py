from pyclick import HumanClicker

import os
import sys
import time

if os.name == 'nt':
    import pygetwindow as botMultiAccount
    from pygetwindow import PyGetWindowException

humanClicker = HumanClicker()

class MultiAccount():
    def __init__(self):
        from src.config import Config
        self.config = Config().read()

        self.check_for_updates = 60
        self.next_refresh_heroes = self.config['time_intervals']['send_heroes_for_work'][0]
        self.next_refresh_heroes_positions = self.config['time_intervals']['refresh_heroes_positions'][0]

    def importLibs(self):
        from src.actions import Actions
        from src.app import App
        from src.auth import Auth
        from src.captcha import Captcha
        from src.error import Errors
        from src.heroes import Heroes
        from src.images import Images
        from src.log import Log
        from src.recognition import Recognition
        self.actions = Actions()
        self.app = App()
        self.auth = Auth()
        self.captcha = Captcha()
        self.errors = Errors()
        self.heroes = Heroes()
        self.images = Images()
        self.log = Log()
        self.recognition = Recognition()

    def start(self):
        self.importLibs()
        multiAccount = self.config['app']['multi_account']['enable']
        if multiAccount != True and os.name == 'nt':
            self.log.console('Multi account DISABLE')
            self.botSingle()

        if multiAccount == True and os.name == 'nt':
            self.log.console('Multi account ENABLE')
            self.botMultiAccountWindows()

        if os.name == 'posix':
            self.log.console('Multi account DISABLE')
            self.botSingle()

    def botSingle(self):
        

        last = {
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "refresh_heroes": 0,
            "check_updates": 0
        }

        while True:
            self.steps(last)

    def botMultiAccountWindows(self):
        title = self.config['app']['multi_account']['window_title']
        window_fullscreen = self.config['app']['multi_account']['window_fullscreen']
        try:
            windows = []
            for w in botMultiAccount.getWindowsWithTitle(title):
                if w.title.startswith(title) == True:
                    windows.append({
                        "window": w,
                        "login": 0,
                        "heroes": 0,
                        "new_map": 0,
                        "refresh_heroes": 0,
                        "check_updates": 0
                    })

            while True:
                for last in windows:
                    window = last["window"]
                    if window_fullscreen == True:
                        window.maximize()
                    humanClicker.move(window.center, 0)
                    humanClicker.click()
                    window.activate()                    
                    time.sleep(2)

                self.steps(last)

        except PyGetWindowException:
            self.log.console(
                'Error: Multi Account (PyGetWindow): Trying to resolve, check your farm.', emoji='💥')
            self.botMultiAccountWindows()

    def steps(self, last):
        treasure_hunt_banner = self.images.image('treasure_hunt_banner')
        new_map_button = self.images.image('new_map_button')
        close_button = self.images.image('close_button')
        run_time_app = self.config['app']['run_time_app']

        currentScreen = self.recognition.currentScreen()

        print('currentScreen', currentScreen)
        if currentScreen == "login":
            self.auth.login()

        self.errors.verify()

        now = time.time()

        if now - last["heroes"] > self.next_refresh_heroes * 60:
            last["heroes"] = now
            last["refresh_heroes"] = now
            self.heroes.getMoreHeroes()

        if currentScreen == "main":
            if self.actions.clickButton(treasure_hunt_banner):
                self.log.console('Entering treasure hunt', emoji='▶️')
                last["refresh_heroes"] = now

        if currentScreen == "treasure_hunt":
            if self.actions.clickButton(new_map_button):
                last["new_map"] = now
                self.actions.clickNewMap()

        if currentScreen == "character":
            self.actions.clickButton(close_button)
            self.actions.sleep(1, 2)

        if now - last["check_updates"] > self.check_for_updates * 60:
            last["check_updates"] = now
            self.app.checkUpdate()

        self.auth.checkLogout()
        sys.stdout.flush()
        self.actions.sleep(run_time_app, run_time_app,
                           randomMouseMovement=False)
        self.app.checkThreshold()
