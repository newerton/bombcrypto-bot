import os
import cv2


class Game:
    MAP_IMAGE = './temp/map.png'

    def importLibs(self):
        from src.actions import Actions
        from src.amazon_survival import AmazonSurvival
        from src.config import Config
        from src.desktop import Desktop
        from src.images import Images
        from src.log import Log
        from src.recognition import Recognition
        from src.tokens import Tokens
        from src.treasure_hunt import TreasureHunt
        from src.services.telegram import Telegram

        self.accounts = Config().accounts()
        self.actions = Actions()
        self.amazon_survival = AmazonSurvival()
        self.config = Config().read()
        self.desktop = Desktop()
        self.images = Images()
        self.log = Log()
        self.recognition = Recognition()
        self.tokens = Tokens()
        self.treasure_hunt = TreasureHunt()
        self.telegram = Telegram()

    def goToMap(self):
        self.importLibs()
        account_active = int(os.environ['ACTIVE_BROWSER'])
        mode = self.accounts[account_active]['mode']

        if mode == "treasure_hunt":
            self.treasure_hunt.goToMap()
        elif mode == "amazon_survival":
            self.amazon_survival.goToMap()

    def clickNewMap(self):
        self.importLibs()
        self.log.console('New map', emoji='🗺️', color='magenta')
        self.actions.sleep(2, 2, forceTime=True)

        self.generateMapImage()
        self.telegram.sendMapReport(callMapMethods=False)
        self.chestEstimate()

        self.tokens.openYourChestWindow()
        self.telegram.sendTokenReport(callMapMethods=False)
        self.tokens.getSens()
        self.tokens.getBcoins()

    def generateMapImage(self):
        back_button_image = self.images.image('back_button')
        fullscreen_button_image = self.images.image('full_screen_button')
        self.actions.sleep(1, 1)
        back_button = self.recognition.positions(
            back_button_image, returnArray=True)
        fullscreen_button = self.recognition.positions(
            fullscreen_button_image, returnArray=True)

        if len(back_button) <= 0 or len(fullscreen_button) <= 0:
            return
        x1, y1, _, _ = back_button[0]
        x2, y2, w2, _ = fullscreen_button[0]

        newY0 = y1
        newY1 = y2
        newX0 = x1
        newX1 = x2 + w2

        screenshot = self.desktop.printScreen()
        cropped = screenshot[newY0:newY1, newX0:newX1]
        cv2.imwrite(self.MAP_IMAGE, cropped)
        self.log.console('Map image created', services=False, emoji='🪟')
        self.actions.sleep(1, 1)

    def chestEstimate(self):
        image = cv2.imread(self.MAP_IMAGE)
        totalChest = self.totalChestsByMap(image)

        totalChest01 = totalChest['totalChest01']
        totalChest02 = totalChest['totalChest02']
        totalChest03 = totalChest['totalChest03']
        totalChest04 = totalChest['totalChest04']
        totalChestJail = totalChest['totalChestJail']
        totalChestKey = totalChest['totalChestKey']

        chestValues = self.config['chests']['values']
        divide = chestValues["divide"]
        value01 = totalChest01 * chestValues["chest_01"]
        value02 = totalChest02 * chestValues["chest_02"]
        value03 = totalChest03 * chestValues["chest_03"]
        value04 = totalChest04 * chestValues["chest_04"]

        total = (value01 + value02 + value03 + value04) / divide

        report = f"""
Possible quantity chest per type:
🟤 - {totalChest01}
🟣 - {totalChest02}
🟡 - {totalChest03}
🔵 - {totalChest04}
🏛️ - {totalChestJail}
🗝️ - {totalChestKey}

🤑 Possible amount: {total:.3f} SEN
"""
        reportWithoutEmoji = f"""
Possible quantity chest per type:
Brown - {totalChest01}
Purple - {totalChest02}
Yellow - {totalChest03}
Blue - {totalChest04}
Jail - {totalChestJail}
Key - {totalChestKey}

Possible amount: {total:.3f} SEN
"""
        try:
            self.log.console(report, services=True)
        except UnicodeEncodeError:
            self.log.console(reportWithoutEmoji, services=True)

    def totalChestsByMap(self, baseImage):
        account_active = int(os.environ['ACTIVE_BROWSER'])
        mode = self.accounts[account_active]['mode']
        threshold = self.config['threshold']['chest']
        thresholdJail = self.config['threshold']['jail']
        path = './images/themes/default/chests/{}/'.format(mode)

        chest_01_closed = self.images.image('chest_01_closed', path=path)
        chest_02_closed = self.images.image('chest_02_closed', path=path)
        chest_03_closed = self.images.image('chest_03_closed', path=path)
        chest_04_closed = self.images.image('chest_04_closed', path=path)
        chest_jail_closed = self.images.image('chest_jail_closed', path=path)
        chest_key_closed = self.images.image('chest_key_closed', path=path)

        c01 = len(self.recognition.positions(
            chest_01_closed, threshold, baseImage, returnArray=True))
        c02 = len(self.recognition.positions(
            chest_02_closed, threshold, baseImage, returnArray=True))
        c03 = len(self.recognition.positions(
            chest_03_closed, threshold, baseImage, returnArray=True))
        c04 = len(self.recognition.positions(
            chest_04_closed, threshold, baseImage, returnArray=True))
        jail = len(self.recognition.positions(
            chest_jail_closed, thresholdJail, baseImage, returnArray=True))
        key = len(self.recognition.positions(
            chest_key_closed, thresholdJail, baseImage, returnArray=True))

        chest_01_hit = self.images.image('chest_01_hit', path=path)
        chest_02_hit = self.images.image('chest_02_hit', path=path)
        chest_03_hit = self.images.image('chest_03_hit', path=path)
        chest_04_hit = self.images.image('chest_04_hit', path=path)
        chest_jail_hit = self.images.image('chest_jail_hit', path=path)
        chest_key_hit = self.images.image('chest_key_hit', path=path)

        c01_hit = len(self.recognition.positions(
            chest_01_hit, threshold, baseImage, returnArray=True))
        c02_hit = len(self.recognition.positions(
            chest_02_hit, threshold, baseImage, returnArray=True))
        c03_hit = len(self.recognition.positions(
            chest_03_hit, threshold, baseImage, returnArray=True))
        c04_hit = len(self.recognition.positions(
            chest_04_hit, threshold, baseImage, returnArray=True))
        jail_hit = len(self.recognition.positions(
            chest_jail_hit, thresholdJail, baseImage, returnArray=True))
        key_hit = len(self.recognition.positions(
            chest_key_hit, thresholdJail, baseImage, returnArray=True))

        totalChest01 = c01 + c01_hit
        totalChest02 = c02 + c02_hit
        totalChest03 = c03 + c03_hit
        totalChest04 = c04 + c04_hit
        totalChestJail = jail + jail_hit
        totalChestKey = key + key_hit

        return {
            'totalChest01': totalChest01,
            'totalChest02': totalChest02,
            'totalChest03': totalChest03,
            'totalChest04': totalChest04,
            'totalChestJail': totalChestJail,
            'totalChestKey': totalChestKey,
        }
