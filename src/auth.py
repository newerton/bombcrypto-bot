import pyautogui
import os

login_attempts = 0


class Auth:
    def importLibs(self):
        from src.actions import Actions
        from src.application import Application
        from src.config import Config
        from src.error import Errors
        from src.images import Images
        from src.recognition import Recognition
        from src.log import Log
        from src.services.telegram import Telegram
        self.accounts = Config().accounts()
        self.actions = Actions()
        self.application = Application()
        self.config = Config().read()
        self.errors = Errors()
        self.images = Images()
        self.recognition = Recognition()
        self.log = Log()
        self.telegram = Telegram()

    def login(self):
        global login_attempts
        self.importLibs()

        account_active = int(os.environ['ACTIVE_BROWSER'])

        self.actions.randomMouseMovement()
        metamaskData = self.config['metamask']
        authenticate = self.config['app']['authenticate']

        connect_wallet_button = self.images.image('connect_wallet_button')
        connect_metamask_button = self.images.image('connect_metamask_button')
        metamask_sign_button = self.images.image('metamask_sign_button')
        metamask_unlock_button = self.images.image('metamask_unlock_button')
        treasure_hunt_banner = self.images.image('treasure_hunt_banner')
        username_icon = self.images.image('username_icon')
        password_icon = self.images.image('password_icon')
        login_button = self.images.image('login_button')

        if self.actions.clickButton(connect_wallet_button):
            self.log.console(
                'Connect game button detected', emoji='👍', color='green')
            self.actions.sleep(1, 2)
            # checkCaptcha()
            self.recognition.waitForImage(connect_metamask_button)

        if(authenticate is True):
            username_icon_position = self.recognition.positions(username_icon)
            password_icon_position = self.recognition.positions(password_icon)

            if username_icon_position is not False:
                username = self.accounts[account_active]['username']
                password = self.accounts[account_active]['password']

                x, y, _, _ = username_icon_position[0]
                self.actions.move((int(x+100), int(y+10)), 1)
                if(self.actions.click()):
                    self.actions.sleep(1, 1, forceTime=True)
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(username, interval=0.1)
                    pyautogui.hotkey('tab')
                    pyautogui.typewrite(password, interval=0.1)

            if self.actions.clickButton(login_button):
                self.log.console(
                    'Found login button. Waiting to check if logged in', emoji='✔️', color='green')

                self.actions.sleep(1, 3, forceTime=True)
                self.application.loggingWithUsernameAndPasswordNotAllowTransactions()
                self.application.advertisingBanner()

                self.recognition.waitForImage(treasure_hunt_banner, timeout=30)
                self.errors.verify()
        else:
            if self.actions.clickButton(connect_metamask_button):
                self.log.console(
                    'Connect metamask button detected, logging in!', emoji='🎉', color='green')
                self.actions.sleep(1, 2)
                self.recognition.waitForImage(
                    (metamask_sign_button, metamask_unlock_button), multiple=True)

            metamask_unlock_coord = self.recognition.positions(
                metamask_unlock_button)
            if metamask_unlock_coord is not False:
                if(metamaskData["enable"] is False):
                    self.log.console(
                        'Metamask locked! But login with password is disabled, exiting', emoji='🔒', color='red')
                    self.application.stop()
                self.log.console(
                    'Found unlock button. Waiting for password', emoji='🔓', color='yellow')
                password = metamaskData["password"]
                pyautogui.typewrite(password, interval=0.1)
                self.actions.sleep(1, 2)
                if self.actions.clickButton(metamask_unlock_button):
                    self.log.console('Unlock button clicked',
                                     emoji='🔓', color='green')

            if self.actions.clickButton(metamask_sign_button):
                self.log.console(
                    'Found sign button. Waiting to check if logged in', emoji='✔️', color='green')
                self.actions.sleep(5, 7, forceTime=True)

                if self.actions.clickButton(metamask_sign_button):
                    self.log.console(
                        'Found glitched sign button. Waiting to check if logged in', emoji='✔️', color='yellow')
                self.recognition.waitForImage(treasure_hunt_banner, timeout=30)
                self.errors.verify()

        if self.recognition.currentScreen() == "main":
            self.log.console('Logged in', services=True,
                             emoji='🎉', color='green')
            return True
        else:
            self.log.console('Login failed, trying again',
                             emoji='😿', color='red')
            login_attempts += 1

            if (login_attempts > 2):
                self.telegram.sendPrint()
                self.log.console('+3 login attempts, retrying',
                                 services=True, emoji='🔃', color='red')
                login_attempts = 0
                self.errors.verify()
                self.actions.refreshPage()
                self.actions.sleep(1, 1, forceTime=True,
                                   randomMouseMovement=False)
            self.login()

        self.errors.verify()

    def checkLogout(self):
        self.importLibs()

        connect_wallet_button = self.images.image('connect_wallet_button')
        metamask_cancel_button = self.images.image('metamask_cancel_button')
        metamask_sign_button = self.images.image('metamask_sign_button')

        currentScreen = self.recognition.currentScreen()
        if currentScreen == "unknown" or currentScreen == "login":
            if self.recognition.positions(connect_wallet_button) is not False:
                self.telegram.sendPrint()
                self.log.console('Logout detected',
                                 services=True, emoji='😿', color='red')
                self.actions.refreshPage()
                self.actions.sleep(4, 4, forceTime=True)
                self.recognition.waitForImage(connect_wallet_button)
                self.login()
            elif self.recognition.positions(metamask_sign_button):
                self.log.console('Sing button detected',
                                 services=True, emoji='✔️', color='green')
                if self.actions.clickButton(metamask_cancel_button):
                    self.log.console('Metamask is glitched, fixing',
                                     services=True, emoji='🙀', color='yellow')
            else:
                return False

        else:
            return False
