#!/usr/bin/env python3

from birdprobe import BirdPROBE, __version__
import importlib
import json
from PIL import Image,ImageDraw,ImageFont
from threading import Event

class AbstractDisplay():
    def __init__(self, birdprobe, display_name, display_config):
        self.birdprobe = birdprobe
        self.detection_list = []
        self.detections = {}
        self.config = display_config

    def new_detection(self, msg):
        pass

    def location_update(self, msg):
        pass

    def update_display(self):
        pass

    def run(self):
        while True:
            Event().wait(timeout=5)
            self.update_display()


class AbstractGraphicDisplay(AbstractDisplay):
    def __init__(self, birdprobe, display_name, display_config, display_width, display_height):
        super().__init__(birdprobe, display_name, display_config)

        self.display_width = display_width
        self.display_height = display_height
        self.now_position = 0

        defaults = {
            'font_name_heading': 'OpenSans-Bold',
            'font_name_text': 'OpenSans-Regular',
            'font_name_footer': 'OpenSans-Light',
            'font_size_heading': '16',
            'font_size_text': '12',
            'font_size_footer': '8',
        }

        for key, val in defaults.items():
            if not key in self.config:
                self.config[key] = val

        try:
            self.font_heading = ImageFont.truetype(
                self.config['font_name_heading'],
                size=int(self.config['font_size_heading']))
        except OSError:
            self.font_heading = ImageFont.load_default()

        try:
            self.font_text = ImageFont.truetype(
                self.config['font_name_text'],
                size=int(self.config['font_size_text']))
        except OSError:
            self.font_text = ImageFont.load_default()

        try:
            self.font_footer = ImageFont.truetype(
                self.config['font_name_footer'],
                size=int(self.config['font_size_footer']))
        except OSError:
            self.font_footer = ImageFont.load_default()

        image = Image.new('1', (self.display_height, self.display_width), 255)
        draw = ImageDraw.Draw(image)
        draw.text(
            (int(self.display_height/2), int(self.display_width/2)),
            "BirdPROBE {}".format(__version__),
            font=self.font_heading,
            anchor='mm')
        self.draw_image(image)

    def update_display(self):
        image = Image.new('1', (self.display_height, self.display_width), 255)
        draw = ImageDraw.Draw(image)

        line_height = int(self.config['font_size_text']) + 2
        offset = line_height

        for detection in self.detection_list:
            draw.text(
                (2, offset),
                detection,
                font=self.font_text,
            )
            offset += line_height

        self.draw_image(image)

    def draw_image(self, image):
        pass


class Display(BirdPROBE):
    def init(self, argparser, configparser):
        argparser.add_argument('name', help='config file section name suffix to be used ([birdprobe.display.$name])')

    def start(self):
        display_config = self.configparser["{}.{}".format(self.component, self.args.name)]
        display_class = display_config.get('class')
        if not '.' in display_class:
            display_class = '{}.{}'.format(self.component, display_class)
        display = importlib.import_module(display_class)
        display.run(self, self.args.name, display_config)

    def mqtt_on_connect(self, client, userdata, flags, rc):
        client.message_callback_add(self.config['topic_detection'], display.new_detection)
        client.subscribe(self.config['topic_detection'])

        client.message_callback_add(self.config['topic_location'], display.location_update)
        client.subscribe(self.config['topic_location'])

def main():
    display = Display(__package__, 'location provider')
    display.start()

if __name__ == "__main__":
    main()
