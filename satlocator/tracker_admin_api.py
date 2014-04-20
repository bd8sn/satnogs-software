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
from bottle import route, run  # , error, post, get, abort, redirect, response, request, template
import dataio
import spacetrack
import orbital
import requests
from tracker_config import SPACETRACK_USERNAME
from tracker_config import SPACETRACK_PASSWORD
from tracker_config import TRACKER_WORKER_API_IP
from tracker_config import TRACKER_WORKER_API_PORT


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
def satellite_define_with_TLE(name, norad_id, tle0, tle1, tle2):
    """ Defines an satellite.
    """
    satellite = {'name': name, 'norad_id': norad_id,
                'tle0': tle0, 'tle1': tle1, 'tle2': tle2}
    result = dataio.set_satellite(satellite)
    if result['ok']:
        return result
    else:
        return result['error']


# request an update of specified satellite TLE info from SpaceTrack
@route('/satellite/update_tle/:name')
def satellite_update_TLE(name):
    """ Updates satellite TLE.
    """
    sat_def = satellite_get(name)
    if not sat_def['ok']:
        return {'error': 'not found'}
    else:
        norad_id = sat_def['results'][0]['norad_id']
        tle = satellite_get_tle(norad_id)
        satellite = {'name': name, 'norad_id': norad_id,
                    'tle0': tle['tle0'], 'tle1': tle['tle1'], 'tle2': tle['tle2']}
        result = dataio.set_satellite(satellite)
        if result['ok']:
            return result
        else:
            return result['error']


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
def schedule_request(date_start, date_end, observer, satellite, owner):
    """ Requests a schedule slot.
    """
    slot = {'date_start': date_start, 'date_end': date_end, 'observer': observer,
            'satellite': satellite, 'owner': owner}
    result = dataio.set_schedule_slot(slot)
    if result['ok']:
        return result
    else:
        return result['error']


# post slot deletion
@route('/schedule/remove/:date_start/:date_end/:observer/:satellite/:owner')
def schedule_delete(date_start, observer, owner):
    """ Requests a schedule slot.
    """
#    slot = {'date_start': date_start, 'observer': observer, 'owner': owner}
#    result = dataio.set_schedule_slot(slot)
#    if result['ok']:
#        return result
#    else:
#        return result['error']
    return {'error': 'not implemented yet.'}


# get slot list
@route('/schedule/list')
def schedule_list():
    """
    """
    result = dataio.get_schedule_list()
    if result['ok']:
        return result
    else:
        return result['error']


# get pinpoint for given observer and satellite
@route('/pinpoint/:observer_name/:satellite_name')
def pinpoint(observer_name, satellite_name):
    """ Returns azimuth and altitude of satellite from observer.

        Only names are provided as params,
        they are subsequently searched in their respectable lists.
    """
    o_result = dataio.observer_get(observer_name)
    if o_result['ok']:
        o = o_result['results'][0]
    else:
        return {'error': 'observer not found'}

    s_result = dataio.satellite_get(satellite_name)
    if o_result['ok']:
        s = s_result['results'][0]
    else:
        return {'error': 'satellite not found'}

    result = orbital.pinpoint(o, s)
    return result


# get pinpoint for current observer and satellite
@route('/pinpoint/current')
def pinpoint_current():
    """ Returns azimuth and altitude of currently selected satellite
        from currently selected observer.
    """
    observer_name = current_observer_get()
    satellite_name = current_satellite_get()
    return pinpoint(observer_name, satellite_name)


# get visibility windows
@route('/window/list/:observer_name/:satellite_name/:date_start/:date_end')
def get_windows(observer_name, satellite_name, date_start=None, date_end=None):
    """ Returns a list of all visibility windows of given satellite from given observer.
    """
    # TODO: check if they exist
    observer = observer_get(observer_name)
    satellite = satellite_get(satellite_name)
    # calculate windows
    res = orbital.calculate_windows(observer, satellite, date_start, date_end)
    return res


# post track directive to tracker worker api
@route('/track/:observer_name/:satellite_name')
def track(observer_name, satellite_name):
    """ Requests satellite tracking initiation.

        Tracking request is handled by the tracker worker api.
    """
    # TODO: check if they exist
    observer = observer_get(observer_name)
    satellite = satellite_get(satellite_name)
    url = 'http://' + TRACKER_WORKER_API_IP + ':' + TRACKER_WORKER_API_PORT + '/'
    url += str(observer) + '/' + str(satellite)
    print url  # debug
    r = requests.get(url)
    return r.text


# post track directive to tracker worker api
@route('/track/stop')
def track_stop():
    url = 'http://' + TRACKER_WORKER_API_IP + ':' + TRACKER_WORKER_API_PORT + '/'
    url += 'track_stop'
    r = requests.get(url)
    return r.text


# post track directive to tracker worker api
@route('/track/current')
def track_current():
    """ Requests to stop satellite tracking.

        Tracking request is handled by track() and subsequently by the tracker worker api.
    """
    observer_name = current_observer_get()
    satellite_name = current_satellite_get()
    return track(observer_name, satellite_name)


# post current observer
@route('/current/observer/:observer')
def current_observer_set(observer):
    """ Sets observer to be loaded in application.
    """
    # TODO: Check if in list
    res = dataio.set_current_observer(observer)
    return res


# get current observer
@route('/current/observer')
def current_observer_get():
    """ Returns observer currently loaded in application.
    """
    res = dataio.get_current_observer()
    return res


# post current satellite
@route('/current/satellite/:satellite')
def current_satellite_set(satellite):
    """ Sets satellite to be loaded in application.
    """
    # TODO: Check if in list
    res = dataio.set_current_satellite(satellite)
    return res


# get current satellite
@route('/current/satellite')
def current_satellite_get():
    """ Returns satellite currently loaded in application.
    """
    res = dataio.get_current_satellite()
    return res

# this allows the module to be started without gunicorn, via bottle
if __name__ == "__main__":
    run(host='localhost', port=8000, reloader=True)

app = bottle.default_app()