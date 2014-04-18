# -*- coding: utf-8 -*-

""" Implements all functions defined in dataio.py.
    Contains all logic required to implement defined functionality.
"""
import sqlite3

# UGLY GLOBAL BLOCK
# TODO: Should be retrieved from config
SQLITE_DATABASE_NAME = 'satlocator.sqlite.db'  # ':memory:' for in-memory-only db

# TODO: Move this into an iterable structure (a dictionary perhaps?)
SQLITE_SCHEMA_OBSERVER = '''CREATE TABLE IF NOT EXISTS observer
                            (name text, latitude text, longitude text, elevation integer)'''
SQLITE_SCHEMA_SATELLITE = '''CREATE TABLE IF NOT EXISTS satellite
                            (name text, norad_id text, tle0 text, tle1 text, tle2 text)'''
SQLITE_SCHEMA_SCHEDULE = '''CREATE TABLE IF NOT EXISTS schedule
                            (date text, observer text, satellite text, owner text)'''
SQLITE_SCHEMA_SESSION = '''CREATE TABLE IF NOT EXISTS session
                            (parameter text, value text)'''


def _cursor():
    """ Provides a db cursor to use.
    """
    conn = sqlite3.connect(SQLITE_DATABASE_NAME)
    conn.isolation_level = None  # should be concious of this
    cursor = conn.cursor()
    #_define_schema(cursor)
    return cursor


def _define_schema(cursor=None):
    """ Defines db schema.
    """
    if not cursor:
        cursor = _cursor()
    cursor.execute(SQLITE_SCHEMA_OBSERVER)
    cursor.execute(SQLITE_SCHEMA_SATELLITE)
    cursor.execute(SQLITE_SCHEMA_SCHEDULE)
    cursor.execute(SQLITE_SCHEMA_SESSION)


def _verify_schema():
    """ Verifies db schema.
    (Editor's note:Not sure of this.)
    """
    pass


def set_observer(observer):
    """ Defines a new observer.
    """
    pass


def get_observer(observer_name):
    """ Retrieves an observer by name.
    """
    pass


def get_observer_list():
    """ Retrieves all observers.
    """
    pass


def set_satellite(satellite):
    """ Defines a new satellite.
    """
    pass


def get_satellite(satellite_name):
    """ Retrieves a satellite.
    """
    pass


def get_satellite_list():
    """ Retrieves all satellites.
    """
    pass


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
    pass


def get_next_schedule_slot():
    """ Retrieves nearest reservation.
    """
    pass


def set_current_observer(observer):
    """ Defines current observer.
    """
    pass


def get_current_observer():
    """ Retrieves current observer.
    """
    pass


def set_current_satellite(satellite):
    """ Defines current satellite.
    """
    pass


def get_current_satellite():
    """ Retrieves current satellite.
    """
    pass
