# -*- coding: utf-8 -*-

""" Implements all functions defined in dataio.py.
    Contains all logic required to implement defined functionality.
"""
import sqlite3

import tracker_config as cfg


def _cursor():
    """ Provides a db cursor to use.
    """
    conn = sqlite3.connect(cfg.SQLITE_DATABASE_NAME)
    conn.isolation_level = None  # should be concious of this
    cursor = conn.cursor()
    #_define_schema(cursor)
    return cursor


def _define_schema(cursor=None):
    """ Defines db schema.
    """
    if not cursor:
        cursor = _cursor()
    cursor.execute(cfg.SQLITE_SCHEMA_OBSERVER)
    cursor.execute(cfg.SQLITE_SCHEMA_SATELLITE)
    cursor.execute(cfg.SQLITE_SCHEMA_SCHEDULE)
    cursor.execute(cfg.SQLITE_SCHEMA_SESSION)


def _verify_schema():
    """ Verifies db schema.
    (Editor's note:Not sure of this.)
    """
    pass


def _list2dict(result_type, result):
    """ Transforms results from known app tables returned from sqlite into dictionaries.
    """
    if not result_type or not result:
        return None
    else:
        d = {'results': [], 'ok': True}
        if 'observer' == result_type:
            for r in result:
                d['results'].append({'name': r[0], 'lat': r[1], 'lon': r[2], 'elev': r[3]})
        elif 'satellite' == result_type:
            for r in result:
                d['results'].append({'name': r[0], 'norad_id': r[1], 'tle0': r[2], 'tle1': r[3], 'tle2': r[4]})
        elif 'schedule' == result_type:
            pass
        else:
            d['ok'] = False
    return d


def set_observer(observer):
    """ Defines a new observer.
    """
    # TODO: Add checks
    name = observer['name']
    lat = observer['lat']
    lon = observer['lon']
    elev = observer['elev']
    # create entry
    entry = (name, lat, lon, elev)
    c = _cursor()
    c.execute('INSERT INTO observer VALUES (?,?,?,?)', entry)  # TODO: add try/except


def get_observer(observer_name):
    """ Retrieves an observer by name.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM observer WHERE name=?", (observer_name,))
    rows = c.fetchall()
    return _list2dict('observer', rows)


def get_observer_list():
    """ Retrieves all observers.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM observer")
    rows = c.fetchall()
    return _list2dict('observer', rows)


def set_satellite(satellite):
    """ Defines a new satellite.
    """
    # TODO: Add checks
    name = satellite['name']
    norad_id = satellite['norad_id']
    tle0 = satellite['tle0']
    tle1 = satellite['tle1']
    tle2 = satellite['tle2']
    # create entry
    entry = (name, norad_id, tle0, tle1, tle2)
    c = _cursor()
    c.execute('INSERT INTO satellite VALUES (?,?,?,?,?)', entry)  # TODO: add try/except


def get_satellite(satellite_name):
    """ Retrieves a satellite.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM satellite WHERE name=?", (satellite_name,))
    rows = c.fetchall()
    return _list2dict('satellite', rows)


def get_satellite_list():
    """ Retrieves all satellites.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM satellite")
    rows = c.fetchall()
    return _list2dict('satellite', rows)


def set_schedule_slot(slot):
    """ Reserves a schedule slot.
    """
    pass


def del_schedule_slot(slot):
    """ Deletes a schedule reservation.
    """
    pass


# does this function move (too much) logic into the db?
def check_schedule_slot_availability(slot):
    """ Checks whether a schedule slot is available for reservation.
    """
    pass


def get_schedule_list():
    """ Retrieves schedule.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM schedule")
    rows = c.fetchall()
    return _list2dict('schedule', rows)


def get_next_schedule_slot():
    """ Retrieves nearest reservation.
    """
    pass
#    c = _cursor()  # with _cursor() as c:
#    c.execute("SELECT * FROM schedule")
#    rows = c.fetchall()
#    return _list2dict('schedule', rows)


def set_current_observer(observer_name):
    """ Defines current observer.
    """
    c = _cursor()  # with _cursor() as c:
    if get_current_observer() != []:
        c.execute('DELETE FROM session where parameter=?', ('current_observer',))
    c.execute('INSERT INTO session VALUES (?,?)', ('current_observer', observer_name))


def get_current_observer():
    """ Retrieves current observer.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT value FROM session WHERE parameter=?", ('current_observer',))
    rows = c.fetchall()
    return rows[0][0]


def set_current_satellite(satellite_name):
    """ Defines current satellite.
    """
    c = _cursor()  # with _cursor() as c:
    if get_current_observer() != []:
        c.execute('DELETE FROM session where parameter=?', ('current_satellite',))
    c.execute('INSERT INTO session VALUES (?,?)', ('current_satellite', satellite_name))


def get_current_satellite():
    """ Retrieves current satellite.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT parameter, value FROM session WHERE param=?", ('current_satellite',))
    rows = c.fetchall()
    return rows[0][0]
