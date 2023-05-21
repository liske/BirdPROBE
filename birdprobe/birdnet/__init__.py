#!/usr/bin/env python3

from birdnetlib.main import SAMPLE_RATE
from birdprobe import BirdPROBE
from birdprobe.birdnet.recording import LiveRecording
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

    def detection(self, detections):
        for detection in detections:
            labels = detection[0].split('_')
            data = {
                'label': labels[0],
                'label2': labels[1],
                'conf': detection[1],
                'time': datetime.now().isoformat(),
            }
            msg = json.dumps(data, cls=NumpyEncoder)

            self.config['birdnet_label'] = labels[0]
            self.config['birdnet_label2'] = labels[1]
            print(msg)
            self.mqtt_client.publish(self.config['topic_detection'], msg)

    def main(self):
        pa = pyaudio.PyAudio()
        lr = LiveRecording(
            pa=pa, 
            callback=self.detection,
            sample_rate=self.configparser[self.component].getint('sample_rate'),
            sensitivity=self.configparser[self.component].getfloat('sensitivity'),
            min_conf=self.configparser[self.component].getfloat('min_conf'))
        lr.start_recording()

        while True:
            Event().wait()


def main():
    birdnet = Birdnet(__package__, 'vocal detector based on birdnetlib')
    birdnet.start()

if __name__ == "__main__":
    main()
