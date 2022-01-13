from cv2 import cv2
from os import listdir


class Bcoins:

    def importLibs(self):
        from src.date import Date
        from src.desktop import Desktop
        from src.images import Images
        from src.recognition import Recognition
        from src.report import Report
        self.date = Date()
        self.desktop = Desktop()
        self.images = Images()
        self.recognition = Recognition()
        self.report = Report()

    def bcoinsWaitForClaim(self):
        self.importLibs()
        self.getBcoins()

    def getBcoins(self):
        self.importLibs()
        screenshot = self.desktop.printScreen()
        your_bcoins = self.images.image('your_chest_bcoin')
        positions = self.recognition.positions(
            your_bcoins, baseImage=screenshot)
        if positions is False:
            return False
        x, y, w, h = positions[0]
        x = x - 30
        y = y + 130
        w = w + 60
        h = h - 85
        cropped = screenshot[y: y + h, x: x + w]
        digits = self.getDigits(cropped)

        headers = ['date', 'bcoins']
        content = [self.date.dateFormatted(), digits.replace('.', ',')]
        self.report.writeCsv('bcoins-report', headers, content)
        return digits

    def loadImages(self, dir):
        file_names = listdir(dir)
        targets = {}
        for file in file_names:
            path = dir + file
            targets[file.replace('.png', '')] = cv2.imread(path)
        return targets

    def getDigits(self, img, threshold=0.95):
        d = self.loadImages('./images/themes/default/your_chest/')
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

            result = [a for a in digits if a['digit'] not in digits]
            if len(positionDot) > 0 and len(result) == 0:
                digits.append({'digit': '.', 'x': positionDot[0][0]})

        def getX(e):
            return e['x']

        digits.sort(key=getX)
        r = list(map(lambda x: x['digit'], digits))
        return(''.join(r))

