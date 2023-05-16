#!/usr/bin/env python3

import pyaudio
import time
from birdprobe import birdprobe_argparser, birdprobe_load_config
from birdprobe.birdnet.recording import LiveRecording


def main():
    parser = birdprobe_argparser(__package__, 'BirdPROBE: vocal detector based on birdnetlib')
    args = parser.parse_args()

    config = birdprobe_load_config(args.config, __package__)

    pa = pyaudio.PyAudio()
    lr = LiveRecording(pa=pa)
    lr.start_recording()

    while True:
        time.sleep(2.0)

if __name__ == "__main__":
    main()
