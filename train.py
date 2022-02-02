from sklearn.neighbors import KNeighborsClassifier
import glob
import os
import pickle
from sklearn.metrics import accuracy_score
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
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
if __name__=="__main__":
    observed = ["normal", "elated", "manic", "down", "depressed"]
    X = []
    y = []
    for file in glob.glob("./Macillion_Audio/*.wav"):
        file_name = os.path.basename(file)
        emotion = file_name.split("_")[1]
        feature = feature_extraction(file, mfcc = True, mel=True, chroma=True, rms=True, zcr=True)
        X.append(feature)
        y.append(emotion)
    x_train, x_test, y_train, y_test = train_test_split(np.array(X), y, test_size=0.2, random_state=42) #split data into testing and training sets.
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(x_train, y_train) #train the model
    y_pred = model.predict(x_test)
    pkl_filename = "model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    print(y_pred)
    print(accuracy)