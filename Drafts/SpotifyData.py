import sys
import spotipy
import spotipy.util as util
import csv
import urllib, urllib2
import json
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
import numpy as np
from sklearn.decomposition import PCA
import sklearn.preprocessing as preprocessing

SPOTIPY_CLIENT_ID='562a7296affa4b5dbe70437d11d837e3'
SPOTIPY_CLIENT_SECRET='0153de287f2c45e0846c0390b67f991d'
SPOTIPY_REDIRECT_URL = 'localhost:5000/authorize'

scope = 'user-library-read'
username = 'charmip'
api_key = 'PV1DZKHWQ6OZX6LEO'

def cluster():
    songid_file = open("/Users/danielchen/Documents/Music-Visualization/static/songids.csv", "rU")
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
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
    trained=min_max_scaler.fit_transform(features)
    pca = PCA(n_components=3)
    trained = pca.fit_transform(trained)
    print(pca.explained_variance_ratio_)
    print trained

def show_tracks(results):
    songid_file = open("/Users/danielchen/Documents/Music-Visualization/static/songids.csv", 'w')
    writer = csv.writer(songid_file)
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print "   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name'])
        url = "http://developer.echonest.com/api/v4/song/search"
        data = {}
        data['api_key'] = api_key
        artist = (("%32.32s" % (track['artists'][0]['name'])).encode("utf8")).strip()
        data['artist'] = artist
        name = track['name']
        data['title'] = name
        url_values = urllib.urlencode(data)
        full_url = url + '?' + url_values
        ids = urllib2.urlopen(full_url).read()
        json_response = json.loads(ids)
        song_id = json_response["response"]["songs"][0]["id"]

        url2 = "http://developer.echonest.com/api/v4/song/profile"
        data2 = {}
        data2['api_key'] = api_key
        data2['id'] = song_id
        data2['bucket'] = 'audio_summary'
        url_values2 = urllib.urlencode(data2)
        full_url2 = url2 + '?' + url_values2
        features = urllib2.urlopen(full_url2).read()
        json_response2 = json.loads(features)


        acousticness = json_response2["response"]["songs"][0]["audio_summary"]["acousticness"]
        danceability = json_response2["response"]["songs"][0]["audio_summary"]["danceability"]
        duration = json_response2["response"]["songs"][0]["audio_summary"]["duration"]
        energy = json_response2["response"]["songs"][0]["audio_summary"]["energy"]
        liveness = json_response2["response"]["songs"][0]["audio_summary"]["liveness"]
        loudness = json_response2["response"]["songs"][0]["audio_summary"]["loudness"]
        mode = json_response2["response"]["songs"][0]["audio_summary"]["mode"]
        speechiness = json_response2["response"]["songs"][0]["audio_summary"]["speechiness"]
        tempo = json_response2["response"]["songs"][0]["audio_summary"]["tempo"]
        feature_arr = [song_id, name, artist, acousticness, danceability, duration, energy, liveness, loudness, mode, speechiness, tempo]
        
        writer.writerow(feature_arr)


token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URL)
if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print playlist['name']
                print '  total tracks', playlist['tracks']['total']
                results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
                break
else:
    print "Can't get token for", username
cluster()