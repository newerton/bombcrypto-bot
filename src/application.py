from colorama import Fore
from deepdiff import DeepDiff

import requests
import yaml

class Application:
    def __init__(self):
        from src.config import Config
        from src.services.telegram import Telegram
        self.config = Config().read()
        self.configThreshold = self.config['threshold']
        self.telegram = Telegram()

    def importLibs(self):
        from src.log import Log
        self.log = Log()

    def start(self):
        self.compareYamlConfig()
        self.checkUpdate()
        self.getVersions()

        input('Press Enter to start the bot...\n')
        self.log.console('Starting bot...', services=True,
                         emoji='🤖', color='green')

    def stop(self):
        self.telegram.stop()
        exit()

    def getVersions(self):
        self.importLibs()

        if self.config['app']['verify_version'] == True:
            gitHubVersion = self.gitHubVersion()
            localVersion = self.localVersion()

            banner = """
Versions
  Local
    App: {}
    Config File: {}
  GitHub
    App: {}
    Config File: {}
""".format(localVersion[0], localVersion[1], gitHubVersion[0], gitHubVersion[1])

            print(banner)

    def checkUpdate(self):

        gitHubVersion = self.gitHubVersion()
        localVersion = self.localVersion()

        versionGithubApp = gitHubVersion[0]
        versionGithubConfigFile = gitHubVersion[1]
        emergencyGithubApp = gitHubVersion[2]

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

    def gitHubVersion(self):
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
                'Version file not found in GitHub', emoji='💥', color='red')
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

    def compareYamlConfig(self):
        from src.config import Config
        configGitHubExample = Config().readGitHubExample()
        diff = DeepDiff(self.config, configGitHubExample)
        if len(diff) > 0 and 'dictionary_item_added' in diff:
            print('File that needs updating: ./config/config.yaml\n')
            try:
                if len(diff['dictionary_item_added']) > 0:
                    print(Fore.RED + '***************************' + Fore.RESET)
                    print(Fore.RED + '***** UPDATE REQUIRED *****' + Fore.RESET)
                    print(Fore.RED + '***************************' + Fore.RESET)
                    print('Key added:')
                    for added in diff['dictionary_item_added']:
                        key = added.replace("root", "")
                        print(Fore.GREEN + key + Fore.RESET)
                if len(diff['dictionary_item_removed']) > 0:
                    print(Fore.LIGHTBLACK_EX + '\n\n***************************' + Fore.RESET)
                    print(Fore.LIGHTBLACK_EX + '***** UPDATE OPTIONAL *****' + Fore.RESET)
                    print(Fore.LIGHTBLACK_EX + '***************************' + Fore.RESET)
                    print('Key removed:')
                    for removed in diff['dictionary_item_removed']:
                        key = removed.replace("root", "")
                        print(Fore.GREEN + key + Fore.RESET)

                print(Fore.WHITE + '\nSee: https://github.com/newerton/bombcrypto-bot/blob/main/config/EXAMPLE-config.yaml' + Fore.RESET)    
                print(Fore.GREEN + '\n*********************************************************************************' + Fore.RESET)

                if len(diff['dictionary_item_added']) > 0:
                    exit()
            except KeyError:
                print('Erro in validation configs')
                exit()
