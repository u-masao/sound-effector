import time

import streamlit as st
from utils.audio_interface import AudioInterface

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
            status_text.text(f"{i} frames display")
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
    display_index = 0
    while ai.is_active() and display_index < 3:
        frames = ai.get_waveforms()
        frame_length = len(frames)
        for i in range(display_index, frame_length):
            status_text.text(f"{i} frames display")
            chart.add_rows(frames[i])
            progress_bar.progress(i)
            time.sleep(0.05)

        display_index = frame_length

    ai.stop()
    print("play done")
    del ai
