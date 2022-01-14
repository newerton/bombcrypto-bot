from cv2 import cv2
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.bot import Bot, BotCommand

import mss
import numpy as np
import telegram
import yaml

Commands = [
    BotCommand("chat_id", "Send chat id"),
    BotCommand("print", "Send printscreen"),
    BotCommand("map", "Send a printscreen of the map (disabled in multi account)"),
    BotCommand("bcoin", "Send a printscreen of your BCOIN"),
    BotCommand("donation", "Some wallets for donation")
]


class Telegram:
    def __init__(self):
        from src.config import Config
        self.config = Config().read()
        self.enableTelegram = self.config['services']['telegram']
        self.updater = None

        if self.enableTelegram == True:
            self.telegramConfig = self.telegramConfig()
            try:
                self.updater = Updater(self.telegramConfig['botfather_token'])
                self.TelegramBot = telegram.Bot(
                    token=self.telegramConfig['botfather_token'])
            except telegram.error.InvalidToken:
                self.updater = None
                if self.enableTelegram == True:
                    print('Telegram: BotFather Token invalid or Bot not initialized.')
                    exit()
                return

    def importLibs(self):
        from src.actions import Actions
        from src.bcoins import Bcoins
        from src.config import Config
        from src.desktop import Desktop
        from src.images import Images
        from src.log import Log
        from src.recognition import Recognition
        self.actions = Actions()
        self.bcoins = Bcoins()
        self.config = Config().read()
        self.desktop = Desktop()
        self.images = Images()
        self.log = Log()
        self.recognition = Recognition()

    def telegramConfig(self):
        try:
            file = open("./config/services/telegram.yaml",
                        'r', encoding='utf8')
        except FileNotFoundError:
            print('Info: Telegram not configure, rename EXAMPLE-telegram.yaml to telegram.yaml in /config/services/ folder')
            exit()

        with file as s:
            stream = s.read()
        return yaml.safe_load(stream)

    def start(self):
        self.importLibs()
        if self.enableTelegram == False:
            return

        self.log.console('Initializing Telegram...', emoji='📱')
        botFatherToken = self.telegramConfig['botfather_token']
        self.updater = Updater(botFatherToken)

        self.bot = Bot(botFatherToken)
        self.bot.set_my_commands(Commands, language_code='en')

        def sendPrint(update: Update, context: CallbackContext) -> None:
            self.commandSendPrint(update)

        def sendChatId(update: Update, context: CallbackContext) -> None:
            self.commandSendChatId(update)

        def sendMap(update: Update, context: CallbackContext) -> None:
            self.commandSendMap(update)

        def sendBcoin(update: Update, context: CallbackContext) -> None:
            self.commandSendBcoin(update)

        def sendDonation(update: Update, context: CallbackContext) -> None:
            self.commandSendDonation(update)

        commands = [
            ['chat_id', sendChatId],
            ['print', sendPrint],
            ['map', sendMap],
            ['bcoin', sendBcoin],
            ['donation', sendDonation],
        ]

        for command in commands:
            self.updater.dispatcher.add_handler(
                CommandHandler(command[0], command[1]))
        try:
            self.updater.start_polling()
        except:
            self.log.console(
                'Bot not initialized, see configuration file', emoji='🤖')

    def stop(self):
        if self.updater:
            self.updater.stop()

    def sendMapReport(self):
        self.importLibs()
        if self.enableTelegram == False:
            return
        if(len(self.telegramConfig['chat_ids']) <= 0 or self.telegramConfig['enable_map_report'] is False):
            return

        currentScreen = self.recognition.currentScreen()

        back_button = self.images.image('back_button')
        close_button = self.images.image('close_button')
        full_screen_button = self.images.image('full_screen_button')
        treasure_hunt_banner = self.images.image('treasure_hunt_banner')

        if currentScreen == "main":
            if self.actions.clickButton(treasure_hunt_banner):
                self.actions.sleep(2, 2)
        elif currentScreen == "character":
            if self.clickButton(close_button):
                self.actions.sleep(2, 2)
                if self.clickButton(treasure_hunt_banner):
                    self.actions.sleep(2, 2)
        elif currentScreen == "treasure_hunt":
            self.actions.sleep(2, 2)
        else:
            return

        back_btn = self.recognition.positions(back_button, returnArray=True)
        full_screen_btn = self.recognition.positions(
            full_screen_button, returnArray=True)

        if len(back_btn) <= 0 or len(full_screen_btn) <= 0:
            return
        x, y, _, _ = back_btn[0]
        x1, y1, w, _ = full_screen_btn[0]

        newY0 = y
        newY1 = y1
        newX0 = x
        newX1 = x1 + w

        image = './logs/map-report.%s' % self.telegramConfig['format_of_image']
        with mss.mss() as sct:
            monitorToUse = self.config['app']['monitor_to_use']
            monitor = sct.monitors[monitorToUse]
            sct_img = np.array(sct.grab(monitor))
            crop_img = sct_img[newY0:newY1, newX0:newX1]

            cv2.imwrite(image, crop_img)
            self.actions.sleep(1, 1)
            try:
                for chat_id in self.telegramConfig['chat_ids']:
                    self.TelegramBot.send_photo(
                        chat_id=chat_id, photo=open(image, 'rb'))
            except:
                self.log.console('Telegram offline', emoji='😿')

            try:
                self.sendPossibleAmountReport(sct_img[:, :, :3])
            except:
                self.log.console('Error finding chests',
                                 services=True, emoji='😿')

        self.actions.clickButton(close_button)
        self.log.console('Map report sent', services=True, emoji='📄')
        return True

    def sendPossibleAmountReport(self, baseImage=None):
        if self.enableTelegram == False:
            return
        if baseImage is None:
            baseImage = self.desktop.printScreen()

        totalChest = self.totalChestsByMap(baseImage)

        totalChest01 = totalChest['totalChest01']
        totalChest02 = totalChest['totalChest02']
        totalChest03 = totalChest['totalChest03']
        totalChest04 = totalChest['totalChest04']

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

