import pyautogui
import requests
import yaml


class Application:
    def __init__(self):
        from src.config import Config
        self.config = Config().read()
        self.configThreshold = self.config['threshold']

    def importLibs(self):
        from src.log import Log
        self.log = Log()

    def start(self):
        pyautogui.PAUSE = self.config['time_intervals']['interval_between_movements']
        pyautogui.FAILSAFE = False

        self.checkUpdate()
        self.getVersions()

        input('Press Enter to start the bot...\n')
        self.log.console('Starting bot...', services=True,
                         emoji='🤖', color='green')

    def getVersions(self):
        self.importLibs()

        if self.config['app']['verify_version'] == True:
            githubVersion = self.githubVersion()
            localVersion = self.localVersion()

            banner = """
Versions
  Local
    App: {}
    Config File: {}
  GitHub
    App: {}
    Config File: {}
""".format(localVersion[0], localVersion[1], githubVersion[0], githubVersion[1])

            print(banner)

    def checkUpdate(self):

        githubVersion = self.githubVersion()
        localVersion = self.localVersion()

        versionGithubApp = githubVersion[0]
        versionGithubConfigFile = githubVersion[1]
        emergencyGithubApp = githubVersion[2]

        versionLocalApp = localVersion[0]
        versionLocalConfigFile = localVersion[1]

        if (emergencyGithubApp == 'true' and versionGithubApp > versionLocalApp):
            self.log.console(
                'Update is required for your security', services=True, emoji='🆘', color='red')

        if versionLocalApp is not None:
            if versionGithubApp > versionLocalApp:
                self.log.console('New app version ' + versionGithubApp +
                                 ' available, please update!', services=True, emoji='🎉', color='red'),
            if versionGithubConfigFile > versionLocalConfigFile:
                self.log.console('New config file version ' + versionGithubConfigFile +
                                 ' available, please update!', services=True, emoji='🎉', color='red'),
        else:
            self.log.console(
                'Version file not found, update is required', services=True, emoji='💥', color='red')

    def githubVersion(self):
        self.importLibs()
        data = requests.get(
            'https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/config/version.yaml')
        try:
            streamVersionGithub = yaml.safe_load(data.text)
            version = streamVersionGithub['version']
            app = version['app']
            config_file = version['config_file']
            emergency = version['emergency']
        except KeyError:
            self.log.console(
                'Version file not found in github', emoji='💥', color='red')
            app = "0.0.0"
            config_file = "0.0.0"
            emergency = False

        return [app, config_file, emergency]

    def localVersion(self):
        try:
            fileVersion = open("./config/version.yaml", 'r')
            streamVersion = yaml.safe_load(fileVersion)
            version = streamVersion['version']
            app = version['app']
            config_file = version['config_file']
            emergency = version['emergency']
            fileVersion.close()
        except FileNotFoundError:
            self.log.console(
                'Version file not found in local', emoji='💥', color='red')
            app = "0.0.0"
            config_file = "0.0.0"
            emergency = False

        return [app, config_file, emergency]

    def checkThreshold(self):
        from src.config import Config
        config = Config().read()
        newConfigThreshold = config['threshold']

        if newConfigThreshold != self.configThreshold:
            self.configThreshold = newConfigThreshold
            self.log.console('New Threshold applied', emoji='⚙️', color='grey')
