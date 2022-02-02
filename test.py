import glob
import os
import pickle
import numpy as np
import librosa
from scipy.io.wavfile import write
import sounddevice as sd
def feature_extraction(file_name, mfcc, mel, chroma, zcr, rms):
    y, sr = librosa.load(file_name) # get the audio data and sampling rate
    result = np.array([])
    if mfcc:
        mfcc=np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40))
        result=np.hstack((result, mfcc))
    if zcr:
        zcr = np.mean(librosa.feature.chroma_stft(y, sr=sr))
        result=np.hstack((result, zcr))
    if rms:
        rms = np.median(librosa.feature.rms(y=y).T, axis= 0)
        result = np.hstack((result, rms))
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(y, sr))
        result = np.hstack((result, mel))
    if chroma:
        chroma = np.mean(librosa.feature.chroma_stft(y, sr))
        result = np.hstack((result, chroma))
    return result

def record_to_file():
    fs = 44100  # Sample rate
    seconds = 3 # Duration of recording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    file_name = "test.wav"
    write(file_name, fs, myrecording)
    return file_name

def predict_emotion():
    # load the saved model (after training)
    model = pickle.load(open("model.pkl", "rb"))
    #print("Please talk")
    filename = record_to_file()
    # record the file (start talking)
    # extract features and reshape it
    features = feature_extraction(filename, mfcc=True, mel=True, chroma=True, rms=True, zcr=True).reshape(1, -1)
    # predict
    emotion = model.predict(features)[0]
    # show the result !
    #print(emotion)
    return emotion
