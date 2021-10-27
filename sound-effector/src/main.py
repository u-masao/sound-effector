import pyaudio
import wave
import streamlit as st
import pandas as pd
import numpy as np


class AudioInterface:
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100
        self.record_second = 3

        self.p = pyaudio.PyAudio()


    def record(self):
        stream = self.p.open(format=self.format, channels=self.channels, rate=self.fs, input=True, frames_par_buffer=self.chunk)
        print("recording")

        self.frames = []

        for i in range(int(self.fs / self.chunk * self.record_second)):
            data = stream.read(self.chunk)
            self.frames.append(self.data)

        print("done recording")

        stream.stop_stream()
        stream.close()
        self.p.terminate()

    def save(self, filename="output.wav"):

        wf = wave.open(filename, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.fs)
        wf.writeframes(b"".join(frames))
        wf.close()


st.title("hey")
st.write("hey")

if st.button("recording"):
    st.write("hello")
    ai = AudioInterface()
    ai.record()
    ai.save()
    print("pushed")
else:
    st.write("bye")


