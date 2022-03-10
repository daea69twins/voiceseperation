# imports
import pyaudio
import wave
from audioplayer import AudioPlayer

# from .ipynb
import noisereduce as nr
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import librosa
import librosa.display
import IPython.display as ipd
import matplotlib.pyplot as plt
from pydub import AudioSegment
import soundfile as sf
from torch import hub

# ---------------------------------------------------
# recording audio file from board

# the file name output you want to record into
file = "recorded"
filename = file + ".wav"
# set the chunk size of 1024 samples
chunk = 1024
# sample format
FORMAT = pyaudio.paInt16
# mono, change to 2 if you want stereo
channels = 1
# 22050 samples per second
sample_rate = 22050
record_seconds = 5
# initialize PyAudio object
p = pyaudio.PyAudio()
# open stream object as input & output
stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)
frames = []
print("Recording...")
for i in range(int(44100 / chunk * record_seconds)):
    data = stream.read(chunk)
    frames.append(data)
print("Finished recording.")
# stop and close stream
stream.stop_stream()
stream.close()
# terminate pyaudio object
p.terminate()
# save audio file
# open the file in 'write bytes' mode
wf = wave.open(filename, "wb")
# set the channels
wf.setnchannels(channels)
# set the sample format
wf.setsampwidth(p.get_sample_size(FORMAT))
# set the sample rate
wf.setframerate(sample_rate)
# write the frames as bytes
wf.writeframes(b"".join(frames))
# close the file
wf.close()


# ---------------------------------------------------
# splitting and noise reducing

filepath = "./"
# load data
data, rate = librosa.load(filename)

# split audio
model = hub.load('JorisCos/asteroid', 'conv_tasnet', 'JorisCos/ConvTasNet_Libri2Mix_sepclean_8k')
audio_filepath = filepath + filename
model.separate(audio_filepath, resample=True, force_overwrite=True)

# audio stream 1
s1_filename = file + '_est1.wav'
s1, rate = librosa.load(filepath+s1_filename)
reduced_noise1 = nr.reduce_noise(y=s1, sr=rate)
voice1_file = filepath + 'voice1.wav'
sf.write(voice1_file, reduced_noise1, rate)

# audio stream 2
s2_filename = file + '_est2.wav'
s2, rate = librosa.load(filepath+s2_filename)
reduced_noise2 = nr.reduce_noise(y=s2, sr=rate)
voice2_file = filepath + 'voice2.wav'
sf.write(voice2_file, reduced_noise2, rate)

# normalize audio streams
orig = AudioSegment.from_file(audio_filepath)
stream1 = AudioSegment.from_file(voice1_file)
stream2 = AudioSegment.from_file(voice2_file)

normalized1 = stream1.apply_gain(orig.dBFS - stream1.dBFS)
normalized2 = stream2.apply_gain(orig.dBFS - stream2.dBFS)

normalized1.export(voice1_file, format='wav')
normalized2.export(voice2_file, format='wav')

# ---------------------------------------------------
# playback

AudioPlayer("./recorded.wav").play(block=True)
AudioPlayer("./voice1.wav").play(block=True)
AudioPlayer("./voice2.wav").play(block=True)
