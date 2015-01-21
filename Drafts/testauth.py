import urllib
import urllib2
import requests
import json

SPOTIPY_CLIENT_ID='562a7296affa4b5dbe70437d11d837e3'
SPOTIPY_CLIENT_SECRET='0153de287f2c45e0846c0390b67f991d'

username = 'dchen7'
create_playlist = "https://api.spotify.com/v1/users/" + username + "/playlists"
values = {'name' : 'Test Playlist'}
token = "BQDhZoPcw652OjGioO9kOm3-GrUrw5xpGk_YdUVqf-lHoApRUYwTbkxLv6O1ONsM9Xtg-BL0lxTAjcZ-FmrnfqLsRwcH3SgMt_a4NRHfsRMKuHsnt7VW9CVprzhZjamFMbHkFmES-4nbTVKKo_XDM1KKUSJBazgAD64h02sT0iV99cQgoVbpU0gw50y3VGFYnw7_YwVH8gyXKDIwHTQl8IMBxM6UJ5WtrBmodhOTXnvcHA"
auth = "Bearer " + token
print auth
headers = {'Content-Type': 'application/json', 'Authorization' : auth}
r = requests.post(create_playlist, data=json.dumps(values), headers=headers)
print r.text
json_response = json.loads(r.text)
playlist_id = json_response["id"]

add_playlist = "https://api.spotify.com/v1/users/" + username + "/playlists/" + playlist_id + "/tracks"
values = {'uris' : ['spotify:track:4iV5W9uYEdYUVa79Axb7Rh']}
r = requests.post(add_playlist, data=json.dumps(values), headers=headers)
print r.text



