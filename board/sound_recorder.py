#!/usr/bin/python

import argparse
import wave
from time import gmtime, strftime
from os import system

import pyaudio


class SoundRecorder:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Read microphone')
        parser.add_argument('-f', '--FORMAT', help='format type', type=int,
                            default=pyaudio.paInt32, required=False)
        parser.add_argument('-ca', '--CHANNEL', help='channels', type=int,
                            default=2, required=False)
        parser.add_argument('-r', '--RATE', help='sample rate', type=int,
                            default=44100, required=False)
        parser.add_argument('-cu', '--CHUNK', help='chunk size', type=int,
                            default=1024, required=False)
        parser.add_argument('-s', '--SECOND', help='record seconds', type=int,
                            default=20, required=False)
        parser.add_argument('-o', '--OUTPUT', help='wave output file name',
                            type=str,
                            default=strftime("mic%Y-%m-%d_%H:%M:%S", gmtime()) + ".wav",
                            required=False)
        self.args = parser.parse_args()

    def record_sound(self, audio_format, channel, rate, chunk, second, output):
        audio = pyaudio.PyAudio()
        # start Recording
        stream = audio.open(format=audio_format,
                            channels=channel,
                            rate=rate,
                            input=True,
                            frames_per_buffer=chunk)
        print "recording..."
        frames = []
        for i in range(0, int(rate / chunk * second)):
            data = stream.read(chunk)
            frames.append(data)
        print "finished recording"

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        wave_file = wave.open(output, 'wb')
        wave_file.setnchannels(channel)
        wave_file.setsampwidth(audio.get_sample_size(audio_format))
        wave_file.setframerate(rate)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        system('cp ' + output + ' orig.wav')

    def run(self):
        self.record_sound(self.args.FORMAT, self.args.CHANNEL, self.args.RATE,
                          self.args.CHUNK, self.args.SECOND, self.args.OUTPUT)


if __name__ == "__main__":
    sm = SoundRecorder()
    sm.run()
