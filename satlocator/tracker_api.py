# -*- coding: utf-8 -*-
""" API for Tracker service.

    Requires:

    gevent (optional)
        sudo aptitude install gevent

    gunicorn
        sudo aptitude install gunicorn

    Usage:
        gunicorn --workers 2 --log-level INFO tracker_api:app
        gunicorn --workers 2 --log-level INFO --worker-class gevent --bind 127.0.0.1:8002 tracker_api:app
        gunicorn --workers 2 --daemon --log-level INFO --worker-class gevent --bind 127.0.0.1:8002 tracker_api:app

    Help:
        gunicorn --help
"""
import bottle
from bottle import route, error, post, get, run, abort, redirect, response, request, template


@get('/hello')
def hello():
    """ Being friendly.
    """
    return {"hello": "I am alive."}


@get('/admin')
def admin():
    return {"admin": "area"}  # needs proper template to render all functionality output


# post observer definition
@post('/observer/add/:name/:lat/:lon/:elevation')
def observer_define(name, lat, lon, elevation):
    """ Defines an observer point.
    """
    return {"": ""}


# post observer deletion
@post('/observer/remove/:name')
def observer_delete(name):
    """ Deletes an observer point.
    """
    return {"": ""}


# get observer list
@get('/observer/list')
def observer_get_list():
    """ Returns all registered observer points.
    """
    return {"": ""}


# post satellite definition
@post('/satellite/add/:name/:norad_id/:tle0/:tle1/:tle2')
def satellite_define(name, tle0, tle1, tle2):
    """ Defines an satellite.
    """
    return {"": ""}


# get satellite definition
@get('/satellite/get_tle/:norad_id')
def satellite_get_tle(norad_id):
    """ Gets the most recent TLE of the satellite.
    """
    return {"": ""}


# post satellite deletion
@post('/satellite/remove/:name')
def satellite_delete(name):
    """ Deletes an satellite.
    """
    return {"": ""}


# get satellite list
@get('/satellite/list')
def get_satellite_list():
    """ Returns all registered satellites.
    """
    return {"": ""}


# get slot availability
@get('/schedule/availability/:date_start/:date_end')
def get_schedule_slot_availability(date_start, date_end):
    """ Returns schedule slot availability
    """
    return {"": ""}


# post slot reservation
@post('/schedule/request/:date_start/:date_end/:observer/:satellite/:owner')
def schedule_request(name):
    """ Requests a schedule slot.
    """
    return {"": ""}


# post slot deletion
@post('/schedule/request/:date_start/:date_end/:observer/:satellite/:owner')
def schedule_delete(date_start, observer):
    """ Requests a schedule slot.
    """
    return {"": ""}


# get slot list
@get('/schedule/list')
def schedule_list():
    """
    """
    return {"": ""}


# get pinpoint
@get('/pinpoint')
def pinpoint():
    """
    """
    return {"": ""}


# get visibility windows
@get('/window/list/:observer/:satellite/:date_start/:date_end')
def get_windows(observer, satellite, date_start=None, date_end=None):
    """ Returns a list of all visibility windows of given satellite from given observer.
    """
    return {"": ""}


# post track  # will need some bottle magic!
@post('/track/:observer/:satellite')
def track(observer, satellite):
    """ Requests to start tracking satellite.
    """
    return {"": ""}


# post current observer
@post('/current/observer/:observer')
def current_observer_set(observer):
    """ Sets observer to be loaded in application.
    """
    return {"": ""}


# get current observer
@get('/current/observer')
def current_observer_get():
    """ Returns observer currently loaded in application.
    """
    return {"": ""}


# post current satellite
@post('/current/satellite/:satellite')
def current_satellite_set(observer):
    """ Sets satellite to be loaded in application.
    """
    return {"": ""}


# get current satellite
@get('/current/satellite')
def current_satellite_get():
    """ Returns satellite currently loaded in application.
    """
    return {"": ""}


if __name__ == "__main__":
    run(host='localhost', port=8080)

app = bottle.default_app()