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
    def init(self, argparser, configparser):
        configparser[self.component] = {
            'provider': 'none',
        }

    def main(self):
        provider_name = self.config.get('provider')
        if not '.' in provider_name:
            provider_name = '{}.{}'.format(self.component, provider_name)
        provider = importlib.import_module(provider_name)
        provider.run(self)

def location_decode(message):
    try:
        location = json.loads(message.payload)
    except json.JSONDecodeError:
        return None

    if location is not None:
        for key in ['lat', 'lon']:
            if not key in location or not isinstance(location[key], float):
                return None

    return location

def main():
    location = Location(__package__, 'location provider')
    location.start()

if __name__ == "__main__":
    main()
