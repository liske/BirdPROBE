import epaper
import time
from birdprobe.display import AbstractDisplay

class WaveshareEPD(AbstractDisplay):
    def __init__(self, birdprobe, display_name, display_config):
        super().__init__(birdprobe, display_name, display_config)

        self.epd = epaper.epaper('epd2in7').EPD()
        self.epd.init()
        self.epd.Clear(0)
        time.sleep(2)
        self.epd.Clear(0xFF)
        time.sleep(1)
        self.epd.sleep()

def run(birdprobe, display_name, display_config):
    display = WaveshareEPD(birdprobe, display_name, display_config)
    display.run()
