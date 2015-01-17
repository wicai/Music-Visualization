import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
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

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()