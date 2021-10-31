import time

import pyaudio

"""
example code

pyaudio async recording
"""

frames = []


def input_callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)


def main():

    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=8000,
        input=True,
        frames_per_buffer=1024,
        stream_callback=input_callback,
    )

    stream.start_stream()
    start = time.time()
    while stream.is_active() and time.time() - start < 3:
        print(len(frames))
        if len(frames) > 0:
            # print(frames[-1])
            pass
        time.sleep(0.25)

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    main()
