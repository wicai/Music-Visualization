#usr/bin/env python
import csv
import numpy
import sklearn.preprocessing as preprocessing
from sklearn.decomposition import PCA as PCA
from sklearn.cluster import k_means as k_means

songid_file = open("../static/songids.csv", "rU")
reader = csv.reader(songid_file)
features = []
other = []

for row in reader:
    other_row = [row[1], row[2]]
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
    other.append(other_row)
print features
print other
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
trained=min_max_scaler.fit_transform(features)
print trained

pca = PCA(copy=True, n_components=3, whiten=False)
pca.fit(trained)

pcaed = pca.fit_transform(trained)
print pcaed

n_clusters = 3
returned = k_means(pcaed, n_clusters=n_clusters) 
print returned

