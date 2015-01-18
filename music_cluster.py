import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import urllib
import urllib2
import base64
import json
import os
import sys
import csv
import urllib, urllib2
import json
from pylab import plot,show
from numpy import vstack,array
from numpy import sum
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
import numpy as np
from sklearn.decomposition import PCA
import sklearn.preprocessing as preprocessing
from sklearn.cluster import k_means as k_means
import spotipy
import spotipy.util as util

DATABASE = '/tmp/features.db'
DEBUG = True
USERNAME = 'test'
PASSWORD = 'test'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'why would I tell you my secret key?'
SPOTIPY_CLIENT_ID='562a7296affa4b5dbe70437d11d837e3'
SPOTIPY_CLIENT_SECRET='0153de287f2c45e0846c0390b67f991d'
SPOTIPY_REDIRECT_URL = 'http://localhost:5000/authorize/'

scope = 'user-library-read'
username = 'DChen7'
api_key = 'PV1DZKHWQ6OZX6LEO'
api_key2 = '4BHBA6BB9J7GOEAJU'
api_key3 = '4L4M7QV9W0QSNZ2UD'

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

#def show_tracks(tracks):
    # songid_file = open("static/songids.csv", 'w')
    # writer = csv.writer(songid_file)
    # for i, item in enumerate(tracks['items']):
    #     track = item['track']
    #     print "   %d %32.32s %s" % (i, track['artists'][0]['name'],
    #         track['name'])
       #  url = "http://developer.echonest.com/api/v4/song/search"
       #  data = {}
       #  data['api_key'] = api_key
       #  artist = (("%32.32s" % (track['artists'][0]['name'])).encode("utf8")).strip()
       #  data['artist'] = artist
       #  name = track['name']
       #  data['title'] = name
       #  url_values = urllib.urlencode(data)
       #  full_url = url + '?' + url_values
       #  print full_url
       #  print
      	# if artist and name:
	      #   ids = urllib2.urlopen(full_url).read()
	      #   json_response = json.loads(ids)
	      #   print json_response
	      #   if len(json_response["response"]["songs"]) > 0:
	      #   	song_id = json_response["response"]["songs"][0]["id"]
		     #    url2 = "http://developer.echonest.com/api/v4/song/profile"
		     #    data2 = {}
		     #    data2['api_key'] = api_key
		     #    data2['id'] = song_id
		     #    data2['bucket'] = 'audio_summary'
		     #    url_values2 = urllib.urlencode(data2)
		     #    full_url2 = url2 + '?' + url_values2
		     #    features = urllib2.urlopen(full_url2).read()
		     #    json_response2 = json.loads(features)


		     #    acousticness = json_response2["response"]["songs"][0]["audio_summary"]["acousticness"]
		     #    danceability = json_response2["response"]["songs"][0]["audio_summary"]["danceability"]
		     #    duration = json_response2["response"]["songs"][0]["audio_summary"]["duration"]
		     #    energy = json_response2["response"]["songs"][0]["audio_summary"]["energy"]
		     #    liveness = json_response2["response"]["songs"][0]["audio_summary"]["liveness"]
		     #    loudness = json_response2["response"]["songs"][0]["audio_summary"]["loudness"]
		     #    mode = json_response2["response"]["songs"][0]["audio_summary"]["mode"]
		     #    speechiness = json_response2["response"]["songs"][0]["audio_summary"]["speechiness"]
		     #    tempo = json_response2["response"]["songs"][0]["audio_summary"]["tempo"]
		     #    feature_arr = [song_id, name, artist, acousticness, danceability, duration, energy, liveness, loudness, mode, speechiness, tempo]
		        
		     #    writer.writerow(feature_arr)

# def spotify_info():
# 	token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URL)
# 	if token:
# 	    sp = spotipy.Spotify(auth=token)
# 	    playlists = sp.user_playlists(username)
#         for playlist in playlists['items']:
#             if playlist['owner']['id'] == username:
#                 print playlist['name']
#                 print '  total tracks', playlist['tracks']['total']
#                 results = sp.user_playlist(username, playlist['id'],
#                     fields="tracks,next")
#                 tracks = results['tracks']
#                 show_tracks(tracks)
#                 while tracks['next']:
#                     tracks = sp.next(tracks)
#                     show_tracks(tracks)
#                 break
# 	else:
# 	    print "Can't get token for", username

