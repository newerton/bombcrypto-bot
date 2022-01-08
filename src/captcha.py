class Captcha:
    def importLibs(self):
        from src.config import Config
        from src.images import Images
        from src.recognition import Recognition
        from src.log import Log
        self.config = Config().read()
        self.images = Images()
        self.recognition = Recognition()
        self.log = Log()

    def check(self):
        self.importLibs()
        if self.config['app']['captcha'] is not False:
            title_robot = self.images.image('title_robot')
            isCaptcha = self.recognition.positions(title_robot)
            if isCaptcha is not False:
                self.log.console('Captcha detected',
                                 services=True, emoji='🧩', color='green')

                if self.config['app']['captcha'] == 'crazy_numbers':
                    from captchas.crazy_numbers.solveCaptcha import CrazyNumbersCaptcha
                    CrazyNumbersCaptcha().solveCaptcha()
                elif self.config['app']['captcha'] == 'puzzle':
                    from captchas.puzzle.main import PuzzleCaptcha
                    PuzzleCaptcha().solveCaptcha()
                elif self.config['app']['captcha'] == 'reveal_numbers':
                    from captchas.reveal_numbers.main import RevealNumbersCaptcha
                    RevealNumbersCaptcha().solveCaptcha()
                else:
                    return
            else:
                return True
