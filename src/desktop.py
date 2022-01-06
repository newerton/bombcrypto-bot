import numpy as np
import mss

class Desktop:
    def importLibs(self):
        from src.config import Config
        self.config = Config().read()

    def printScreen(self):
        self.importLibs()
        with mss.mss() as sct:
            monitorToUse = self.config['app']['monitor_to_use']
            monitor = sct.monitors[monitorToUse]
            sct_img = np.array(sct.grab(monitor))
            return sct_img[:, :, :3]
