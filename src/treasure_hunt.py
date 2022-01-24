import cv2
import pyautogui

class TreasureHunt:
    MAP_IMAGE = './temp/map.png'

    def importLibs(self):
        from src.actions import Actions
        from src.auth import Auth
        from src.desktop import Desktop
        from src.config import Config
        from src.images import Images
        from src.log import Log
        from src.recognition import Recognition
        from src.treasure_hunt import TreasureHunt
        self.actions = Actions()
        self.auth = Auth()
        self.desktop = Desktop()
        self.config = Config().read()
        self.images = Images()
        self.recognition = Recognition()
        self.log = Log()
        self.treasure_hunt = TreasureHunt()

    def goToMap(self):
        self.importLibs()
        currentScreen = self.recognition.currentScreen()

        treasure_hunt_banner = self.images.image('treasure_hunt_banner')
        close_button = self.images.image('close_button')

        self.log.console('Entering treasure hunt', emoji='▶️', color='yellow')

        if currentScreen == "main":
            self.actions.clickButton(treasure_hunt_banner)
        if currentScreen == "character":
            if self.actions.clickButton(close_button):
                self.actions.clickButton(treasure_hunt_banner)
        if currentScreen == "unknown" or currentScreen == "login":
            self.auth.checkLogout()
        self.actions.sleep(1, 1, forceTime=True, randomMouseMovement=False)

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
        value01 = totalChest01 * chestValues["chest_01"]
        value02 = totalChest02 * chestValues["chest_02"]
        value03 = totalChest03 * chestValues["chest_03"]
        value04 = totalChest04 * chestValues["chest_04"]

        total = value01 + value02 + value03 + value04

        report = f"""
Possible quantity chest per type:
🟤 - {totalChest01}
🟣 - {totalChest02}
🟡 - {totalChest03}
🔵 - {totalChest04}
🏛️ - {totalChestJail}
🗝️ - {totalChestKey}

🤑 Possible amount: {total:.3f} BCoin
"""
        reportWithoutEmoji = f"""
Possible quantity chest per type:
Brown - {totalChest01}
Purple - {totalChest02}
Yellow - {totalChest03}
Blue - {totalChest04}
Jail - {totalChestJail}
Key - {totalChestKey}

Possible amount: {total:.3f} BCoin
"""
        try:
            self.log.console(report, services=True)
        except UnicodeEncodeError:
            self.log.console(reportWithoutEmoji, services=True)

    def totalChestsByMap(self, baseImage):
        threshold = self.config['threshold']['chest']
        thresholdJail = self.config['threshold']['jail']

        chest_01_closed = self.images.image(
            'chest_01_closed', newPath='./images/themes/default/chests/')
        chest_02_closed = self.images.image(
            'chest_02_closed', newPath='./images/themes/default/chests/')
        chest_03_closed = self.images.image(
            'chest_03_closed', newPath='./images/themes/default/chests/')
        chest_04_closed = self.images.image(
            'chest_04_closed', newPath='./images/themes/default/chests/')
        chest_jail_closed = self.images.image(
            'chest_jail_closed', newPath='./images/themes/default/chests/')
        chest_key_closed = self.images.image(
            'chest_key_closed', newPath='./images/themes/default/chests/')

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

        chest_01_hit = self.images.image(
            'chest_01_hit', newPath='./images/themes/default/chests/')
        chest_02_hit = self.images.image(
            'chest_02_hit', newPath='./images/themes/default/chests/')
        chest_03_hit = self.images.image(
            'chest_03_hit', newPath='./images/themes/default/chests/')
        chest_04_hit = self.images.image(
            'chest_04_hit', newPath='./images/themes/default/chests/')
        chest_jail_hit = self.images.image(
            'chest_jail_hit', newPath='./images/themes/default/chests/')
        chest_key_hit = self.images.image(
            'chest_key_hit', newPath='./images/themes/default/chests/')

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
