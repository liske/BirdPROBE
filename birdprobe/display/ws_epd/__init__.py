import atexit
import signal
import epaper
import time
from birdprobe.display import AbstractGraphicDisplay

class WaveshareEPD(AbstractGraphicDisplay):
    def __init__(self, birdprobe, display_name, display_config):
        self.epd = epaper.epaper('epd2in7').EPD()
        self.epd.init()
        self.epd.Clear(0xFF)
        self.epd.sleep()

        super().__init__(birdprobe, display_name, display_config, self.epd.width, self.epd.height)

    def draw_image(self, image):
        self.epd.init()
        self.epd.display(self.epd.getbuffer(image))
        self.epd.sleep()

    def clear_screen(self, *args):
        self.epd.init()
        self.epd.Clear(0xFF)
        self.epd.sleep()

def run(birdprobe, display_name, display_config):
    display = WaveshareEPD(birdprobe, display_name, display_config)
    atexit.register(display.clear_screen)
    signal.signal(signal.SIGTERM, display.clear_screen)
    display.run()
