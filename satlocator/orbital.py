# -*- coding: utf-8 -*-
""" Functional implementation of required orbital tracking functionality.

Observer and satellite passed objects are both dictionaries.

Observer dict contains:
    lat
    lon
    elev

Satellite dict contains:
    tle0
    tle1
    tle2

"""

import ephem
from datetime import datetime, timedelta
import sys


def pinpoint(observer_dict, satellite_dict, timestamp=None):
    """ Provides azimuth and altitude of tracked object.

        Args:
            observer_dict: dictionary with details of observation point.
            satellite_dict: dictionary with details of satellite.
            time: timestamp we want to use for pinpointing the observed object.

        returns:
            Dictionary containing azimuth and altitude. Also contains "ok" for error detection.
    """
    # observer object
    if 'lat' in observer_dict and 'lon' in observer_dict and 'elev' in observer_dict:
        observer = ephem.Observer()
        observer.lon = str(observer_dict['lon'])
        observer.lat = str(observer_dict['lat'])
        observer.elevation = observer_dict['elev']
    else:
        return {'ok': False}

    # satellite object
    if 'tle0' in satellite_dict and 'tle1' in satellite_dict and 'tle2' in satellite_dict:
        tle0 = str(satellite_dict['tle0'])
        tle1 = str(satellite_dict['tle1'])
        tle2 = str(satellite_dict['tle2'])
        try:
            satellite = ephem.readtle(tle0, tle1, tle2)
        except ValueError:
            print(("error:", "ephem object", "tle values", sys.exc_info()[0]))
            return False
        except:
            print(("error:", "ephem object", sys.exc_info()[0]))
            return False
    else:
        return {'ok': False}

    # time of observation
    if timestamp is None:
        timestamp = datetime.now()

    # observation calculation
    observer.date = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    satellite.compute(observer)
    return {'alt': satellite.alt, 'az': satellite.az,
            'rng': satellite.range, 'rng_vlct': satellite.range_velocity,
            'ok': True}


def calculate_windows(observer_dict, satellite_dict, time_start=None, time_end=None):
    """ Calculates windows of visibility of a satellite from an observation point.

        Args:
            observer_dict: dictionary with details of observation point.
            satellite_dict: dictionary with details of satellite.
            time_start: datetime object denoting start of calculation period.
            time_end: datetime object denoting end of calculation period.

        Returns:
            Dictionary containing observation window periods.
    """
    # return object
    windows = {'ok': True, 'windows': []}

    # observer object
    if 'lat' in observer_dict and 'lon' in observer_dict and 'elev' in observer_dict:
        observer = ephem.Observer()
        observer.lon = str(observer_dict['lon'])
        observer.lat = str(observer_dict['lat'])
        observer.elevation = observer_dict['elev']
    else:
        return {'ok': False}

    # satellite object
    if 'tle0' in satellite_dict and 'tle1' in satellite_dict and 'tle2' in satellite_dict:
        tle0 = str(satellite_dict['tle0'])
        tle1 = str(satellite_dict['tle1'])
        tle2 = str(satellite_dict['tle2'])
        try:
            satellite = ephem.readtle(tle0, tle1, tle2)
        except ValueError:
            print(("error:", "ephem object", "tle values", sys.exc_info()[0]))
            return False
        except:
            print(("error:", "ephem object", sys.exc_info()[0]))
            return False
    else:
        return {'ok': False}

    # initialise window borders
    if time_start is None:
        time_start = datetime.now()
    if time_end is None:
        time_end = datetime.now() + timedelta(days=1)

    # calculate windows
    observer.date = time_start.strftime("%Y-%m-%d %H:%M:%S.%f")
    #i = 0  # remove
    while True:
        #i += 1  # remove
        satellite.compute(observer)
        window = observer.next_pass(satellite)
        # Weird bug in ephem library's next_pass function
        # returns set time earlier than rise time, leads to infinite loop
        if not _check_window_sanity(window):
            window_new = list(window)
            window_new[0] = window[4]  # replace 0 with 4
            window_new[1] = window[1]
            window_new[2] = window[2]
            window_new[3] = window[3]
            window_new[4] = window[0]  # replace 4 with 0
            window_new[5] = window[5]
            window = window_new
            # weird bug fix end.
        if ephem.Date(window[0]).datetime() < time_end:
            windows['windows'].append(
                {
                    'start': ephem.Date(window[0]).datetime().strftime("%Y-%m-%d %H:%M:%S.%f"),
                    'end': ephem.Date(window[4]).datetime().strftime("%Y-%m-%d %H:%M:%S.%f"),
                    'az_start': window[1]
                })
            if ephem.Date(window[4]).datetime() > time_end:
                # window end outside of window bounds; break
                break
            else:
                #if i > 100:  # remove
                    #break  # remove
                time_start_new = ephem.Date(window[4]).datetime() + timedelta(seconds=1)
                observer.date = time_start_new.strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            # window start outside of window bounds
            break
    return windows


def _check_window_sanity(window):
    """ Helps with detecting weird pyephem next_pass() results, where the set is before rise.
    """
    if ephem.Date(window[0]).datetime() > ephem.Date(window[4]).datetime():
        # print(window)
        return False
    return True
