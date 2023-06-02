#!/usr/bin/env python3

from birdnetlib.main import SAMPLE_RATE
from birdprobe import BirdPROBE
from birdprobe.birdnet.recording import LiveRecording
from birdprobe.location import location_decode
from datetime import datetime
import json
import numpy as np
import pyaudio
from threading import Event

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        else:
            return super(NumpyEncoder, self).default(obj)

class Birdnet(BirdPROBE):
    def init(self, argparser, configparser):
        configparser[self.component] = {
            'sample_rate': SAMPLE_RATE,
            'sensitivity': 1.0,
            'min_conf': 0.1,
        }
        self.lr = None
        self.location = None

    def detection(self, detections):
        for detection in detections:
            labels = detection[0].split('_')
            data = {
                'label': labels[0],
                'label2': self.labels_l18n.get(labels[0], labels[1]),
                'conf': detection[1],
                'loc': self.location,
                'time': datetime.now().isoformat(),
            }
            msg = json.dumps(data, cls=NumpyEncoder)

            self.config['birdnet_label'] = labels[0]
            self.config['birdnet_label2'] = labels[1]
            print(msg)
            self.mqtt_client.publish(self.config['topic_detection'], msg)

    def location_update(self,client, userdata, message):
        self.location = location_decode(message)

        if self.lr:
            self.lr.location_update(self.location)

    def mqtt_on_connect(self, client, userdata, flags, rc):
        client.message_callback_add(self.config['topic_location'], self.location_update)
        client.subscribe(self.config['topic_location'])

    def main(self):
        self.labels_l18n = {}
        labels_path = self.config.get('labels_path')
        if labels_path is not None:
            with open(labels_path, 'r') as fh:
                for line in fh:
                    label = line.strip().split('_')
                    self.labels_l18n[label[0]] = label[1]

        pa = pyaudio.PyAudio()
        self.lr = LiveRecording(
            pa=pa,
            callback=self.detection,
            location=self.location,
            sample_rate=self.configparser[self.component].getint('sample_rate'),
            sensitivity=self.configparser[self.component].getfloat('sensitivity'),
            min_conf=self.configparser[self.component].getfloat('min_conf'))
        self.lr.start_recording()

        while True:
            Event().wait()


def main():
    birdnet = Birdnet(__package__, 'vocal detector based on birdnetlib')
    birdnet.start()

if __name__ == "__main__":
    main()
