from colorama import Fore
from cv2 import cv2

heroe_clicks = 0
last_log_is_progress = False
new_map_btn_img = cv2.imread('./targets/new-map.png')

COLOR = {
    'blue': Fore.BLUE,
    'default': Fore.WHITE,
    'grey': Fore.LIGHTBLACK_EX,
    'yellow': Fore.YELLOW,
    'black': Fore.BLACK,
    'cyan': Fore.CYAN,
    'green': Fore.GREEN,
    'magenta': Fore.MAGENTA,
    'white': Fore.WHITE,
    'red': Fore.RED
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
        console_message_colorfull = color_formatted + message + Fore.RESET
        service_message = "⏰{}\n{}".format(formatted_datetime, message)

        if self.config['app']['terminal_colorful'] is True:
            console_message = "{} - {}".format(
                formatted_datetime, console_message_colorfull)

        if emoji is not None and emoji is not False and self.config['app']['emoji'] is True:
            console_message = "{} - {} {}".format(
                formatted_datetime, emoji, message)
            service_message = "⏰{}\n{} {}".format(
                formatted_datetime, emoji, message)

            if self.config['app']['terminal_colorful'] is True:
                console_message = "{} - {} {}".format(
                    formatted_datetime, emoji, console_message_colorfull)

        print(console_message)

        if services == True:
            self.telegram.sendMessage(service_message)

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
