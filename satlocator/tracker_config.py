# -*- coding: utf-8 -*-

"""DATAIO BLOCK"""
SQLITE_DATABASE_NAME = 'satlocator.sqlite.db'  # ':memory:' for in-memory-only db

# TODO: Move this into an iterable structure (a dictionary perhaps?)
SQLITE_SCHEMA_OBSERVER = '''CREATE TABLE IF NOT EXISTS observer
                            (name text, latitude DECIMAL(4,6), longitude DECIMAL(4,6), elevation integer)'''
SQLITE_SCHEMA_SATELLITE = '''CREATE TABLE IF NOT EXISTS satellite
                            (name text, norad_id text, tle0 text, tle1 text, tle2 text)'''
SQLITE_SCHEMA_SCHEDULE = '''CREATE TABLE IF NOT EXISTS schedule
                            (date_start text, date_end text, observer text, satellite text, owner text)'''
SQLITE_SCHEMA_SESSION = '''CREATE TABLE IF NOT EXISTS session
                            (parameter text, value text)'''
SQLITE_SCHEMA_SCHEMA = '''SELECT * FROM sqlite_master'''


TRACKING_RECEIVER_IP = ''
TRACKING_RECEIVER_PORT = 4533  # default rotctld port is 4533