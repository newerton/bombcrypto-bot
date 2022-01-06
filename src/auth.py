import pyautogui

login_attempts = 0


class Auth:
    def importLibs(self):
        from src.actions import Actions
        from src.config import Config
        from src.error import Errors
        from src.images import Images
        from src.recognition import Recognition
        from src.log import Log
        from src.services.telegram import Telegram
        self.actions = Actions()
        self.config = Config().read()
        self.errors = Errors()
        self.images = Images()
        self.recognition = Recognition()
        self.log = Log()
        self.telegram = Telegram()

    def login(self):
        global login_attempts
        self.importLibs()

        self.actions.randomMouseMovement()
        metamaskData = self.config['metamask']

        connect_wallet_button = self.images.image('connect_wallet_button')
        metamask_cancel_button = self.images.image('metamask_cancel_button')
        metamask_sign_button = self.images.image('metamask_sign_button')
        metamask_unlock_button = self.images.image('metamask_unlock_button')
        treasure_hunt_banner = self.images.image('treasure_hunt_banner')

        if self.actions.clickButton(connect_wallet_button):
            self.log.console(
                'Connect wallet button detected, logging in!', emoji='🎉')
            self.actions.sleep(1, 2)
            # checkCaptcha()
            self.recognition.waitForImage(
                (metamask_sign_button, metamask_unlock_button), multiple=True)

        metamask_unlock_coord = self.recognition.positions(
            metamask_unlock_button)
        if metamask_unlock_coord is not False:
            if(metamaskData["enable_login_metamask"] is False):
                self.log.console(
                    'Metamask locked! But login with password is disabled, exiting', emoji='🔒')
                exit()
            self.log.console(
                'Found unlock button. Waiting for password', emoji='🔓')
            password = metamaskData["password"]
            pyautogui.typewrite(password, interval=0.1)
            self.actions.sleep(1, 2)
            if self.actions.clickButton(metamask_unlock_button):
                self.log.console('Unlock button clicked', emoji='🔓')

        if self.actions.clickButton(metamask_sign_button):
            self.log.console(
                'Found sign button. Waiting to check if logged in', emoji='✔️')
            self.actions.sleep(5, 7)
            if self.actions.clickButton(metamask_sign_button):
                self.log.console(
                    'Found glitched sign button. Waiting to check if logged in', emoji='✔️')
            self.recognition.waitForImage(treasure_hunt_banner, timeout=30)
            self.errors.verify()

        if self.recognition.currentScreen() == "main":
            self.log.console('Logged in', services=True, emoji='🎉')
            return True
        else:
            self.log.console('Login failed, trying again', emoji='😿')
            login_attempts += 1

            if (login_attempts > 3):
                self.telegram.sendTelegramPrint()
                self.log.console('+3 login attempts, retrying',
                                 services=True, emoji='🔃')
                pyautogui.hotkey('ctrl', 'shift', 'r')
                login_attempts = 0

                if self.actions.clickButton(metamask_cancel_button):
                    self.log.console('Metamask is glitched, fixing', emoji='🙀')

                self.recognition.waitForImage(connect_wallet_button)

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
                self.telegram.sendTelegramPrint()
                self.log.console('Logout detected', services=True, emoji='😿')
                self.log.console('Refreshing page', services=True, emoji='🔃')
                pyautogui.hotkey('ctrl', 'shift', 'r')
                self.recognition.waitForImage(connect_wallet_button)
                self.login()
            elif self.recognition.positions(metamask_sign_button):
                self.log.console('Sing button detected',
                                 services=True, emoji='✔️')
                if self.actions.clickButton(metamask_cancel_button):
                    self.log.console('Metamask is glitched, fixing',
                                     services=True, emoji='🙀')
            else:
                return False

        else:
            return False
