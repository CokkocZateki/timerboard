from backend import Timer, db
from flask import Flask, render_template, redirect, request, abort, url_for
import datetime
import json, re
import arrow
from authtools import *

app = Flask(__name__)

with open('config.json', 'r') as fh:
	config = json.loads(fh.read())["timerboard"]

regionmap = {}
with open("system2region.csv", "r") as regionfile:
	for line in regionfile:
		k,v = line.split(",")
		regionmap[k]=v.strip()

@app.route('/admin')
@requires_auth
def admin():
	timers = Timer.query.order_by(Timer.time).all()
	return render_template('timers.html', timers=timers, title=config["title"])

def prettyfy(timer):
	if timer["moon"] == 0:
		timer["moon"] = "-"
	if timer["planet"] == "":
		timer["planet"] == "-"
	return timer

@app.route("/api/timers")
def api_timers():
	timers = Timer.query.order_by(Timer.time).filter(Timer.time > arrow.utcnow().replace(hours=-2).naive)
	timers = map(lambda x:x.to_dict(), timers)
	for timer in timers:
		timer["region"] = regionmap[timer["system"]]
	timers = map(prettyfy, timers)
	timers = map(json.dumps, timers)
	return "["+",".join(timers)+"]"

@app.route('/')
def timerboard():
	return render_template('timers_guest.html', title=config["title"])

systemlist = []
with open("systems.json", "r") as systemsfile:
	systemlist = json.loads(systemsfile.read())
@app.route('/systems')
@requires_auth
def systems():
	term = request.args.get('term')
	results = filter(lambda x:x.lower().startswith(term.lower()), systemlist)
	return json.dumps(results)

@app.route('/add_timer', methods=['POST',])
@requires_auth
def add_timer():
	try:
		results = map(lambda x:request.form[x], ["system", "planet", "moon", "owner", "time", "notes"])
		if results[4]:
			results[4] = datetime.datetime.strptime(results[4], '%m/%d/%Y %H:%M')
		if ("reltime" in request.form) and request.form["reltime"]:
			reltime = request.form["reltime"].lower()
			kwargs = {
					"days": "(\d+)d",
					"hours": "(\d+)h",
					"minutes": "(\d+)m",
					"seconds": "(\d+)s"
				}
			for key, value in kwargs.items():
				kwargs[key] = re.search(value, reltime)
				if kwargs[key]:
					kwargs[key] = int(kwargs[key].groups()[0])
				else:
					del kwargs[key]
			results[4] = datetime.datetime.now() + datetime.timedelta(**kwargs)
		t = Timer(*results)
		db.session.add(t)
		db.session.commit()
		return redirect(url_for('admin'))
	except Exception as e:
		print e
		abort(500)

@app.route('/delete/<id>', methods=['GET',])
@requires_auth
def delete(id):
	r = Timer.query.filter(Timer.id == id).first_or_404()
	db.session.delete(r)
	db.session.commit()
	return redirect(url_for('admin'))

@app.teardown_appcontext
def shutdown_session(exception=None):
	db.session.remove()
