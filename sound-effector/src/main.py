import wave

import numpy as np
import pandas as pd
import pyaudio
import streamlit as st


class AudioInterface:
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100
        self.record_second = 3

        self.frames = []
        self.p = pyaudio.PyAudio()

    def record(self):
        stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.fs,
            input=True,
            frames_per_buffer=self.chunk,
        )

        self.frames = []
        data = []

        for i in range(int(self.fs / self.chunk * self.record_second)):
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        self.p.terminate()

    def save(self, filename):

        wf = wave.open(filename, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.fs)
        wf.writeframes(b"".join(self.frames))
        wf.close()

    def load(self, filename):
        wf = wave.open(filename, "rb")
        stream = self.p.open(
            format=self.p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )
        self.frames = []
        data = wf.readframes(self.chunk)

        while data != "":
            self.frames.append(data)
            stream.write(data)
            data = wf.readframes(self.chunk)
        stream.stop_stream()
        stream.close()

    def play(self):
        pass

    def __def__(self):
        self.p.terminate()


st.title("hey")
st.write("hey")

ai = AudioInterface()
if st.button("save"):
    st.write("hello")
    ai.record()
    ai.save("data/raw/record.wav")

if st.button("load"):
    st.write("hello")
    ai.load("data/raw/record.wav")

if st.button("play"):
    ai.play()
