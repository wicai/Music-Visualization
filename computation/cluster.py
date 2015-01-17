#usr/bin/env python
import csv
import numpy
import sklearn.preprocessing as preprocessing

songid_file = open("../static/songids.csv", "rU")
reader = csv.reader(songid_file)
features = []
for row in reader:
    acousticness = float(row[3])
    danceability = float(row[4])
    duration = float(row[5])
    energy = float(row[6])
    liveness = float(row[7])
    loudness = float(row[8])
    mode = float(row[9])
    speechiness = float(row[10])
    tempo = float(row[11])
    feature_arr = [acousticness, danceability, duration, energy, liveness, loudness, mode, speechiness, tempo]
    features.append(feature_arr)

print features
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
trained=min_max_scaler.fit_transform(features)


