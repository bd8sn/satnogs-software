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
                d['results'].append({'name': r[0], 'norad_id': r[1],
                                    'tle0': r[2], 'tle1': r[3], 'tle2': r[4]})
        elif 'schedule' == result_type:
            for r in result:
                d['results'].append({'date_start': r[0], 'date_end': r[1],
                                    'observer': r[2], 'satellite': r[3], 'owner': r[4]})
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
    return True


def get_observer(observer_name):
    """ Retrieves an observer by name.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM observer WHERE name=?", (observer_name,))
    rows = c.fetchall()
    return _list2dict('observer', rows)


def del_observer(observer_name):
    """ Removes an observer by name.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM observer WHERE name=?", (observer_name,))
    rows = c.fetchall()
    if rows != ():
        c.execute("DELETE FROM observer WHERE name=?", (observer_name,))
        return {'ok': True}
    else:
        return {'error': 'not found'}


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
    return {'ok': True}


def get_satellite(satellite_name):
    """ Retrieves a satellite.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM satellite WHERE name=?", (satellite_name,))
    rows = c.fetchall()
    return _list2dict('satellite', rows)


def del_satellite(satellite_name):
    """ Removes an observer by name.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM satellite WHERE name=?", (satellite_name,))
    rows = c.fetchall()
    if rows != ():
        c.execute("DELETE FROM satellite WHERE name=?", (satellite_name,))
        return {'ok': True}
    else:
        return {'error': 'not found'}


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
    #(date text, observer text, satellite text, owner text)
    date_start = slot['date_start']
    date_end = slot['date_end']
    observer = slot['observer']
    satellite = slot['satellite']
    if 'owner' not in slot:
        slot['owner'] = 'me'
    owner = slot['owner']
    # create entry
    entry = (date_start, date_end, observer, satellite, owner)
    c = _cursor()
    c.execute('INSERT INTO schedule VALUES (?,?,?,?,?)', entry)  # TODO: add try/except
    return True


def del_schedule_slot(date_start):
    """ Deletes a schedule reservation.
    """
    if get_schedule_slot(date_start) is not []:
        c = _cursor()
        c.execute("DELETE FROM schedule where date_start=?", (date_start,))
        return True
    else:
        return False


def check_schedule_slot_availability(date_start, date_end):
    """ Checks whether a schedule slot is available for reservation.
    """
    c = _cursor()
    # TODO: NEEDS PROPER LIMIT CHECKING (will do in upcoming commit)
    c.execute("SELECT * FROM schedule where date_start>? and date_end<?", (date_start, date_end))
    rows = c.fetchall()
    if rows == []:
        return True
    else:
        return False


def get_schedule_slot(date_start):
    """ Retrieves specified schedule slot, if it exists.
    """
    c = _cursor()
    c.execute("SELECT * FROM schedule where date_start=?", (date_start,))
    rows = c.fetchall()
    return _list2dict('schedule', rows)


def get_schedule_list():
    """ Retrieves full schedule list.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM schedule")
    rows = c.fetchall()
    return _list2dict('schedule', rows)


def get_schedule_list_by_owner(owner):
    """ Retrieves full schedule list.
    """
    c = _cursor()  # with _cursor() as c:
    c.execute("SELECT * FROM schedule where owner=?", (owner,))
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


def _get_db_schema():
    c = _cursor()  # with _cursor() as c:
    c.execute(cfg.SQLITE_SCHEMA_SCHEMA)
    rows = c.fetchall()
    return rows
