import requests
from random import getrandbits
from time import sleep
from flask import Response, Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_app import app, cache


apis = Blueprint('apis', __name__)

@apis.route('/api/joke', methods=['GET'])
def joke_api():
	format = request.args.get('format')
	joke = requests.get('https://v2.jokeapi.dev/joke/Any?lang=en&type=single&&format=json').json()

	if format == 'json':
		return jsonify(joke), 200

	return f'<h1>Joke API</h1>\n<p>{joke["joke"]}</p>', 200


def starify(value):
	return value.replace(' ', '*')

@apis.route('/api/bored', methods=['GET'])
def bored_api():
	format = request.args.get('format')
	res = requests.get('https://www.boredapi.com/api/activity',
		params=request.args,).json()

	if format == 'json':
		return jsonify(res), 200

	res["price"] = round(res["price"]*10)
	res["accessibility"] = round(res["accessibility"]*10)
	res["type"] = res["type"].capitalize()
	del res["key"]

	return render_template('bored.html', data=res), 200

