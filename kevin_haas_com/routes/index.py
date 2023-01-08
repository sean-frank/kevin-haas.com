import requests
from random import getrandbits
from time import sleep
from flask import Response, Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_from_directory
from kevin_haas_com import app, cache


def has_no_empty_params(rule):
	defaults = rule.defaults if rule.defaults is not None else ()
	arguments = rule.arguments if rule.arguments is not None else ()
	return len(defaults) >= len(arguments)


#base = Blueprint('base', __name__)

@app.route('/site-map')
#@cache.cached(timeout=15)
def site_map():
	links = []
	for rule in app.url_map.iter_rules():
		# Filter out rules we can't navigate to in a browser
		# and rules that require parameters
		if "GET" in rule.methods and has_no_empty_params(rule):
			url = url_for(rule.endpoint, **(rule.defaults or {}))
			links.append((url, rule.endpoint))
	# links is now a list of url, endpoint tuples
	return jsonify([ path for path, id in links ]), 200

@app.route('/', methods=['GET'])
#@cache.cached(timeout=15)
def index():
	return render_template('index.html'), 200

@app.route('/dashboard', methods=['GET'])
#@cache.cached(timeout=15)
def dashboard():
	return render_template('dashboard.html'), 200

@app.route('/sandbox', methods=['GET'])
#@cache.cached(timeout=15)
def sandbox():
	return render_template('sandbox.html'), 200

@app.route('/bored', methods=['GET'])
def bored():
	res = requests.get('https://www.boredapi.com/api/activity',
		params=request.args,)
	data = res.json()

	data["price_rating"] = round(data["price"]*10)
	data["accessibility_rating"] = round(data["accessibility"]*10)

	return render_template('fun/bored.html', data=data), 200

@app.route('/jokes', methods=['GET'])
@app.route('/jokes/<category>', methods=['GET'])
def jokes(category=None):
	params = {'lang': 'en', 'type': 'twopart', 'format': 'json'}
	if not category:
		category = 'Any'

	res = requests.get(f'https://v2.jokeapi.dev/joke/{category}', params=params)
	data = res.json()

	return render_template('fun/jokes.html', data=data), 200


