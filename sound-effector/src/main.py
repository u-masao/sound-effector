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
        self.wf = None
        print("__init__()")

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
        self.wf = wave.open(filename, "wb")
        self.wf.setnchannels(self.channels)
        self.wf.setsampwidth(self.p.get_sample_size(self.format))
        self.wf.setframerate(self.fs)
        self.wf.writeframes(b"".join(self.frames))
        self.wf.close()

    def load(self, filename):
        self.wf = wave.open(filename, "rb")
        stream = self.get_output_stream(self.wf)
        self.frames = []
        data = self.wf.readframes(self.chunk)

        while len(data) > 0:
            self.frames.append(data)
            stream.write(data)
            data = self.wf.readframes(self.chunk)
        stream.stop_stream()
        stream.close()

    def get_output_stream(self, wf):
        return self.p.open(
            format=self.p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )

    def play(self, filename):
        self.wf = wave.open(filename, "rb")
        stream = self.get_output_stream(self.wf)
        print(stream)
        for data in self.frames:
            stream.write(data)
        stream.stop_stream()
        stream.close()

    def __def__(self):
        self.p.terminate()


st.title("sound effect")
st.write("pyaudio のテスト")

if st.button("save"):
    ai = AudioInterface()
    ai.record()
    ai.save("data/raw/record.wav")
    print("done")

if st.button("load"):
    ai = AudioInterface()
    ai.load("data/raw/record.wav")
    print("done")

if st.button("play"):
    ai = AudioInterface()
    ai.record()
    ai.play("data/raw/record.wav")
    print("done")
