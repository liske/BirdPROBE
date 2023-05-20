#!/usr/bin/env python3

from birdprobe import BirdPROBE
import importlib
import json
from threading import Event

class AbstractProvider():
    def __init__(self, birdprobe):
        self.birdprobe = birdprobe

    def publish(self, location=None):
        print(location)

    def run(self):
        self.publish()

        Event().wait()

class Location(BirdPROBE):
    def start_provider(self):
        provider_name = self.configparser[self.component].get('provider', 'none')
        if not '.' in provider_name:
            provider_name = '{}.{}'.format(self.component, provider_name)
        provider = importlib.import_module(provider_name)
        provider.run(self)

def main():
    location = Location(__package__, 'location provider')
    location.start_provider()

if __name__ == "__main__":
    main()
