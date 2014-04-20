# -*- coding: utf-8 -*-
""" API for Tracker service.

    Requires:

    gevent (optional)
        sudo aptitude install gevent

    gunicorn
        sudo aptitude install gunicorn

    Usage:
        gunicorn --workers 1 --log-level INFO tracker_api:app
        gunicorn --workers 1 --log-level INFO --worker-class gevent --bind 127.0.0.1:8002 tracker_api:app
        gunicorn --workers 1 --daemon --log-level INFO --worker-class gevent --bind 127.0.0.1:8002 tracker_api:app

    Help:
        gunicorn --help

    Can also be called directly from python, using bottle:
        python tracker_worker_api.py
"""
import bottle
from bottle import run
import tracker_worker


class WorkerApp(object):

    tracker = None

    def __init__(self):
        self.tracker = tracker_worker.TrackerWorker()

    # route "/track/:observer_dict/:satellite_dict"
    def track(self, observer_dict, satellite_dict):
        """ Initiates tracking of designated satellite from designated observer.

            Can also be called to change the desired observation, without stopping.

            NOTE: Dictionaries need to be double quoted!!! Use "", not ''.
        """
        self.tracker.trackobject(observer_dict, satellite_dict)
        if not self.tracker.isalive():
            self.tracker.trackstart()
        return({"action": "tracking started"})

    # route "/track/stop"
    def track_stop(self):
        """ Stop tracking.
        """
        self.tracker.trackstop()
        return({"action": "tracking stopped"})

# instanciation of application
app = WorkerApp()
# route designation (needs to be done outside of class)
bottle.route("/track/:observer_dict/:satellite_dict")(app.track)
bottle.route("/track/stop")(app.track_stop)

# this allows the module to be started (via bottle) directly from python
if __name__ == "__main__":
    run(host='localhost', port=8002, reloader=True)
