import requests
import yaml

class App:
    def __init__(self):
        from src.config import Config
        self.config = Config().read()
        self.configThreshold = self.config['threshold']

    def importLibs(self):
        from src.log import Log        
        self.log = Log()        

    def getVersions(self):
        self.importLibs()

        if self.config['app']['verify_version'] == True:
            githubVersion = self.githubVersion()
            localVersion = self.localVersion()

            banner = """Versions
  Local
    App: {}
    Config File: {}
  GitHub
    App: {}
    Config File: {}
""".format(githubVersion[0], githubVersion[1], localVersion[0], localVersion[1])

            print(banner)

    def checkUpdate(self):

        githubVersion = self.githubVersion()
        localVersion = self.localVersion()

        versionGithubApp = githubVersion[0]
        emergencyGithubApp = githubVersion[2]

        versionLocalApp = localVersion[0]

        # Allow BCBOT to be stopped remotely in case of emergency
        if (emergencyGithubApp == 'true' and versionGithubApp > versionLocalApp):
            self.log.console('Update is required for your security', services=True, emoji='🆘')

        if versionLocalApp is not None:
            if versionGithubApp > versionLocalApp:
                self.log.console('New version ' + versionGithubApp + ' available, please update!', services=True, emoji='🎉'),
        else:
            self.log.console('Version file not found, update is required', services=True, emoji='💥')

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
                'Version file not found in github', emoji='💥')
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
                'Version file not found in local', emoji='💥')
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
            self.log.console('New Threshold applied', telegram=False, emoji='⚙️')
