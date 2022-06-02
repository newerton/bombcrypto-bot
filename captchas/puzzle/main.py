from cv2 import cv2
from pyclick import HumanClicker

import numpy as np
import pyautogui
import time

humanClicker = HumanClicker()

class PuzzleCaptcha:
    def __init__(self):
        from src.desktop import Desktop
        from src.images import Images
        from src.log import Log
        from src.recognition import Recognition
        self.desktop = Desktop()
        self.images = Images()
        self.log = Log()
        self.recognition = Recognition()

    def solveCaptcha(self):
        pieces_start_pos = self.getPiecesPosition()
        if pieces_start_pos is False:
            return
        slider_start_pos = self.getSliderPosition()
        if slider_start_pos is False:
            return

        x, y = slider_start_pos
        humanClicker.move((int(x), int(y)), np.random.randint(1, 2))
        pyautogui.mouseDown()
        humanClicker.move((int(x + 350), int(y)), np.random.randint(1, 2))
        pieces_end_pos = self.getPiecesPosition()
        if pieces_end_pos is False:
            return False

        piece_start, _, _, _ = self.getLeftPiece(pieces_start_pos)
        piece_end, _, _, _ = self.getRightPiece(pieces_end_pos)
        piece_middle, _, _, _ = self.getRightPiece(pieces_start_pos)
        slider_start, _, = slider_start_pos
        slider_end, _ = self.getSliderPosition()

        if piece_start is False or piece_end is False or piece_middle is False or slider_start is False or slider_end is False:
            return False

        piece_domain = piece_end - piece_start
        middle_piece_in_percent = (piece_middle - piece_start)/piece_domain

        slider_domain = slider_end - slider_start
        slider_awnser = slider_start + \
            (middle_piece_in_percent * slider_domain)

        humanClicker.move((int(slider_awnser), int(y)),
                          np.random.randint(1, 2))
        time.sleep(1)
        pyautogui.mouseUp()
        time.sleep(2)

        title_robot = self.images.image('title_robot')
        isCaptcha = self.recognition.positions(title_robot)
        if isCaptcha is not False:
            self.log.console('Captcha error', emoji='🧩')
            self.solveCaptcha()
        else:
            self.log.console('Captcha solved', emoji='🧩')

    def getPiecesPosition(self, t=150):
        title_robot = self.images.image('title_robot')
        piece = self.images.image('piece', path='./captchas/puzzle/images/')

        popup_pos = self.recognition.positions(title_robot)
        if popup_pos is False:
            self.log.console('Captcha not found', emoji='🧩')
            return
        rx, ry, _, _ = popup_pos[0]

        w = 380
        h = 200
        x_offset = -40
        y_offset = 65

        y = ry + y_offset
        x = rx + x_offset

        img = self.desktop.printScreen()

        cropped = img[y: y + h, x: x + w]
        blurred = cv2.GaussianBlur(cropped, (3, 3), 0)
        edges = cv2.Canny(blurred, threshold1=t/2,
                          threshold2=t, L2gradient=True)

        piece_img = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(edges, piece_img, cv2.TM_CCORR_NORMED)

        puzzle_pieces = self.findPuzzlePieces(result, piece_img)

        if puzzle_pieces is None:
            return False

        absolute_puzzle_pieces = []
        for i, puzzle_piece in enumerate(puzzle_pieces):
            px, py, pw, ph = puzzle_piece
            absolute_puzzle_pieces.append([x + px, y + py, pw, ph])

        absolute_puzzle_pieces = np.array(absolute_puzzle_pieces)
        return absolute_puzzle_pieces

    def findPuzzlePieces(self, result, piece_img, threshold=0.5):
        piece_w = piece_img.shape[1]
        piece_h = piece_img.shape[0]
        yloc, xloc = np.where(result >= threshold)

        r = []
        for (piece_x, piece_y) in zip(xloc, yloc):
            r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])
            r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])

        r, weights = cv2.groupRectangles(r, 1, 0.2)

        if len(r) < 2:
            return self.findPuzzlePieces(result, piece_img, threshold-0.01)

        if len(r) == 2:
            return r

        if len(r) > 2:
            # logger('🧩 Overshoot by %d attempts' % len(r))

            return r

    def getSliderPosition(self):
        slider = self.images.image('slider', path='./captchas/puzzle/images/')
        slider_pos = self.recognition.positions(slider)
        if slider_pos is False:
            return False
        x, y, w, h = slider_pos[0]
        position = [x+w/2, y+h/2]
        return position

    def getLeftPiece(self, puzzle_pieces):
        if puzzle_pieces is False:
            return False

        xs = [row[0] for row in puzzle_pieces]
        index_of_left_rectangle = xs.index(min(xs))

        left_piece = puzzle_pieces[index_of_left_rectangle]
        return left_piece

    def getRightPiece(self, puzzle_pieces):
        if puzzle_pieces is False:
            return False

        xs = [row[0] for row in puzzle_pieces]
        index_of_right_rectangle = xs.index(max(xs))

        right_piece = puzzle_pieces[index_of_right_rectangle]
        return right_piece
