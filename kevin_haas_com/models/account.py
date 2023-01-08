from datetime import datetime, timedelta
from sqlalchemy.sql import func
from flask_login import UserMixin
from kevin_haas_com import db


class Account(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	email = db.Column(db.String(256), unique=True)
	username = db.Column(db.String(256), unique=True)
	password = db.Column(db.String(1024))
	creation_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())
	deleted_date = db.Column(db.DateTime(timezone=True))
	is_deleted = db.Column(db.Boolean, default=False)
	admin = db.Column(db.Boolean, default=False)