@app.route('/')
def index():
	#spotify_info()
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
	if request.method == 'POST':
		url = 'https://accounts.spotify.com/authorize'
		data = {}
		data['client_id'] = SPOTIPY_CLIENT_ID
		data['response_type'] = 'code'
		data['redirect_uri'] = SPOTIPY_REDIRECT_URL
		data['scope'] = scope
		url_values = urllib.urlencode(data)
		full_url = url + '?' + url_values
		response = urllib2.urlopen(full_url)
		#spotify_info()
		print response.read()
		return redirect(url_for('authorize'))


@app.route('/authorize')
def authorize():
	code = request.args.get('code')
	print "CODE: " + code
	url = 'https://accounts.spotify.com/api/token'
	values = {'grant_type' : 'authorization_code',
						'code' : code,
						'redirect_uri' : SPOTIPY_REDIRECT_URL,
						'client_id' : SPOTIPY_CLIENT_ID,
						'client_secret' : SPOTIPY_CLIENT_SECRET
	}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req).read()
	json_response = json.loads(response)
	access_token = json_response['access_token']
	refresh_token = json_response['refresh_token']
	print access_token
	return redirect(url_for('cluster'))

@app.route('/cluster')
def cluster():
	songid_file = open("static/songids.csv", "rU")
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

	costs = []
	ratios = []
	ratio_differences = []
	for i in range(3, 11):
		kmeans_data = k_means(pcaed, n_clusters=i)
		cost = kmeans_data[2]
		costs.append(cost)
		if i > 3:
			ratios.append(costs[i - 3] / costs[i - 4])
		if i > 4:
			ratio_differences.append(abs(ratios[i - 4] - ratios[i - 5]))
	
	n_clusters = 0
	max_diff = 0
	for i in range(0, len(ratio_differences)):
		if ratio_differences[i] > max_diff:
			max_diff = ratio_differences[i]
			n_clusters = i

	n_clusters += 4
	print n_clusters

	returned = k_means(pcaed, n_clusters=n_clusters) 
	print returned



	centroids = returned[0]


        #write centroids, but with original features
        centroid_features = []
        for i in range(0, max(returned[1]) + 1): #for each cluster
                tot = [0] * 9
                num_el = 0
                for ii in range(0, len(returned[1])): #for each song
                        if (returned[1][ii] == i): # if it's this cluster
                                tot = sum([features[ii], tot], axis=0)
                                num_el+=1.
                print(tot)
                tot *= 1/(num_el)
                centroid_features.append(tot)

        print("centroid features[0] is")
        print(centroid_features[0])
        with open('static/features.csv', 'wb') as csvfile:
                feature_writer = csv.writer(csvfile)
                for i in range(0, len(centroid_features)):
                        feature_writer.writerow([centroid_features[i][0],centroid_features[i][1],centroid_features[i][2],centroid_features[i][3],centroid_features[i][4],centroid_features[i][5],centroid_features[i][6],centroid_features[i][7],centroid_features[i][8]])
        
        #write centroids                                                                                                     
        with open('static/centroids.csv', 'wb') as csvfile:
                center_writer = csv.writer(csvfile)
                for i in range (0, len(centroids)):
                        center_writer.writerow([str(i), centroids[i][0], centroids[i][1], centroids[i][2]])
	x1 = []
	x2 = []
	x3 = []

	for i in range(0, len(pcaed)):
		x1.append(pcaed[i][0])
		x2.append(pcaed[i][1])
		x3.append(pcaed[i][2])

	min1 = min(x1)
	min2 = min(x2)
	min3 = min(x3)

	for i in range(0, len(x1)):
		x1[i] -= min1
		x2[i] -= min2
		x3[i] -= min3

	names = []
	artists = []
	for i in range(0,len(other)):
		names.append(other[i][0])
		artists.append(other[i][1])
	print names
	print artists

	clusters = returned[1].tolist()
	colors = []
	options = {0 : "#000",  #black
					1 : "#FF0000", #red
					2 : "#0000FF", #blue
					3 : "#008000", #green
					4 : "#FFA500", #orange
					5 : "#800080", #purple
					6 : "#625D5D", #grey
					7 : "#00FFFF", #blue
					8 : "#FFE5B4", #light orange
					9 : "#FC6C85",#pink
	}
	for i in range(0, len(clusters)):
		colors.append(options[clusters[i]])
	print colors
	xmax = []
	xmax.append(max(x1))
	xmax.append(max(x2))
	xmax.append(max(x3))
	
	num_colors=max(clusters) + 1

	return render_template('cluster.html', colors=json.dumps(colors), x1=json.dumps(x1), x2=json.dumps(x2), x3=json.dumps(x3), names=json.dumps(names), artists=json.dumps(artists), xmax=json.dumps(xmax), num_colors=json.dumps(num_colors))

if __name__ == '__main__':
	app.run(host='0.0.0.0')
