class TreasureHunt:
    def importLibs(self):
        from src.actions import Actions
        from src.auth import Auth
        from src.images import Images
        from src.log import Log
        from src.recognition import Recognition

        self.actions = Actions()
        self.auth = Auth()
        self.images = Images()
        self.recognition = Recognition()
        self.log = Log()

    def goToMap(self):
        self.importLibs()
        currentScreen = self.recognition.currentScreen()

        adventure = self.images.image('adventure')
        self.log.console('Entering treasure hunt', emoji='🎮', color='yellow')

        if currentScreen == "main":
            self.actions.clickButton(adventure)
        if currentScreen == "character":
            close_button = self.images.image('close_button')
            if self.actions.clickButton(close_button):
                self.actions.sleep(2, 2, forceTime=True, randomMouseMovement=False)
                self.actions.clickButton(adventure)
        if currentScreen == "unknown" or currentScreen == "login":
            self.auth.checkLogout()
        self.actions.sleep(2, 2, forceTime=True, randomMouseMovement=False)
