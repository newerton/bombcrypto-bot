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
        from src.treasure_hunt import TreasureHunt
        self.actions = Actions()
        self.auth = Auth()
        self.errors = Errors()
        self.images = Images()
        self.recognition = Recognition()
        self.log = Log()
        self.treasureHunt = TreasureHunt()

    def getMoreHeroes(self, heroesMode=None):

        global next_refresh_heroes
        global heroes_clicked

        self.importLibs()

        mode = self.config['heroes']['mode']
        if mode in ["all", 'workall', 'full', 'green']:
          self.log.console('Search for heroes to work', emoji='🏢', color='green')

        self.goToHeroes()

        if heroesMode is not None:
            mode = heroesMode

        if mode == 'all' or mode == 'workall':
            self.log.console('Sending all heroes to work!',
                             services=True, emoji='⚒️', color='green')
        elif mode == 'full':
            self.log.console(
                'Sending heroes with full stamina bar to work!',
                services=True,
                emoji='⚒️',
                color='green')
        elif mode == 'green':
            self.log.console(
                'Sending heroes with green stamina bar to work!',
                services=True,
                emoji='⚒️',
                color='green')
        elif mode == 'restall':
            self.log.console(
                'Put the heroes to rest',
                services=True,
                emoji='💤',
                color='green')
        else:
            self.log.console('Sending all heroes to work!',
                             services=True,
                             emoji='⚒️',
                             color='green')

        if mode == 'all' or mode == 'workall':
            self.clickSendAllButton()
            return

        if mode == 'restall':
            self.clickRestAllButton()
            return

        scrolls_attempts = self.config['heroes']['list']['scroll_attempts']
        next_refresh_heroes = random.uniform(
            self.config['time_intervals']['send_heroes_for_work'][0],
            self.config['time_intervals']['send_heroes_for_work'][1]
        )

        buttonsClicked = 0
        heroes_clicked = 0
        while(scrolls_attempts > 0):
            if mode == 'full':
                buttonsClicked = self.clickFullBarButtons()
                if buttonsClicked is not None:
                    heroes_clicked += buttonsClicked
            elif mode == 'green':
                buttonsClicked = self.clickGreenBarButtons()
                if buttonsClicked is not None:
                    heroes_clicked += buttonsClicked

            if buttonsClicked == 0 or buttonsClicked is None:
                scrolls_attempts = scrolls_attempts - 1
                self.scroll()
            self.actions.sleep(1, 1, randomMouseMovement=False, forceTime=True)

        self.log.console('{} total heroes sent since the bot started'.format(
            heroes_clicked_total), services=True, emoji='🦸', color='yellow')

        self.treasureHunt.goToMap()
        # pyautogui.hotkey('ctrl', 'shift', 'r') # bug - no broken last item

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

        title_heroes_list = self.images.image('title_heroes_list', theme=True)
        character_indicator_pos = self.recognition.positions(title_heroes_list)
        if character_indicator_pos is False:
            return

        x, y, _, h = character_indicator_pos[0]
        scrollHeight = int(y+420)
        self.actions.move(
            (int(x), scrollHeight), np.random.randint(1, 2))

        self.actions.sleep(0.5, 0.5, randomMouseMovement=False, forceTime=True)
        pyautogui.mouseDown(button='left')
        moveCoordinates = (int(x), int(y+h+2))
        self.actions.move(moveCoordinates, 1, forceTime=True)
        self.actions.sleep(0.5, 0.5, randomMouseMovement=False, forceTime=True)
        pyautogui.mouseUp(button='left')
        self.actions.sleep(1, 1, randomMouseMovement=False, forceTime=True)

    def clickFullBarButtons(self):
        self.importLibs()
        offset = self.config['offsets']['work_button_full']
        threshold = self.config['threshold']

        workButtons = self.checkWorkButton()
        if workButtons is False:
            return

        bar_full_stamina = self.images.image('bar_full_stamina')
        bars = self.recognition.positions(
            bar_full_stamina, threshold=threshold['heroes_full_bar'])

        return self.barButtons(bars, workButtons, offset, 'full')

    def clickGreenBarButtons(self):
        self.importLibs()
        offset = self.config['offsets']['work_button_green']
        threshold = self.config['threshold']

        workButtons = self.checkWorkButton()
        if workButtons is False:
            return

        bar_green_stamina = self.images.image('bar_green_stamina')
        bars = self.recognition.positions(
            bar_green_stamina, threshold=threshold['heroes_green_bar'], debug=True)

        return self.barButtons(bars, workButtons, offset, 'green')

    def clickSendAllButton(self):
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

    def clickRestAllButton(self):
        self.importLibs()
        threshold = self.config['threshold']

        rest_all_heroes_button = self.images.image('rest_all_heroes_button')
        send_all_heroes_button = self.images.image('send_all_heroes_button')

        rest_all = self.recognition.positions(
            rest_all_heroes_button, threshold=threshold['heroes_rest_all'])

        if rest_all is False:
            return

        self.actions.clickButton(rest_all_heroes_button)
        self.recognition.waitForImage(send_all_heroes_button)

    def barButtons(self, bars_elements, workButtons, offset, type):
        if bars_elements is False:
            return

        if self.config['log']['debug'] is not False:
            self.log.console('%d STAMINA bars detected' %
                             len(bars_elements), emoji='🟩', color='red')
            self.log.console('%d WORK buttons detected' %
                             len(workButtons), emoji='🔳', color='red')

        not_working_bars = []
        for bar in bars_elements:
            isWorking = self.isWorking(bar, workButtons)
            if not isWorking:
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

    def checkWorkButton(self):
        threshold = self.config['threshold']
        work_button = self.images.image('work_button')
        return self.recognition.positions(
            work_button, threshold=threshold['work_button'], debug=True)
