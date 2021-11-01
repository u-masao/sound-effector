import time
import wave

import numpy as np
import pyaudio
import streamlit as st


class AudioInterface:

    """
    ```
    import time

    ai = AudioInterface()
    start = time.time()
    while ai.is_active() and time.time() - start < 3:
        if len(ai.get_frames()) > 0:
            # print(ai.get_frames[-1])
            pass
        time.sleep(0.25)
    ```
    """

    def input_callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def output_callback(self, in_data, frame_count, time_info, status):
        status = pyaudio.paContinue
        data = None
        if len(self.frames) > self.play_index:
            data = self.frames[self.play_index]
            self.play_index += 1
        elif len(self.frames) == self.play_index:
            status = pyaudio.paComplete
        else:
            status = pyaudio.paAbort

        return (data, status)

    def __init__(
        self, channels=2, chunk=1024, format=pyaudio.paInt16, sampling_rate=8000
    ):
        self.frames = []

        self.channels = channels
        self.chunk = chunk
        self.format = format
        self.sampling_rate = sampling_rate

        self.p = pyaudio.PyAudio()

    def __del__(self):
        self.p.terminate()

    def get_frames(self):
        return self.frames

    def get_waveforms(self):
        waveforms = []
        for frame in self.frames:
            waveforms.append(np.array(self.parse_frame(frame)))
            waveforms[-1] = [np.mean(x) for x in np.array_split(waveforms[-1], 32, 0)]
        return waveforms

    def parse_frame(self, frame):
        values = []
        sample_size = self.p.get_sample_size(self.format)
        for i in range(len(frame) // sample_size):
            values.append(
                int.from_bytes(
                    frame[(i * sample_size) : ((i + 1) * sample_size)],
                    byteorder="big",
                    signed=True,
                )
            )
        values = [
            values[i : (i + self.channels)]
            for i in range(0, len(values), self.channels)
        ]
        return values

    def record(self):

        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.sampling_rate,
            frames_per_buffer=self.chunk,
            input=True,
            stream_callback=self.input_callback,
        )

    def play(self):
        self.play_index = 0
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.sampling_rate,
            frames_per_buffer=self.chunk,
            output=True,
            stream_callback=self.output_callback,
        )

    def is_active(self):
        return self.stream.is_active()

    def start(self):
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()

    def save(self, filename):
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.sampling_rate)
            wf.writeframes(b"".join(self.frames))

    def load(self, filename):
        self.frames = []
        with wave.open(filename, "rb") as wf:
            self.channels = wf.getnchannels()
            self.sampling_rate = wf.getframerate()
            self.format = self.p.get_format_from_width(wf.getsampwidth())
            while True:
                data = wf.readframes(self.chunk)
                if len(data) <= 0:
                    break
                self.frames.append(data)


st.title("sound effect")
st.write("pyaudio のテスト")


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
chart = st.line_chart()

if st.button("record"):
    record_sec = 5

    ai = AudioInterface()
    ai.record()
    ai.start()
    start = time.time()
    display_index = 0
    while ai.is_active() and time.time() - start < record_sec:
        frames = ai.get_waveforms()
        frame_length = len(frames)
        for i in range(display_index, frame_length):
            status_text.text(f"{i} frames display")  # ToDo parse int16
            chart.add_rows(frames[i])
            progress_bar.progress(i)
            time.sleep(0.05)

        display_index = frame_length

    ai.stop()
    print("recod done")
    ai.save("data/raw/record.wav")
    print("save done")
    ai.play()
    ai.start()
    start = time.time()
    while ai.is_active() and time.time() - start < record_sec:
        if len(ai.get_frames()) > 0:
            # print(ai.get_frames[-1])
            pass
        time.sleep(0.25)
    ai.stop()
    print("play done")
    del ai

if st.button("play"):
    ai = AudioInterface()
    ai.load("data/raw/record.wav")
    ai.play()
    ai.start()
    start = time.time()
    display_index = 0
    while ai.is_active() and display_index < 3:
        frames = ai.get_waveforms()
        frame_length = len(frames)
        for i in range(display_index, frame_length):
            status_text.text(f"{i} frames display")  # ToDo parse int16
            chart.add_rows(frames[i])
            progress_bar.progress(i)
            time.sleep(0.05)

        display_index = frame_length

    ai.stop()
    print("play done")
    del ai
