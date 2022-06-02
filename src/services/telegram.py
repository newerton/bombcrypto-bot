from cv2 import cv2
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.bot import Bot, BotCommand

import telegram
import yaml

Commands = [
    BotCommand("chat_id", "Send chat id"),
    BotCommand("print", "Send printscreen"),
    BotCommand("map", "Send a printscreen of the map (disabled in multi account)"),
    BotCommand(
        "tokens", "Send a printscreen of your TOKENS (disabled in multi account temporarily)"),
    BotCommand(
        "workall", "Send all heroes to work (disabled in multi account temporarily)"),
    BotCommand(
        "restall", "Send all heroes to rest (disabled in multi account temporarily)"),
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
        from src.tokens import Tokens
        from src.config import Config
        from src.desktop import Desktop
        from src.game import Game
        from src.heroes import Heroes
        from src.images import Images
        from src.log import Log
        from src.recognition import Recognition
        self.actions = Actions()
        self.tokens = Tokens()
        self.config = Config().read()
        self.desktop = Desktop()
        self.game = Game()
        self.heroes = Heroes()
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

        def userHasPermission(self, update: Update):
            return True if f'{update.message.from_user.id}' in self.telegramConfig['chat_ids'] else False

        def sendPrint(update: Update, context: CallbackContext) -> None:
            if userHasPermission(self, update):
                self.commandSendPrint(update)

        def sendChatId(update: Update, context: CallbackContext) -> None:
            if userHasPermission(self, update):
                self.commandSendChatId(update)

        def sendMap(update: Update, context: CallbackContext) -> None:
            if userHasPermission(self, update):
                self.commandSendMap(update)

        def sendTokens(update: Update, context: CallbackContext) -> None:
            if userHasPermission(self, update):
                self.commandSendToken(update)

        def sendDonation(update: Update, context: CallbackContext) -> None:
            if userHasPermission(self, update):
                self.commandSendDonation(update)

        def sendAllHeroesToWork(update: Update, context: CallbackContext) -> None:
            if userHasPermission(self, update):
                self.commandAllHeroesToWork(update)

        def sendAllHeroesToRest(update: Update, context: CallbackContext) -> None:
            if userHasPermission(self, update):
                self.commandAllHeroesToRest(update)

        commands = [
            ['chat_id', sendChatId],
            ['print', sendPrint],
            ['map', sendMap],
            ['tokens', sendTokens],
            ['workall', sendAllHeroesToWork],
            ['restall', sendAllHeroesToRest],
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

    def sendMapReport(self, callMapMethods=True):
        self.importLibs()
        if self.enableTelegram == False:
            return
        if(len(self.telegramConfig['chat_ids']) <= 0 or self.telegramConfig['enable_map_report'] is False):
            return

        if callMapMethods == True:
            self.game.goToMap()
            self.game.generateMapImage()

        try:
            image = self.game.MAP_IMAGE
            for chat_id in self.telegramConfig['chat_ids']:
                self.TelegramBot.send_photo(
                    chat_id=chat_id, photo=open(image, 'rb'))
        except:
            self.log.console('Telegram offline', emoji='😿')

        self.log.console('Map image sent to Telegram',
                         services=False, emoji='📄')
        return True

    def sendTokenReport(self, callMapMethods=True):
        self.importLibs()
        if self.enableTelegram == False:
            return
        if(len(self.telegramConfig['chat_ids']) <= 0 or self.telegramConfig['enable_coin_report'] is False):
            return

        if callMapMethods == True:
            self.tokens.openYourChestWindow()

        try:
            image = self.tokens.TOKENS_BOX_IMAGE
            for chat_id in self.telegramConfig['chat_ids']:
                self.TelegramBot.send_photo(
                    chat_id=chat_id, photo=open(image, 'rb'))
        except:
            self.log.console('Telegram offline', emoji='😿')

        self.log.console('Tokens image sent to Telegram',
                         services=False, emoji='📄')
        return True

    def sendMessage(self, message):
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

    def sendPrint(self):
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
        self.importLibs()
        if self.enableTelegram == False:
            return
        try:
            update.message.reply_text('🔃 Proccessing printscreen...')
            screenshot = self.desktop.printScreen()
            image = './logs/print-report.{}'.format(
                self.telegramConfig['format_of_image'])
            cv2.imwrite(image, screenshot)
            update.message.reply_photo(photo=open(image, 'rb'))
        except:
            self.log.console(
                'Error to send telegram print', emoji='📄')

    def commandSendChatId(self, update):
        update.message.reply_text(f'🆔 Your id is: {update.effective_user.id}')

    def commandSendMap(self, update):
        update.message.reply_text('🔃 Proccessing image map...')
        if self.config['app']['multi_account']['enable'] is not True:
            if self.sendMapReport() is None:
                update.message.reply_text('😿 An error has occurred')
        else:
            update.message.reply_text(
                '⚠️ Command disabled, because of the Multi Accounts is enabled.')

    def commandSendToken(self, update):
        update.message.reply_text('🔃 Proccessing image tokens...')
        if self.config['app']['multi_account']['enable'] is not True:
            if self.sendTokenReport() is None:
                update.message.reply_text('😿 An error has occurred')
        else:
            update.message.reply_text(
                '⚠️ Command disabled, because of the Multi Accounts is enabled.')

    def commandAllHeroesToWork(self, update):
        if self.config['app']['multi_account']['enable'] is not True:
            self.heroes.getMoreHeroes('workall')
        else:
            update.message.reply_text(
                '⚠️ Command disabled, because of the Multi Accounts is enabled.')

    def commandAllHeroesToRest(self, update):
        if self.config['app']['multi_account']['enable'] is not True:
            self.heroes.getMoreHeroes('restall')
        else:
            update.message.reply_text(
                '⚠️ Command disabled, because of the Multi Accounts is enabled.')

    def commandSendDonation(self, update):
        update.message.reply_text(
            '🎁 Smart Chain Wallet: \n\n 0x4847C29561B6682154E25c334E12d156e19F613a \n\n Thank You! 😀')
        update.message.reply_text(
            '🎁 Chave PIX: \n\n 08912d17-47a6-411e-b7ec-ef793203f836 \n\n Muito obrigado! 😀')
