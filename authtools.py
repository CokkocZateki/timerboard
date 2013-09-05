from functools import wraps
from flask import request, Response
import json
from auth.ldaptools import LDAPTools

with open('config.json', 'r') as fh:
	config = json.loads(fh.read())

ldaptools = LDAPTools(config)

def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""
	try:
		user = ldaptools.getuser(username)
		print user
		assert(user)
		print user.authGroup
		assert("timerboard" in user.authGroup)
		assert(ldaptools.check_credentials(username, password))
		return True
	except Exception as e:
		print e
		return False

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Services Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated
