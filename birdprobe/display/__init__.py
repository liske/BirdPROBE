#!/usr/bin/env python3

from birdprobe import BirdPROBE
import importlib
import json
from threading import Event

class AbstractDisplay():
    def __init__(self, birdprobe, display_name, display_config):
        self.birdprobe = birdprobe

    def run(self):
        Event().wait()

class Display(BirdPROBE):
    def init(self, parser):
        parser.add_argument('name', help='config file section name suffix to be used ([birdprobe.display.$name])')

    def start(self):
        display_config = self.configparser["{}.{}".format(self.component, self.args.name)]
        display_class = display_config.get('class')
        if not '.' in display_class:
            display_class = '{}.{}'.format(self.component, display_class)
        display = importlib.import_module(display_class)
        display.run(self, self.args.name, display_config)

def main():
    display = Display(__package__, 'location provider')
    display.start()

if __name__ == "__main__":
    main()
