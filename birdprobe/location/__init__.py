#!/usr/bin/env python3

from birdprobe import BirdPROBE
import importlib
import json
from threading import Event

class AbstractProvider():
    def __init__(self, birdprobe):
        self.birdprobe = birdprobe
        self.location = None

    def publish(self):
        self.birdprobe.mqtt_client.publish(
            self.birdprobe.config['topic_location'],
            json.dumps(self.location),
            retain=True)
        print("Location: {}".format(self.location))

    def mqtt_on_connect(self, client, userdata, flags, rc):
        self.publish()

    def run(self):
        self.publish()

        Event().wait()

class Location(BirdPROBE):
    def main(self):
        provider_name = self.config.get('provider', 'none')
        if not '.' in provider_name:
            provider_name = '{}.{}'.format(self.component, provider_name)
        provider = importlib.import_module(provider_name)
        provider.run(self)

def main():
    location = Location(__package__, 'location provider')
    location.start()

if __name__ == "__main__":
    main()
