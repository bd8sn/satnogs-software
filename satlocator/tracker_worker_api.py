# -*- coding: utf-8 -*-
""" API for Tracker service.

    Requires:

    gevent (optional)
        sudo aptitude install gevent

    gunicorn
        sudo aptitude install gunicorn

    Usage:
        gunicorn --workers 1 --log-level INFO tracker_api:app
        gunicorn --workers 1 --log-level INFO --worker-class gevent --bind 127.0.0.1:8004 tracker_api:app
        gunicorn --workers 1 --daemon --log-level INFO --worker-class gevent --bind 127.0.0.1:8004 tracker_api:app

    Help:
        gunicorn --help
"""
import bottle

import orbital


class WorkerApp(object):
    def __init__(self):
        pass

    def track(self, observer, satellite):

        return("I'm 1 | self.param = %s" % self.param)

    def track_stop(self):
        return("Tracking stopped.")

myapp = WorkerApp()
bottle.route("/track/:observer/:satellite")(myapp.track)
bottle.route("/track_stop")(myapp.track_stop)
