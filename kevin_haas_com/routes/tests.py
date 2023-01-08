import requests
from random import getrandbits
from time import sleep
from flask import Response, Blueprint, render_template, redirect, url_for, request, flash, jsonify
from kevin_haas_com import app, cache


#tests = Blueprint('tests', __name__)

# Simulate a redirect
@app.route('/tests/redirect', methods=['GET'])
def redirect():
	return redirect("http://www.example.com", code=302)

# Simulate Infinite Redirections
@app.route('/tests/inf_redirects', methods=['GET'])
def inf_redirect():
	try:
		return redirect(request.path), 302
	except Exception as e:
		return str(e)

# Simulate User Agent Restrictions
@app.route('/tests/strict_agent', methods=['GET'])
def strict_agent():
	#agent = request.headers.get('User-Agent')
	browser = request.user_agent.string.lower()
	if 'firefox' in browser:
		return "Validated User Agent", 200
	else:
		return "Unauthorized User Agent", 403


