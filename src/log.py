from cv2 import cv2

heroe_clicks = 0
last_log_is_progress = False
new_map_btn_img = cv2.imread('./targets/new-map.png')

COLOR = {
    'blue': '\033[94m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m'
}


class Log:
    def importLibs(self):
        from src.actions import Actions
        from src.config import Config
        from src.date import Date
        from src.services.telegram import Telegram
        self.actions = Actions()
        self.config = Config().read()
        self.date = Date()
        self.log = Log()
        self.telegram = Telegram()

    def console(self, message, services=False, emoji=False, color='default'):
        self.importLibs()
        color_formatted = COLOR.get(color.lower(), COLOR['default'])

        formatted_datetime = self.date.dateFormatted()
        console_message = "{} - {}".format(formatted_datetime, message)
        console_message_colorful  = console_message

        if self.config['app']['terminal_colorful'] is True:
            console_message_colorful  = color_formatted + console_message + '\033[0m'        

        if emoji is not None and self.config['app']['emoji'] is True:
            console_message = "{} - {} {}".format(
                formatted_datetime, emoji, message)

        print(console_message_colorful)

        if services == True:
            service_message = "⏰{}\n{} {}".format(formatted_datetime, emoji, message)
            self.telegram.sendTelegramMessage(service_message)

        if (self.config['log']['save_to_file'] == True):
            file = open("./logs/logger.log", "a", encoding='utf-8')
            file.write(console_message + '\n')
            file.close()
        return True

    def mapClicked(self):
        self.importLibs()
        if self.actions.clickButton(new_map_btn_img):
            self.console('🗺️ New Map button clicked!')
            file = open("./logs/new-map.log", "a", encoding='utf-8')
            file.write(self.date.dateFormatted() + '\n')
            file.close()
