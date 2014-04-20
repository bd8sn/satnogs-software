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
import dataio
import spacetrack
from tracker_config import SPACETRACK_USERNAME
from tracker_config import SPACETRACK_PASSWORD


@route('/hello')
def hello():
    """ Being friendly.
    """
    return {"hello": "I am alive."}


@route('/admin')
def admin():
    return {"admin": "area"}  # needs proper template to render all functionality output


# post observer definition
@route('/observer/add/:name/:lat/:lon/:elevation')
def observer_define(name, lat, lon, elevation):
    """ Defines an observer point.
    """
    observer = {'name': name, 'lat': lat, 'lon': lon, 'elev': elevation}
    result = dataio.set_observer(observer)
    return {"done": result}


# get observer definition
@route('/observer/show/:name')
def observer_get(name):
    """ Returns an observer point definition.
    """
    result = dataio.get_observer(name)
    if result['ok']:
        return result
    else:
        return result['error']


# post observer deletion
@route('/observer/remove/:name')
def observer_delete(name):
    """ Deletes an observer point.
    """
    result = dataio.del_observer(name)
    if result['ok']:
        return result
    else:
        return result['error']


# get observer list
@route('/observer/list')
def observer_get_list():
    """ Returns all registered observer points.
    """
    result = dataio.get_observer_list()
    if result['ok']:
        return result
    else:
        return result['error']


# get satellite TLE and full info from SpaceTrack
@route('/satellite/get_full_tle_for/:norad_id')
def satellite_get_full_tle(norad_id):
    """ Gets the most recent TLE of the satellite.
    """
    credentials = {'identity': SPACETRACK_USERNAME, 'password': SPACETRACK_PASSWORD}
    sresponse = spacetrack.request_sequence(credentials, norad_id)
    return sresponse[0]


# get satellite TLE info from SpaceTrack
@route('/satellite/get_tle_for/:norad_id')
def satellite_get_tle(norad_id):
    """ Gets the most recent TLE of the satellite.
    """
    credentials = {'identity': SPACETRACK_USERNAME, 'password': SPACETRACK_PASSWORD}
    sresponse = spacetrack.request_sequence(credentials, norad_id)
    tle = {'tle0': sresponse[0]['TLE_LINE0'],
            'tle1': sresponse[0]['TLE_LINE1'],
            'tle2': sresponse[0]['TLE_LINE2']}
    return tle


# post satellite definition, without TLE info
@route('/satellite/add/:name/:norad_id')
def satellite_define(name, norad_id):
    """ Defines an satellite. TLE info is retrieved from SpaceTrack.
    """
    tle = satellite_get_tle(norad_id)
    satellite = {'name': name, 'norad_id': norad_id,
                'tle0': tle['tle0'], 'tle1': tle['tle1'], 'tle2': tle['tle2']}
    result = dataio.set_satellite(satellite)
    if result['ok']:
        return result
    else:
        return result['error']


# post satellite definition, with TLE info
@route('/satellite/add_with_tle/:name/:norad_id/:tle0/:tle1/:tle2')
def satellite_define_with_TLE(name, tle0, tle1, tle2):
    """ Defines an satellite.
    """
    return {'error': 'not implemented yet.'}


# request an update of specified satellite TLE info from SpaceTrack
@route('/satellite/update_tle/:name')
def satellite_update_TLE(name):
    """ Updates satellite TLE.
    """
    return {'error': 'not implemented yet.'}


# post satellite deletion
@route('/satellite/remove/:name')
def satellite_delete(name):
    """ Deletes an satellite.
    """
    result = dataio.del_satellite(name)
    if result['ok']:
        return result
    else:
        return result['error']


# get satellite definition
@route('/satellite/show/:name')
def satellite_get(name):
    """ Returns an satellite definition.
    """
    result = dataio.get_satellite(name)
    if result['ok']:
        return result
    else:
        return result['error']


# get satellite list
@route('/satellite/list')
def get_satellite_list():
    """ Returns all registered satellites.
    """
    result = dataio.get_satellite_list()
    if result['ok']:
        return result
    else:
        return result['error']


# get slot availability
@route('/schedule/availability/:date_start/:date_end')
def get_schedule_slot_availability(date_start, date_end):
    """ Returns schedule slot availability
    """
    return {'error': 'not implemented yet.'}


# post slot reservation
@route('/schedule/request/:date_start/:date_end/:observer/:satellite/:owner')
def schedule_request(name):
    """ Requests a schedule slot.
    """
    return {'error': 'not implemented yet.'}


# post slot deletion
@route('/schedule/request/:date_start/:date_end/:observer/:satellite/:owner')
def schedule_delete(date_start, observer):
    """ Requests a schedule slot.
    """
    return {'error': 'not implemented yet.'}


# get slot list
@route('/schedule/list')
def schedule_list():
    """
    """
    return {'error': 'not implemented yet.'}


# get pinpoint
@route('/pinpoint')
def pinpoint():
    """
    """
    return {'error': 'not implemented yet.'}


# get visibility windows
@route('/window/list/:observer/:satellite/:date_start/:date_end')
def get_windows(observer, satellite, date_start=None, date_end=None):
    """ Returns a list of all visibility windows of given satellite from given observer.
    """
    return {'error': 'not implemented yet.'}


# post track directive to tracker worker api
@route('/track/:observer/:satellite')
def track(observer, satellite):
    """ Requests to start tracking satellite.
    """
    return {'error': 'not implemented yet.'}


# post current observer
@route('/current/observer/:observer')
def current_observer_set(observer):
    """ Sets observer to be loaded in application.
    """
    return {'error': 'not implemented yet.'}


# get current observer
@route('/current/observer')
def current_observer_get():
    """ Returns observer currently loaded in application.
    """
    return {'error': 'not implemented yet.'}


# post current satellite
@route('/current/satellite/:satellite')
def current_satellite_set(observer):
    """ Sets satellite to be loaded in application.
    """
    return {'error': 'not implemented yet.'}


# get current satellite
@route('/current/satellite')
def current_satellite_get():
    """ Returns satellite currently loaded in application.
    """
    return {'error': 'not implemented yet.'}


if __name__ == "__main__":
    run(host='localhost', port=8000, reloader=True)

app = bottle.default_app()