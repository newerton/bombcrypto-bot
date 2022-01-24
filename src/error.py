import pyautogui


class Errors:
    def importLibs(self):
        from src.actions import Actions
        from src.auth import Auth
        from src.config import Config
        from src.recognition import Recognition
        from src.images import Images
        from src.log import Log
        from src.services.telegram import Telegram
        self.actions = Actions()
        self.auth = Auth()
        self.config = Config().read()
        self.recognition = Recognition()
        self.images = Images()
        self.log = Log()
        self.telegram = Telegram()

    def verify(self):
        self.importLibs()
        thresholdError = self.config['threshold']['error_message']

        title_error = self.images.image('title_error', theme=True)
        ok_button = self.images.image('ok_button')
        connect_wallet_button = self.images.image('connect_wallet_button')

        if self.recognition.positions(title_error, thresholdError) is not False:
            self.log.console('Error detected, trying to resolve',
                             services=True, emoji='💥', color='red')
            self.telegram.sendPrint()
            self.actions.clickButton(ok_button)
            self.actions.refreshPage()
            self.recognition.waitForImage(connect_wallet_button)
            self.auth.login()
        else:
            return False
