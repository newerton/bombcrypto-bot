from cv2 import cv2
from pyclick import HumanClicker
from os import listdir
from random import randint

import time
import pyautogui
import threading

humanClicker = HumanClicker()

class RevealNumbersCaptcha():
    def __init__(self):
        from src.desktop import Desktop
        from src.recognition import Recognition
        self.desktop = Desktop()
        self.recognition = Recognition()

    def remove_suffix(self, input_string, suffix):
        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return input_string

    def load_images(self, dir_name):
        file_names = listdir(dir_name)
        targets = {}
        for file in file_names:
            path = dir_name + file
            targets[self.remove_suffix(file, '.png')] = cv2.imread(path)

        return targets

    def getDigits(self, d, img, gray=True, threshold=0.88):
        digits = []
        for i in range(10):
            if gray:
                template = cv2.cvtColor(d[str(i)], cv2.COLOR_BGR2GRAY)
            else:
                template = d[str(i)]

            p = self.recognition.positions(template,img=img,threshold=threshold)
            if len (p) > 0:
                digits.append({'digit':str(i),'x':p[0][0]})

        def getX(e):
            return e['x']

        digits.sort(key=getX)
        r = list(map(lambda x : x['digit'],digits))
        return(''.join(r))

    def captchaImg(self, img, pos,w = 520, h = 180):
        rx, ry, _, _ = pos

        x_offset = -10
        y_offset = 140

        y = ry + y_offset
        x = rx + x_offset
        cropped = img[ y : y + h , x: x + w]
        return cropped

    def smallDigitsImg(self, img, pos, w = 200, h = 70):
        rx, ry, _, _ = pos

        x_offset = 150
        y_offset = 80

        y = ry + y_offset
        x = rx + x_offset
        cropped = img[ y : y + h , x: x + w]
        return cropped

    def getSliderPositions(self, screenshot, popup_pos):
        slider = self.recognition.position(d['slider'], img=screenshot, threshold=0.8)
        if slider is None:
            print('Error: Position start slider not found, verify target image or threshold')
            print('Erro: Posição inicial do slider não encontrado, verifique a imagem ou o threshold')
            return None
        (start_x, start_y) = slider

        humanClicker.move((int(start_x), int(start_y)), 1)
        pyautogui.mouseDown()
        humanClicker.move((int(start_x+400), int(start_y)), 1)

        screenshot = self.desktop.printSreen()

        end = self.recognition.position(d['slider'], img=screenshot, threshold = 0.8)
        if end is None:
            print('Error: Position end slider not found, verify target image or threshold')
            print('Erro: Posição final do slider não encontrado, verifique a imagem ou o threshold')
            return None        
        (end_x, end_y) = end

        size = end_x-start_x
        increment = size/6

        positions = []
        for i in range(7):
            positions.append((start_x+increment*i ,start_y+randint(0,10)))
        return positions

    def r(self):
        return randint(0,5)

    def moveToReveal(self, popup_pos):
        x,y,_,_ = popup_pos
        t = 2.5
        offset_x = 20
        offset_y = 140
        w = 453
        h = 160
        passes = 26
        increment_x = w/passes
        increment_y = h/passes
        start_x = x + offset_x
        start_y = y + offset_y

        humanClicker.move((int(start_x), int(start_y)), t)
        humanClicker.move((int(start_x), int(start_y + h)), t)
        humanClicker.move((int(start_x + (w / 2)), int(start_y + h)), t)
        humanClicker.move((int(start_x + w), int(start_y + h)), t)
        humanClicker.move((int(start_x + w), int(start_y)), t)
        humanClicker.move((int(start_x + (w / 2)), int(start_y)), t)
        humanClicker.move((int(start_x), int(start_y)), t)

        for i in range(passes):
            x = start_x + i * increment_x
            y = start_y + h * (i % 2)
            humanClicker.move((int(x), int(y)), t)

        humanClicker.move((int(start_x + w), int(start_y + h)), t)
        humanClicker.move((int(start_x + w), int(start_y)), t)

        time.sleep(1)

    def lookAtCaptcha(self):
        d = self.load_images( './captchas/reveal_numbers/images/')
        screenshot = self.desktop.printSreen()
        popup_pos = self.recognition.positions(d['robot'],img=screenshot)
        img = self.captchaImg(screenshot, popup_pos[0])
        return img

    def preProcess(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,img = cv2.threshold(img,170,240,cv2.THRESH_BINARY_INV)
        return img

    def add(self, img0, img1):
        return cv2.bitwise_and(img0, img1, mask = None)

    def getDiff(self, data):
        try:
            if data[0] is None:
                img0 = self.preProcess(self.lookAtCaptcha())
                img1 = self.preProcess(self.lookAtCaptcha())
                data[0] = self.add(img0,img1)
            while data[1]:
                now = self.preProcess(self.lookAtCaptcha())
                data[0] = self.add(data[0],now)
        except IndexError:
            return
        return

    def watchDiffs(self, data):
        thread = threading.Thread(target=self.getDiff, args =(data,))
        thread.start()
        return thread

    def getBackgroundText(self):
        d = self.load_images( './captchas/reveal_numbers/images/')
        screenshot = self.desktop.printSreen()
        popup_pos = self.recognition.positions(d['robot'],img=screenshot)
        data = [None,True]
        thread = self.watchDiffs(data)
        self.moveToReveal(popup_pos[0])
        data[1]=False
        thread.join()

        digits = self.getDigits(d, data[0])
        return digits

    def getSmallDigits(self, img):
        s = self.load_images( './captchas/reveal_numbers/small-digits/')
        digits = self.getDigits(s, img, gray=False, threshold=0.92)
        return digits

    def solveCaptcha(self):
        d = self.load_images( './captchas/reveal_numbers/images/')
        screenshot = self.desktop.printSreen()
        img = screenshot.copy()
        popup_pos = self.recognition.positions(d['robot'],img=img)
        if len(popup_pos) == 0:
            print('No captcha popup found!')
            return
        img = self.captchaImg(img, popup_pos[0])
        background_digits = self.getBackgroundText()
        # print('background = {}'.format(background_digits))
        slider_positions = self.getSliderPositions(screenshot, popup_pos)

        if slider_positions is None:
            return

        for position in slider_positions:
            x, y = position
            # pyautogui.moveTo(x,y,1)
            humanClicker.move((int(x), int(y)), 1)
            time.sleep(2)
            screenshot = self.desktop.printSreen()
            popup_pos = self.recognition.positions(d['robot'], img=screenshot)
            captcha_img = self.smallDigitsImg(screenshot, popup_pos[0])
            small_digits = self.getSmallDigits(captcha_img)
            # print( 'dig: {}, background_digits: {}'.format(small_digits, background_digits))
            if small_digits == background_digits:
                print('FOUND!')
                pyautogui.mouseUp()
                return
        print('Not found... trying again!')
        pyautogui.mouseUp()
        time.sleep(4)
        self.solveCaptcha()
        return
