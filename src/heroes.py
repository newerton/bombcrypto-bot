from cv2 import cv2
from pyclick import HumanClicker

import numpy as np
import pyautogui
import random

humanClicker = HumanClicker()

heroes_clicked = 0
heroes_clicked_total = 0


class Heroes:
    def __init__(self):
        from src.config import Config
        self.config = Config().read()
        self.next_refresh_heroes = self.config['time_intervals']['send_heroes_for_work'][0]
        self.next_refresh_heroes_positions = self.config['time_intervals']['refresh_heroes_positions'][0]

    def importLibs(self):
        from src.actions import Actions
        from src.auth import Auth
        from src.error import Errors
        from src.images import Images
        from src.recognition import Recognition
        from src.log import Log
        self.actions = Actions()
        self.auth = Auth()
        self.errors = Errors()
        self.images = Images()
        self.recognition = Recognition()
        self.log = Log()

    def getMoreHeroes(self):

        global next_refresh_heroes
        global heroes_clicked

        self.importLibs()
        self.log.console('Search for heroes to work', emoji='🏢', color='green')

        self.goToHeroes()

        mode = self.config['heroes']['mode']
        if mode == "all":
            self.log.console('Sending all heroes to work!',
                             services=True, emoji='⚒️', color='green')
        elif mode == "full":
            self.log.console(
                'Sending heroes with full stamina bar to work!', emoji='⚒️', color='green')
        elif mode == "green":
            self.log.console(
                'Sending heroes with green stamina bar to work!', emoji='⚒️', color='green')
        else:
            self.log.console('Sending all heroes to work!',
                             emoji='⚒️', color='green')

        if mode == 'all':
            self.clickSendAllButtons()
            self.goToTreasureHunt()
            return

        buttonsClicked = 0
        heroes_clicked = 0
        empty_scrolls_attempts = self.config['heroes']['list']['scroll_attempts']
        next_refresh_heroes = random.uniform(
            self.config['time_intervals']['send_heroes_for_work'][0],
            self.config['time_intervals']['send_heroes_for_work'][1]
        )

        while(empty_scrolls_attempts > 0):
            if mode == 'full':
                buttonsClicked = self.clickFullBarButtons()
                if buttonsClicked is not None:
                    heroes_clicked += buttonsClicked
            elif mode == 'green':
                buttonsClicked = self.clickGreenBarButtons()
                if buttonsClicked is not None:
                    heroes_clicked += buttonsClicked

            if buttonsClicked == 0 or buttonsClicked is None:
                empty_scrolls_attempts = empty_scrolls_attempts - 1
                self.scroll()
            self.actions.sleep(1, 2)

        self.log.console('{} total heroes sent since the bot started'.format(
            heroes_clicked_total), services=True, emoji='🦸', color='yellow')
        self.goToTreasureHunt()

    def goToHeroes(self):
        self.importLibs()
        currentScreen = self.recognition.currentScreen()

        back_button = self.images.image('back_button')
        menu_heroe_icon = self.images.image('menu_heroe_icon')
        home_button = self.images.image('home_button')

        if currentScreen == "treasure_hunt":
            if self.actions.clickButton(back_button):
                self.actions.sleep(1, 1)
                if self.actions.clickButton(menu_heroe_icon):
                    self.actions.sleep(1, 1)
                    # checkCaptcha()
                    self.recognition.waitForImage(home_button)
        if currentScreen == "main":
            if self.actions.clickButton(menu_heroe_icon):
                self.actions.sleep(1, 1)
                # checkCaptcha()
                self.recognition.waitForImage(home_button)
        if currentScreen == "unknown" or currentScreen == "login":
            self.auth.checkLogout()

    def goToTreasureHunt(self):
        currentScreen = self.recognition.currentScreen()

        treasure_hunt_banner = self.images.image('treasure_hunt_banner')
        close_button = self.images.image('close_button')

        if currentScreen == "main":
            self.actions.clickButton(treasure_hunt_banner)
        if currentScreen == "character":
            if self.actions.clickButton(close_button):
                self.actions.clickButton(treasure_hunt_banner)
        if currentScreen == "unknown" or currentScreen == "login":
            self.auth.checkLogout()

    def refreshHeroesPositions(self):
        self.log.console('Refreshing heroes positions',
                         emoji='🔃', color='yellow')

        global next_refresh_heroes_positions

        next_refresh_heroes_positions = random.uniform(
            self.config['time_intervals']['refresh_heroes_positions'][0],
            self.config['time_intervals']['refresh_heroes_positions'][1]
        )

        currentScreen = self.recognition.currentScreen()

        back_button = self.images.image('back_button')
        treasure_hunt_banner = self.images.image('treasure_hunt_banner')

        if currentScreen == "treasure_hunt":
            if self.actions.clickButton(back_button):
                self.actions.clickButton(treasure_hunt_banner)
                return True
        if currentScreen == "main":
            if self.actions.clickButton(treasure_hunt_banner):
                return True
            else:
                return False
        else:
            return False

    def isWorking(self, bar, buttons):
        y = bar[1]
        for (_, button_y, _, button_h) in buttons:
            isBelow = y < (button_y + button_h)
            isAbove = y > (button_y - button_h)
            if isBelow and isAbove:
                return False
        return True

    def scroll(self):
        self.importLibs()
        offset = self.config['offsets']['work_button_full']
        offset_random = random.uniform(offset[0], offset[1])

        title_heroes_list = self.images.image('title_heroes_list', theme=True)

        character_indicator_pos = self.recognition.positions(title_heroes_list)
        if character_indicator_pos is False:
            return

        x, y, w, h = character_indicator_pos[0]
        self.actions.move(
            (int(x+(w/2)), int(y+h+offset_random)), np.random.randint(1, 2))

        click_and_drag_amount = (-self.config['heroes']
                                 ['list']['click_and_drag_amount'])
        pyautogui.mouseDown(button='left')
        moveCoordinates = (int(x), int(y+click_and_drag_amount))
        self.actions.move(moveCoordinates, np.random.randint(1, 2))
        pyautogui.mouseUp(button='left')

    def clickFullBarButtons(self):
        self.importLibs()
        offset = self.config['offsets']['work_button_full']
        threshold = self.config['threshold']

        bar_full_stamina = self.images.image('bar_full_stamina')

        bars = self.recognition.positions(
            bar_full_stamina, threshold=threshold['heroes_full_bar'])

        return self.barButtons(bars, offset, 'full')

    def clickGreenBarButtons(self):
        self.importLibs()
        offset = self.config['offsets']['work_button_green']
        threshold = self.config['threshold']

        bar_green_stamina = self.images.image('bar_green_stamina')

        bars = self.recognition.positions(
            bar_green_stamina, threshold=threshold['heroes_green_bar'])

        return self.barButtons(bars, offset, 'green')

    def clickSendAllButtons(self):
        self.importLibs()
        threshold = self.config['threshold']

        send_all_heroes_button = self.images.image('send_all_heroes_button')
        rest_all_heroes_button = self.images.image('rest_all_heroes_button')

        send_all = self.recognition.positions(
            send_all_heroes_button, threshold=threshold['heroes_send_all'])

        if send_all is False:
            return

        self.actions.clickButton(send_all_heroes_button)
        self.recognition.waitForImage(rest_all_heroes_button)

    def barButtons(self, bars_elements, offset, type):
        threshold = self.config['threshold']

        work_button = self.images.image('work_button')
        buttons = self.recognition.positions(
            work_button, threshold=threshold['back_button'])

        if bars_elements is False or buttons is False:
            return

        if self.config['log']['debug'] is not False:
            self.log.console('%d green bars detected' %
                             len(bars_elements), emoji='🟩', color='red')
            self.log.console('%d buttons detected' %
                             len(buttons), emoji='🔳', color='red')

        not_working_bars = []
        for bar in bars_elements:
            if not self.isWorking(bar, buttons):
                not_working_bars.append(bar)

        if len(not_working_bars) > 0:
            message = 'Clicking in {} heroes with {} bar detected.'.format(
                len(not_working_bars), type)
            self.log.console(message, emoji='👆', color='green')

        for (x, y, w, h) in not_working_bars:
            offset_random = random.uniform(offset[0], offset[1])
            self.actions.move(
                (int(x+offset_random+(w/2)), int(y+(h/2))),
                np.random.randint(1, 2)
            )
            humanClicker.click()

            global heroes_clicked_total
            global heroes_clicked

            heroes_clicked_total = heroes_clicked_total + 1
            if heroes_clicked > 15:
                self.log.console('Too many hero clicks, try to increase the back_button threshold',
                                 services=True, emoji='⚠️', color='yellow')
                return
            self.actions.sleep(1, 2)
        return len(not_working_bars)
