# Timerboard

A simple EVE online timer board.

## Requirements

Please install the following with pip:

* Flask
* Flask-Sqlalchemy

## Configuration

Configuration is done via a config.json file in the web application's root folder, here's a sample one:

```
{
	"timerboard":{
		"title": "MYALLIANCE timerboard",
		"database":
		{
			"username": "timerboard",
			"password": "",
			"host": "localhost",
			"database": "timerboard"
		}
	},
}
```

## Installation

### Database

A schema.sql may be provided as a fallback, but the main way to create the database is as follows:

#### Create the database and user
As the root MySQL user:
```
CREATE DATABASE yourdatabasename;
GRANT ALL PRIVILEGES ON yourdatabasename.* TO 'youruser'@'host';
FLUSH PRIVILEGES;
```
#### Put credentials in the config.json

#### Create tables
In the timerboard folder:
```
python
>>> import backend
>>> backend.db.create_all()
EOF
```

### Debug Mode

```
python run.py
```

The application can be run in debug mode using the run.py script, this allows you to check that everything is working and view errors on the command line, it will also switch the application into debug mode, showing errors within the web browser when they occur. This is not the recommended mode of operation.

### Deploying under uwsgi

To deploy the application as a wsgi container you can use the following uwsgi settings. These may be adapted for other wsgi-capable application servers.

```
[uwsgi]
socket = /var/run/timerboard.sock
chmod-socket = 666
processes = 4
master = true
chdir = /opt/timerboard
pp = /opt/timerboard
module = main
callable = app
```

This can be served using an nginx site configuration like the following:

```
server {
        server_name timers.yourdomain.net;

        root /var/www/;

        location / {
                include         uwsgi_params;
                uwsgi_pass      unix:/var/run/timerboard.sock;
        }
}
```

## Usage

Normal users can go to [http://yourhost/](http://yourhost/) to see the timerboard.

Administrators can go to [http://yourhost/admin](http://yourhost/admin) to create or delete timers using credentials from the linked pizza-auth system.
