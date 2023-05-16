from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from birdnetlib.main import SAMPLE_RATE
import queue
from threading import Thread
import numpy as np
import operator
import pyaudio
import librosa

class LiveRecording(Recording):
    def __init__(self, pa, sensitivity=1.0, min_conf=0.1):
        super().__init__(Analyzer(), '/', sensitivity=1.0, min_conf=0.1)

        self.pyaudio = pa
        self.stream = None
        self.frames_per_buffer = librosa.frames_to_samples(librosa.time_to_frames(3, sr=SAMPLE_RATE))
        self.chunk_queue = queue.Queue(5)
        self.samples_worker = None

    def sample_worker(self):
        while True:
            chunk = self.chunk_queue.get()

            pred = self.analyzer.predict(chunk)[0]

            # Assign scores to labels
            p_labels = dict(zip(self.analyzer.labels, pred))

            # Sort by score
            p_sorted = sorted(
                p_labels.items(), key=operator.itemgetter(1), reverse=True
            )

            print([x for x in p_sorted if x[1] > self.minimum_confidence])

            self.chunk_queue.task_done()

    def start_recording(self, input_device_index=None):
        self.stop_recording()

        self.samples_worker = Thread(target=self.sample_worker, daemon=True).start()

        if input_device_index is None:
            input_device_info = self.pyaudio.get_default_input_device_info()
        else:
            input_device_info = self.pyaudio.get_device_info_by_index(input_device_index)

        print("Using input device '{}'.".format(input_device_info.get('name')))

        self.stream = self.pyaudio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            input_device_index=input_device_index,
            output=False,
            stream_callback=self.read_audio_callback,
            frames_per_buffer=self.frames_per_buffer
        )

    def stop_recording(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        with self.chunk_queue.mutex:
            self.chunk_queue.queue.clear()
        if self.samples_worker:
            self.samples_worker.stop()
            self.samples_worker = None

    def read_audio_callback(self, in_data, frame_count, time_info, flag):
        chunk = np.frombuffer(in_data, dtype=np.float32)

        try:
            self.chunk_queue.put_nowait(chunk)
        except queue.Full:
            print("analyze queue overrun :-(")

        return None, pyaudio.paContinue
