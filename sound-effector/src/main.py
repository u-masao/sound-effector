import time
import wave

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

    def __def__(self):
        self.p.terminate()

    def get_frames(self):
        return self.frames

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
            with self.get_output_stream(wf) as stream:
                while True:
                    data = wf.readframes(self.chunk)
                    if len(data) <= 0:
                        break
                    self.frames.append(data)
                stream.stop_stream()


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
        frames = ai.get_frames()
        frame_length = len(frames)
        for i in range(display_index, frame_length):
            status_text.text(f"{i} frames display")  # ToDo parse int16
            chart.add_rows([max(list(frames[i]))])
            progress_bar.progress(i)
            time.sleep(0.05)

        display_index = frame_length

    ai.stop()
    print("recod done")
    ai.save("data/raw/record.wav")
    print("save done")
    ai.play()
    start = time.time()
    while ai.is_active() and time.time() - start < record_sec:
        if len(ai.get_frames()) > 0:
            # print(ai.get_frames[-1])
            pass
        time.sleep(0.25)
    ai.stop()
    print("play done")
