from cv2 import cv2
from os import listdir

class Bcoins:

    def importLibs(self):
        from src.actions import Actions
        from src.desktop import Desktop
        from src.images import Images
        from src.recognition import Recognition
        self.desktop = Desktop()
        self.images = Images()
        self.recognition = Recognition()

    def bcoinsWaitForClaim(self):
        self.importLibs()
        self.getBackgroundText()

    def getBackgroundText(self):
        screenshot = self.desktop.printScreen()
        your_bcoins = self.images.image('your_chest_bcoin')
        positions = self.recognition.positions(your_bcoins, baseImage=screenshot)
        if positions is False:
            return False
        x, y, w, h = positions[0]
        x = x - 30
        y = y + 130
        w = w + 60
        h = h - 85
        cropped = screenshot[y: y + h, x: x + w]
        digits = self.getDigits(cropped, gray=False)
        print(digits)

    def load_images(self, dir_name):
        file_names = listdir(dir_name)
        targets = {}
        for file in file_names:
            path = dir_name + file
            targets[file.replace('.png', '')] = cv2.imread(path)
        return targets

    def getDigits(self, img, gray=True, threshold=0.91):
        d = self.load_images('./images/themes/default/your_chest/')
        digits = []
        for i in range(10):
            if gray:
                template = cv2.cvtColor(d[str(i)], cv2.COLOR_BGR2GRAY)
            else:
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