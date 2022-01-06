from cv2 import cv2
from pyclick import HumanClicker

import pyautogui
import numpy as np
from os import listdir
import torch
from random import randint

model = torch.hub.load('./captchas/crazy_numbers', 'custom',
                       "captchas/crazy_numbers/bomb_captcha.pt", source='local')

humanClicker = HumanClicker()

class CrazyNumbersCaptcha():

    def __init__(self):
        from src.desktop import Desktop
        from src.recognition import Recognition
        self.desktop = Desktop()
        self.recognition = Recognition()

    def getBackgroundText(self, img, percent_required):
        if type(img) == np.ndarray and percent_required:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = model(img, size=416)
            digits = []

            if results.xyxy[0].shape[0] >= 1:
                for box in results.xyxy[0]:
                    x1, _, _, _, percent, digit = box
                    if percent >= percent_required:
                        digits.append({'x': x1.item(), 'd': digit.item()})

                def getX(e):
                    return e['x']
                digits.sort(key=getX)

                def getD(e):
                    return str(int(e['d']))

                return ''.join(list(map(getD, digits)))

    def remove_suffix(self, input_string, suffix):
        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return input_string

    def load_images(self):
        dir_name = './captchas/crazy_numbers/images/'
        file_names = listdir(dir_name)
        targets = {}
        for file in file_names:
            path = dir_name + file
            targets[self.remove_suffix(file, '.png')] = cv2.imread(path)

        return targets

    def getDigits(self, d, img):
        digits = []
        for i in range(10):
            p = self.recognition.positions(d[str(i)], baseImage=img, threshold=0.95)
            if len(p) > 0:
                digits.append({'digit': str(i), 'x': p[0][0]})

        def getX(e):
            return e['x']

        digits.sort(key=getX)
        r = list(map(lambda x: x['digit'], digits))
        return(''.join(r))

    def captchaImg(self, img, pos, w=500, h=180):
        rx, ry, _, _ = pos

        x_offset = -10
        y_offset = 89

        y = ry + y_offset
        x = rx + x_offset
        cropped = img[y: y + h, x: x + w]
        return cropped

    def getSliderPositions(self, screenshot, popup_pos):
        d = self.load_images()
        slider = self.recognition.position(d['slider'], baseImage=screenshot)

        if slider is None:
            print('no slider')
            return None
        (start_x, start_y) = slider

        humanClicker.move((start_x, start_y+randint(0, 10)), 1)
        pyautogui.mouseDown()
        humanClicker.move((start_x+400, start_y+randint(0, 10)), 1)

        screenshot = self.desktop.printSreen()

        end = self.recognition.position(d['slider'], baseImage=screenshot, threshold=0.8)
        (end_x, end_y) = end

        size = end_x-start_x

        increment = size/4

        positions = []
        for i in range(5):
            positions.append((start_x+increment*i, start_y+randint(0, 10)))
        return positions

    def solveCaptcha(self):
        d = self.load_images()
        screenshot = self.desktop.printScreen()
        img = screenshot.copy()
        popup_pos = self.recognition.positions(d['robot'], baseImage=img)
        if popup_pos == False:
            return
            
        if len(popup_pos) == 0:
            print('no captcha popup found!')
            return
        img = self.captchaImg(img, popup_pos[0])
        digits = self.getDigits(d, img)
        slider_positions = self.getSliderPositions(screenshot, popup_pos)

        if slider_positions is None:
            return

        for position in slider_positions:
            x, y = position
            humanClicker.move((x, y), 1)
            screenshot = self.desktop.printSreen()
            popup_pos = self.recognition.positions(d['robot'], baseImage=screenshot)
            captcha_img = self.captchaImg(screenshot, popup_pos[0])
            background_digits = self.getBackgroundText(captcha_img,  0.7)
            # print( 'dig: {}, background_digits: {}'.format(digits, background_digits))
            if digits == background_digits:
                print('FOUND!')
                pyautogui.mouseUp()
                return
        print('not found... trying again!')
        pyautogui.mouseUp()
        self.solveCaptcha()
        return
