from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from birdnetlib.utils import return_week_48_from_datetime
from datetime import datetime
import queue
from threading import Thread
import numpy as np
import operator
import pyaudio
import librosa

class LiveRecording(Recording):
    def __init__(self, pa, callback, location, sample_rate, overlap=1.0, sensitivity=1.0, min_conf=0.1, labels_path=None, mobel_path=None):
        analyzer = Analyzer(
            classifier_labels_path=labels_path,
            classifier_model_path=mobel_path)
        super().__init__(analyzer, '/', sensitivity=1.0, min_conf=0.1)

        self.pyaudio = pa
        self.callback = callback
        self.sample_rate = sample_rate
        self.stream = None
        self.frames_per_buffer = librosa.frames_to_samples(librosa.time_to_frames(3, sr=self.sample_rate))
        self.chunk_queue = queue.Queue(5)
        self.samples_worker = None
        self.location_update(location)
        self.overlap = int(overlap * sample_rate)
        self.chunk_tail = None

    def location_update(self, location):
        if location:
            self.lat = location['lat']
            self.lon = location['lon']

            self.analyzer.set_predicted_species_list_from_position(self)

    def sample_worker(self):
        while True:
            chunk = self.chunk_queue.get()

            self.week_48 = return_week_48_from_datetime(datetime.now())
            pred = self.analyzer.predict(chunk)[0]

            # Assign scores to labels
            p_labels = dict(zip(self.analyzer.labels, pred))

            # Filter for min_conf score
            p_filtered = [x for x in p_labels.items() if x[1] > self.minimum_confidence]

            # Sort by score
            p_sorted = sorted(
                p_filtered, key=operator.itemgetter(1), reverse=True
            )

            if p_sorted:
                self.callback(p_sorted)

            self.chunk_queue.task_done()

    def start_recording(self, input_device_index=None):
        self.stop_recording()

        self.samples_worker = Thread(target=self.sample_worker, daemon=True).start()

        if input_device_index is None:
            input_device_info = self.pyaudio.get_default_input_device_info()
        else:
            input_device_info = self.pyaudio.get_device_info_by_index(input_device_index)

        print("Using input device '{}'.".format(input_device_info.get('name')))

        if self.overlap:
            stream_callback = self.read_audio_callback_overlap
        else:
            stream_callback = self.read_audio_callback

        self.stream = self.pyaudio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            input_device_index=input_device_index,
            output=False,
            stream_callback=stream_callback,
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

    def read_audio_callback_overlap(self, in_data, frame_count, time_info, flag):
        if self.chunk_tail is not None:
            chunk = np.concatenate((self.chunk_tail, np.frombuffer(in_data, dtype=np.float32)))
        else:
            chunk = np.frombuffer(in_data, dtype=np.float32)
        self.chunk_tail = chunk[-self.overlap:]

        try:
            self.chunk_queue.put_nowait(chunk)
        except queue.Full:
            print("analyze queue overrun :-(")

        return None, pyaudio.paContinue
