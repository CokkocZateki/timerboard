from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3://'
db = SQLAlchemy(app)
db.create_all()


class Timer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	system = db.Column(db.String(12))
	planet = db.Column(db.String(6))
	moon = db.Column(db.Integer)
	owner = db.Column(db.String(12))
	time = db.Column(db.DateTime)
	notes = db.Column(db.String(240))

	def __init__(self, system, planet, moon, owner, time, notes):
		self.system = system
		self.planet = planet
		self.moon = moon
		self.owner = owner
		self.time = time
		self.notes = notes

	def __repr__(self):
		return '<Timer %r>' % self.time

	def to_unix_time(self):
		return time.mktime(self.time.timetuple())
