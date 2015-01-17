import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_oauthlib.client import OAuth, OAuthException
from contextlib import closing
import urllib
import urllib2
import base64
import json
import os

DATABASE = '/tmp/features.db'
DEBUG = True
USERNAME = 'test'
PASSWORD = 'test'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'why would I tell you my secret key?'
oauth = OAuth(app)
SPOTIPY_CLIENT_ID='562a7296affa4b5dbe70437d11d837e3'
SPOTIPY_CLIENT_SECRET='0153de287f2c45e0846c0390b67f991d'

scope = 'user-library-read'
username = 'charmip'


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

spotify = oauth.remote_app(
    'spotify',
    consumer_key=SPOTIPY_CLIENT_ID,
    consumer_secret=SPOTIPY_CLIENT_SECRET,
    # Change the scope to match whatever it us you need
    # list of scopes can be found in the url below
    # https://developer.spotify.com/web-api/using-scopes/
    request_token_params={username: username, scope: scope},
    base_url='https://accounts.spotify.com',
    request_token_url=None,
    access_token_url='/api/token',
    authorize_url='https://accounts.spotify.com/authorize'
)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    callback = url_for(
        'spotify_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    print callback
    return spotify.authorize(callback=callback)


@app.route('/login/authorized')
def spotify_authorized():
    resp = spotify.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: {0}'.format(resp.message)

    session['oauth_token'] = (resp['access_token'], '')
    me = spotify.get('/me')
    return 'Logged in as id={0} name={1} redirect={2}'.format(
        me.data['id'],
        me.data['name'],
        request.args.get('next')
    )


@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
	app.run()