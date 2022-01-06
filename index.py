from src.actions import Actions
from src.app import App
from src.auth import Auth
from src.captcha import Captcha
from src.config import Config
from src.error import Errors
from src.heroes import Heroes
from src.images import Images
from src.recognition import Recognition
from src.log import Log

from src.services.telegram import Telegram

import pyautogui
import time
import sys

banner = """
******************************* BombCrypto Bot **********************************
*********************************************************************************
********************* Please consider buying me a coffee :) *********************
*********************************************************************************
******************************** Cryptocurrency *********************************
****************** 0x4847C29561B6682154E25c334E12d156e19F613a *******************
*********************************************************************************
************************************* PIX ***************************************
********************* 08912d17-47a6-411e-b7ec-ef793203f836 **********************
*********************************************************************************

* Press CTRL + C to kill the bot.
* Some configs can be found in the /config/config.yaml file.

=================================================================================
"""

print(banner)

config = Config().read()
streamConfig = config
configTimeIntervals = streamConfig['time_intervals']

pyautogui.PAUSE = streamConfig['time_intervals']['interval_between_movements']
pyautogui.FAILSAFE = False
check_for_updates = 60

next_refresh_heroes = configTimeIntervals['send_heroes_for_work'][0]
next_refresh_heroes_positions = configTimeIntervals['refresh_heroes_positions'][0]

actions = Actions()
app = App()
auth = Auth()
captcha = Captcha()
log = Log()
recognition = Recognition()
errors = Errors()
heroes = Heroes()
images = Images()
telegram = Telegram()


def main():

    app.checkUpdate()
    app.getVersions()

    input('Press Enter to start the bot...\n')
    log.console('Starting bot...', services=True, emoji='🤖')

    telegram.start()

    last = {
        "login": 0,
        "heroes": 0,
        "new_map": 0,
        "refresh_heroes": 0,
        "check_updates": 0
    }

    treasure_hunt_banner = images.image('treasure_hunt_banner')
    new_map_button = images.image('new_map_button')
    close_button = images.image('close_button')
    run_time_app = config['app']['run_time_app']

    while True:
        currentScreen = recognition.currentScreen()

        if currentScreen == "login":
            auth.login()

        errors.verify()

        captcha.check()

        now = time.time()

        if now - last["heroes"] > next_refresh_heroes * 60:
            last["heroes"] = now
            last["refresh_heroes"] = now
            heroes.getMoreHeroes()

        if currentScreen == "main":
            if actions.clickButton(treasure_hunt_banner):
                log.console('Entering treasure hunt', emoji='▶️')
                last["refresh_heroes"] = now

        if currentScreen == "treasure_hunt":
            if actions.clickButton(new_map_button):
                last["new_map"] = now
                actions.clickNewMap()

        if currentScreen == "character":
            actions.clickButton(close_button)
            actions.sleep(1, 2)

        if now - last["refresh_heroes"] > next_refresh_heroes_positions * 60:
            last["refresh_heroes"] = now
            heroes.refreshHeroesPositions()

        if now - last["check_updates"] > check_for_updates * 60:
            last["check_updates"] = now
            app.checkUpdate()

        auth.checkLogout()
        sys.stdout.flush()
        actions.sleep(run_time_app, run_time_app, randomMouseMovement=False)
        app.checkThreshold()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log.console('Shutting down the bot', services=True, emoji='😓')
        telegram.stop()
        exit()
