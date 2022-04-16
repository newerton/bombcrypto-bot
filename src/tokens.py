from cv2 import cv2
from os import listdir


class Tokens:
    TOKEN_BOX_IMAGE = './temp/bcoin-box.png'

    def importLibs(self):
        from src.actions import Actions
        from src.date import Date
        from src.desktop import Desktop
        from src.images import Images
        from src.log import Log
        from src.recognition import Recognition
        from src.report import Report
        self.actions = Actions()
        self.date = Date()
        self.desktop = Desktop()
        self.images = Images()
        self.log = Log()
        self.recognition = Recognition()
        self.report = Report()

    def getSens(self):
        self.importLibs()
        image = cv2.imread(self.TOKEN_BOX_IMAGE)
        y = 5
        x = 170
        h = 30
        w = 150
        cropped = image[y:y+h, x:x+w]
        digits = self.getDigits(cropped)
        headers = ['date', 'senspark']
        content = [self.date.dateFormatted(), digits.replace('.', ',')]
        self.report.writeCsv('senspark-report', headers, content)
        self.log.console('Senspark: {}'.format(digits), services=True, emoji='🤑')
        return digits

    def getBcoins(self):
        self.importLibs()
        image = cv2.imread(self.TOKEN_BOX_IMAGE)
        y = 52
        x = 170
        h = 30
        w = 150
        cropped = image[y:y+h, x:x+w]
        digits = self.getDigits(cropped)
        headers = ['date', 'bcoins']
        content = [self.date.dateFormatted(), digits.replace('.', ',')]
        self.report.writeCsv('bcoins-report', headers, content)
        self.log.console('Bcoin: {}'.format(digits), services=True, emoji='🤑')
        return digits

    def openYourChestWindow(self):
        self.importLibs()
        self.actionToOpenYourChestWindow()

        box_senspark = self.images.image('box_senspark')
        close_button = self.images.image('close_button')

        box_senspark_positions = self.recognition.positions(
            box_senspark, returnArray=True)
        if len(box_senspark_positions) > 0:
            x, y, w, h = box_senspark_positions[0]
            screenshot = self.desktop.printScreen()
            cropped = screenshot[y: y + h + 50, x: x + (w + 250)]
            cv2.imwrite(self.TOKEN_BOX_IMAGE, cropped)
            self.log.console('Your Chest image created',
                             services=False, emoji='🪟')

        self.actions.clickButton(close_button)
        return True

    def actionToOpenYourChestWindow(self):
        treasure_hunt_banner = self.images.image('treasure_hunt_banner')
        close_button = self.images.image('close_button')
        treasure_chest_button = self.images.image('treasure_chest_button')

        currentScreen = self.recognition.currentScreen()
        if currentScreen == "main":
            if self.actions.clickButton(treasure_hunt_banner):
                self.actions.sleep(2, 2)
        elif currentScreen == "character":
            if self.actions.clickButton(close_button):
                self.actions.sleep(2, 2)
                if self.actions.clickButton(treasure_hunt_banner):
                    self.actions.sleep(2, 2)
        elif currentScreen == "treasure_hunt":
            self.actions.sleep(2, 2)
        else:
            return

        self.log.console('Opening modal Your Chest', services=False, emoji='🪟')
        self.actions.clickButton(treasure_chest_button)
        seconds = 5
        message = 'Wait for {} seconds, to show your TOKENS'.format(seconds)
        self.log.console(message, services=False, emoji='⏳')
        self.actions.sleep(seconds, seconds, forceTime=True)

    def loadImages(self, dir):
        file_names = listdir(dir)
        targets = {}
        for file in file_names:
            path = dir + file
            targets[file.replace('.png', '')] = cv2.imread(path)
        return targets

    def getDigits(self, img, threshold=0.90):
        d = self.loadImages('./images/themes/default/your_chest/v2/')
        digits = []
        for i in range(10):
            template = d[str(i)]

            positions = self.recognition.positions(
                target=template, baseImage=img, threshold=threshold, returnArray=True)
            if len(positions) > 0:
                for position in positions:
                    digits.append({'digit': str(i), 'x': position[0]})

            templateDot = d['dot']
            positionDot = self.recognition.positions(
                target=templateDot, baseImage=img, threshold=threshold, returnArray=True)
            if len(positionDot) > 0 and self.checkCharacter(digits, '.') == False:
                digits.append({'digit': '.', 'x': positionDot[0][0]})

            templateComma = d['comma']
            positionComma = self.recognition.positions(
                target=templateComma, baseImage=img, threshold=threshold, returnArray=True)
            if len(positionComma) > 0 and self.checkCharacter(digits, ',') == False:
                digits.append({'digit': ',', 'x': positionComma[0][0]})

        def getX(e):
            return e['x']

        digits.sort(key=getX)
        r = list(map(lambda x: x['digit'], digits))
        return(''.join(r))

    def checkCharacter(self, array, digit):
        exist = False
        for value in array:
            if digit in value['digit']:
                exist = True
                break
        return exist
