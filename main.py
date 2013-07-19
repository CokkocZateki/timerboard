from backend import Timer, db
from flask import Flask, render_template, redirect, request, abort, url_for
import datetime, pytz
import json, re

app = Flask(__name__)

@app.route('/')
def timerboard():
	timers = Timer.query.order_by(Timer.time).all()
	return render_template('timers.html', timers=timers)

systemlist = []
with open("systems.json", "r") as systemsfile:
	systemlist = json.loads(systemsfile.read())

@app.route('/systems')
def systems():
	term = request.args.get('term')
	results = filter(lambda x:x.lower().startswith(term.lower()), systemlist)
	return json.dumps(results)

@app.route('/add_timer', methods=['POST',])
def add_timer():
	try:
		results = map(lambda x:request.form[x], ["system", "planet", "moon", "owner", "time", "notes"])
		if results[4]:
			results[4] = datetime.datetime.strptime(results[4], '%m/%d/%Y %H:%M')
		if ("reltime" in request.form) and request.form["reltime"]:
			reltime = request.form["reltime"].lower()
			kwargs = {
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
			results[4] = datetime.datetime.utcnow() + datetime.timedelta(**kwargs)
		t = Timer(*results)
		db.session.add(t)
		db.session.commit()
		return redirect(url_for('timerboard'))
	except Exception as e:
		print e
		abort(500)

@app.route('/delete/<id>', methods=['GET',])
def delete(id):
	r = Timer.query.filter(Timer.id == id).first_or_404()
	db.session.delete(r)
	db.session.commit()
	return redirect(url_for('timerboard'))

@app.teardown_appcontext
def shutdown_session(exception=None):
	db.session.remove()
