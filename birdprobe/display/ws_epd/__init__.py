import atexit
from birdprobe.display import AbstractGraphicDisplay
import epaper
from PIL import ImageChops
import signal
import time

class WaveshareEPD(AbstractGraphicDisplay):
    def __init__(self, birdprobe, display_name, display_config):
        module = display_config['module']
        print("display module: {}".format(module))
        self.epd = epaper.epaper(module).EPD()
        self.epd.init()
        self.epd.Clear(0xFF)
        self.epd.sleep()
        self.has_partial_updates = hasattr(self.epd, 'display_Partial') and callable(self.epd.display_Partial)
        self.last_image = None

        print("Display partial update support: {}".format(self.has_partial_updates))

        super().__init__(birdprobe, display_name, display_config, self.epd.width, self.epd.height)

    def draw_image(self, image):
        self.epd.init()

        full_refresh = True
        if self.last_image is not None:
            diff = ImageChops.difference(self.last_image, image)
            if diff is None:
                # skip update if last and current image are identical
                return

            if self.has_partial_updates:
                full_refresh = (diff[2] - diff[0]) > self.display_width / 2 and (diff[3] - diff[1]) > self.display_height / 2
                if not full_refresh:
                    self.epd.display_Partial(self.epd.getbuffer(image), *diff)

        self.last_image = image

        if full_refresh:
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
