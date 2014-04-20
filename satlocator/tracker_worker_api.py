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

import tracker_worker


class WorkerApp(object):

    tracker = None

    def __init__(self):
        self.tracker = tracker_worker.TrackerWorker()

    def track(self, observer_dict, satellite_dict):
        self.tracker.trackobject(observer_dict, satellite_dict)
        if not self.tracker.isalive:
            self.tracker.trackstart()
        return("Tracking.")

    def track_stop(self):
        self.tracker.trackstop()
        return("Tracking stopped.")

myapp = WorkerApp()
bottle.route("/track/:observer_dict/:satellite_dict")(myapp.track)
bottle.route("/track_stop")(myapp.track_stop)
