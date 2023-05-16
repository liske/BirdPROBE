#!/usr/bin/env python3

import pyaudio
import time
from birdprobe.birdnet.recording import LiveRecording

def main():
    pa = pyaudio.PyAudio()
    lr = LiveRecording(pa=pa)
    lr.start_recording()

    while True:
        time.sleep(2.0)

if __name__ == "__main__":
    main()
