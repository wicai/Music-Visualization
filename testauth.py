import urllib
import urllib2

SPOTIPY_CLIENT_ID='562a7296affa4b5dbe70437d11d837e3'
SPOTIPY_CLIENT_SECRET='0153de287f2c45e0846c0390b67f991d'
scope = 'user-library-read'

url = 'https://accounts.spotify.com/authorize'
data = {}
data['client_id'] = SPOTIPY_CLIENT_ID
data['response_type'] = 'code'
data['redirect_uri'] = '/'
data['scope'] = scope
url_values = urllib.urlencode(data)
full_url = url + '?' + url_values
response = urllib2.urlopen(full_url).read()
print response

