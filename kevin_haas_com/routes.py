import requests
from random import getrandbits
from time import sleep
from flask import Response, render_template, redirect, url_for, request, flash, jsonify
from flask_app import app, cache

from flask_app.auth import auth
from flask_app.index import base
from flask_app.tests import tests
from flask_app.apis import apis

app.register_blueprint(auth)
app.register_blueprint(base)
app.register_blueprint(tests)
app.register_blueprint(apis)

