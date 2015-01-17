import urllib
import urllib2
import json

echonest_playlists_api = 'http://developer.echonest.com/api/v4/playlist/static?'
echonest_songs_api = 'http://developer.echonest.com/api/v4/song/search?'
echonest_taste_profile_create_api = 'http://developer.echonest.com/api/v4/tasteprofile/create'
echonest_taste_profile_update_api = 'http://developer.echonest.com/api/v4/tasteprofile/update'

api_key = "4L4M7QV9W0QSNZ2UD"

def find_data():
    url = 'http://developer.echonest.com/api/v4/song/search?api_key=FILDTEOIK2HBORODV&artist=kanye%20west&title=all%20of%20the%20lights'
    response = urllib2.urlopen(url)
    page = response.read()
    print(page)

def find_songs(acoustic, danceability, duration, energy, liveness, loudness, mode, speechiness, tempo):  
    values = {
        'api_key': api_key,
        'min_acousticness': acoustic - 0.05 if acoustic - 0.05 > 0 else 0.001,
        'max_acousticness': acoustic + 0.05 if acoustic + 0.05 < 1 else 0.999,
        'min_danceability': danceability - 0.05 if danceability - 0.05 > 0 else 0.001,
        'max_danceability': danceability + 0.05 if danceability + 0.05 < 1 else 0.999,
        'min_duration': duration - 30 if duration - 30 > 0 else 0.001,
        'max_duration': duration + 30 if duration + 30 < 3600 else 3599.999,
        'min_energy': energy - 0.05 if energy - 0.05 > 0 else 0.001, 
        'max_energy': energy + 0.05 if energy + 0.05 < 1 else 0.999,
        'min_liveness': liveness - 0.05 if liveness - 0.05 > 0 else 0.001,
        'max_liveness': liveness + 0.05 if liveness + 0.05 < 1 else 0.999,
        'min_loudness': loudness - 5.5 if loudness - 5.5 > -100 else -99.999,
        'max_loudness': loudness + 5.5 if loudness + 5.5 < 100 else 99.999,
        'mode': mode,
        'min_speechiness': speechiness - 0.05 if speechiness - 0.05 > 0 else 0.001,
        'max_speechiness': speechiness + 0.05 if speechiness + 0.05 < 1 else 0.999,
        'min_tempo': tempo - 10.5 if tempo - 10.5 > 0 else 0.001,
        'max_tempo': tempo + 10.5 if tempo + 10.5 < 500 else 499.999,
        'sort': 'song_hotttnesss-desc',
        'results': 25
    }
    data = urllib.urlencode(values)
    url = echonest_songs_api + data

    try: 
        response = urllib2.urlopen(url)
        song_ids = []
        songs = json.loads(response.read())["response"]["songs"]
        
        for s in songs:
            song_ids.append(str(s["id"]))
            #song_data[str(s["id"])]["artist_id"] = str(s["artist_id"])
        #print song_ids  
        return song_ids
    except urllib2.URLError as e:
        print(e.reason)

def create_taste_profile(songs):
    values = {
        'api_key': api_key,
        'type': 'song',
        'name': 'song_catalog',
        'format': 'json'
    }
     
    data = urllib.urlencode(values)
    req = urllib2.Request(echonest_taste_profile_create_api, data)
    
    try: 
        response = urllib2.urlopen(req)  
        response_data = response.read()   
        success = str(json.loads(response_data)["response"]["status"]["message"])
        print(success)
        if(success == 'Success'):
            catalog_id = str(json.loads(response_data)["response"]["id"])
        else:
            catalog_id = str(json.loads(response_data)["response"]["status"]["id"])
        
        taste_profile = []
        
        for i in songs:
            taste_profile.append({'item': {'song_id': i}})
        json_taste_profile = json.dumps(taste_profile)

        update_values = {
            'api_key': api_key,
            'id': catalog_id,
            'data': json_taste_profile,
            'data_type': 'json',
            'format': 'json'
        }
        
        update_data = urllib.urlencode(update_values)
        update_req = urllib2.Request(echonest_taste_profile_update_api, update_data)
        try:
            update_response = urllib2.urlopen(req)
            print(update_response.read())
        except urllib2.URLError as update_e:
            print(update_e.reason)
        
        
        # u = 'http://developer.echonest.com/api/v4/tasteprofile/read?api_key=4L4M7QV9W0QSNZ2UD&format=json&id=' + catalog_id + '&bucket=audio_summary'
        # print(u)
        # u1 = urllib2.urlopen(u)
        # p = u1.read()
        # print(p)
        
        return catalog_id
        
    except urllib2.URLError as e:
        print(e.reason)
   
def create_playlist(taste_profile_id):
    values = {
        'api_key': api_key,
        'results': 20,
        'type': 'catalog',
        'seed_catalog': taste_profile_id
    }
    
    data = urllib.urlencode(values)
    req = urllib2.Request(echonest_playlists_api, data)
    try:
        print(data)
        response = urllib2.urlopen(req)
        
    except urllib2.URLError as e:
        print(e.reason)


songs = find_songs(0.9101, 0.1515, 401.30667, 0.2253, 0.07785, -15.4083, 1, 0.0354, 83.3769)
taste_profile_id = create_taste_profile(songs)
#create_playlist(taste_profile_id)
# find_data()