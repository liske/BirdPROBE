#!/usr/bin/env python3

import numpy as np
import pyaudio
import time
import librosa
from birdnetlib.main import SAMPLE_RATE
from birdprobe.birdnet.recording import LiveRecording
from birdprobe.birdnet.analyzer import LiveAnalyzer

def main():
    pa = pyaudio.PyAudio()
    lr = LiveRecording(pa=pa, analyzer=LiveAnalyzer())
    lr.start_recording()

    while True:
        time.sleep(2.0)

if __name__ == "__main__":
    main()