🤑 Possible amount: {total:.3f} BCoin
"""
        self.log.console(report, services=True)

    def sendBCoinReport(self):
        self.importLibs()
        if self.enableTelegram == False:
            return
        if(len(self.telegramConfig['chat_ids']) <= 0 or self.telegramConfig['enable_coin_report'] is False):
            return

        try:
            image = self.bcoins.BCOIN_BOX_IMAGE
            for chat_id in self.telegramConfig['chat_ids']:
                self.TelegramBot.send_photo(chat_id=chat_id, photo=open(image, 'rb'))
        except:
            self.log.console('Telegram offline', emoji='😿')

        self.log.console('BCoin image sent to Telegram', services=False, emoji='📄')

        return True

    def totalChestsByMap(self, baseImage):
        threshold = self.config['threshold']['chest']

        chest_01_closed = self.images.image(
            'chest_01_closed', newPath='./images/themes/default/chests/')
        chest_02_closed = self.images.image(
            'chest_02_closed', newPath='./images/themes/default/chests/')
        chest_03_closed = self.images.image(
            'chest_03_closed', newPath='./images/themes/default/chests/')
        chest_04_closed = self.images.image(
            'chest_04_closed', newPath='./images/themes/default/chests/')

        c01 = len(self.recognition.positions(
            chest_01_closed, threshold, baseImage, returnArray=True))
        c02 = len(self.recognition.positions(
            chest_02_closed, threshold, baseImage, returnArray=True))
        c03 = len(self.recognition.positions(
            chest_03_closed, threshold, baseImage, returnArray=True))
        c04 = len(self.recognition.positions(
            chest_04_closed, threshold, baseImage, returnArray=True))

        chest_01_hit = self.images.image(
            'chest_01_hit', newPath='./images/themes/default/chests/')
        chest_02_hit = self.images.image(
            'chest_02_hit', newPath='./images/themes/default/chests/')
        chest_03_hit = self.images.image(
            'chest_03_hit', newPath='./images/themes/default/chests/')
        chest_04_hit = self.images.image(
            'chest_04_hit', newPath='./images/themes/default/chests/')

        c01_hit = len(self.recognition.positions(
            chest_01_hit, threshold, baseImage, returnArray=True))
        c02_hit = len(self.recognition.positions(
            chest_02_hit, threshold, baseImage, returnArray=True))
        c03_hit = len(self.recognition.positions(
            chest_03_hit, threshold, baseImage, returnArray=True))
        c04_hit = len(self.recognition.positions(
            chest_04_hit, threshold, baseImage, returnArray=True))

        totalChest01 = c01 + c01_hit
        totalChest02 = c02 + c02_hit
        totalChest03 = c03 + c03_hit
        totalChest04 = c04 + c04_hit

        return {
            'totalChest01': totalChest01,
            'totalChest02': totalChest02,
            'totalChest03': totalChest03,
            'totalChest04': totalChest04,
        }

    def sendTelegramMessage(self, message):
        self.importLibs()
        if self.enableTelegram == False:
            return

        try:
            if(len(self.telegramConfig['chat_ids']) > 0):
                for chat_id in self.telegramConfig['chat_ids']:
                    self.TelegramBot.send_message(
                        text=message, chat_id=chat_id)
        except:
            self.log.console(
                'Error to send telegram message. See configuration file', emoji='📄')
            return

    def sendTelegramPrint(self):
        self.importLibs()
        if self.enableTelegram == False:
            return
        try:
            image = './logs/print-report.%s' % self.telegramConfig['format_of_image']
            if(len(self.telegramConfig['chat_ids']) > 0):
                screenshot = self.desktop.printScreen()
                cv2.imwrite(image, screenshot)
                for chat_id in self.telegramConfig['chat_ids']:
                    self.TelegramBot.send_photo(
                        chat_id=chat_id, photo=open(image, 'rb'))
        except:
            self.log.console(
                'Error to send telegram print. See configuration file', emoji='📄')

    def commandSendPrint(self, update):
        update.message.reply_text('🔃 Proccessing...')
        screenshot = self.desktop.printScreen()
        image = './logs/print-report.{}'.format(
            self.telegramConfig['format_of_image'])
        cv2.imwrite(image, screenshot)
        update.message.reply_photo(photo=open(image, 'rb'))

    def commandSendChatId(self, update):
        update.message.reply_text('🆔 Your id is: {update.effective_user.id}')

    def commandSendMap(self, update):
        update.message.reply_text('🔃 Proccessing...')
        if self.config['app']['multi_account']['enable'] is not True:
            if self.sendMapReport() is None:
                update.message.reply_text('😿 An error has occurred')
        else:
            update.message.reply_text(
                '⚠️ Command disabled, because of the Multi Accounts is enabled.')

    def commandSendBcoin(self, update):
        update.message.reply_text('🔃 Proccessing...')
        if self.config['app']['multi_account']['enable'] is not True:
            if self.sendBCoinReport() is None:
                update.message.reply_text('😿 An error has occurred')
        else:
            update.message.reply_text(
                '⚠️ Command disabled, because of the Multi Accounts is enabled.')

    def commandSendDonation(self, update):
        update.message.reply_text(
            '🎁 Smart Chain Wallet: \n\n 0x4847C29561B6682154E25c334E12d156e19F613a \n\n Thank You! 😀')
        update.message.reply_text(
            '🎁 Chave PIX: \n\n 08912d17-47a6-411e-b7ec-ef793203f836 \n\n Muito obrigado! 😀')
