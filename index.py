from src.app import App
from src.log import Log
from src.multi_account import MultiAccount

from src.services.telegram import Telegram


banner = """\033[92m
******************************* BombCrypto Bot **********************************
*********************************************************************************
********************* Please consider buying me a coffee :) *********************
*********************************************************************************
************************************ BCOIN **************************************
****************** 0x4847C29561B6682154E25c334E12d156e19F613a *******************
*********************************************************************************
************************************* PIX ***************************************
********************* 08912d17-47a6-411e-b7ec-ef793203f836 **********************
*********************************************************************************

* Press CTRL + C to kill the bot.
* Some configs can be found in the /config/config.yaml file.

*********************************************************************************
\033[0m
"""

print(banner)

app = App()
log = Log()
multi_account = MultiAccount()
telegram = Telegram()


def main():
    app.start()
    telegram.start()
    multi_account.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log.console('Shutting down the bot', services=True, emoji='😓', color='red')
        telegram.stop()
        exit()
