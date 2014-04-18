# -*- coding: utf-8 -*-
import ephem
from datetime import datetime, timedelta
import time
import sys


class tracker:
    """ Handles tracking of satellites and orbiting bodies from given geolocations.
    """

    stations = {}
    satellites = {}

    def __init__(self):
        pass

    def add_satellite(self, tle1, tle2, tle3, friendly_name=None):
        """ Adds a satellite to the tracker.

            Args:
                tle1: line 1 of the TLE of the satellite.
                tle2: line 2 of the TLE of the satellite.
                tle3: line 3 of the TLE of the satellite.
                friendly_name: name to use for satellite within tracker.

            Returns:
                True if satellite added correctly.
                False if there was an error.

            If friendly_name is not given, line 1 of the TLE is used for it.
        """
        try:
            sat_ephem = ephem.readtle(tle1, tle2, tle3)
        except ValueError:
            print(("error:", "ephem object", "tle values", sys.exc_info()[0]))
            return False
        except:
            print(("error:", "ephem object", sys.exc_info()[0]))
            return False
        if friendly_name is None:
            friendly_name = tle1
        self.satellites['friendly_name'] = sat_ephem
        return True

    def add_satellite_from_tle(self, tle_dict, friendly_name=None):
        """ Adds a satellite to the tracker using a dictionary containing the TLE info.

            Args:
                tle_dict: line 1 of the TLE of the satellite.
                friendly_name: name to use for satellite within tracker.

            Returns:
                True if satellite added correctly.
                False if there was an error.

            If friendly_name is not given, line 1 of the TLE is used for it.
        """
        if 'TLE_LINE0' in tle_dict and 'TLE_LINE1' in tle_dict and 'TLE_LINE2' in tle_dict:
            tle1 = tle_dict['TLE_LINE0']
            tle2 = tle_dict['TLE_LINE1']
            tle3 = tle_dict['TLE_LINE2']
        else:
            return False

        try:
            sat_ephem = ephem.readtle(tle1, tle2, tle3)
        except ValueError:
            print(("error:", "ephem object", "tle values", sys.exc_info()[0]))
            return False
        except:
            print(("error:", "ephem object", sys.exc_info()[0]))
            return False
        if friendly_name is None:
            friendly_name = tle1
        self.satellites[friendly_name] = sat_ephem
        return True

    def remove_satellite(self, friendly_name):
        """ Removes a satellite from the tracker.

            Args:
                friendly_name: friendly name of observation point, provided upon creation.

            Returns:
                True if satellite added correctly.
                False if there was an error.
        """
        if friendly_name is not None and friendly_name in self.satellites:
            del self.satellites[friendly_name]
            return True
        else:
            return True

    def add_station(self, name, geolat, geolong, elevation=0):
        """ Adds a station or objervation point to the tracker.
            Args:
                name: name of observation point.
                geolat: geolocation latitude, in float format.
                geolong: geolocation longitude, in float format.
                elevation: geolocation elevation, in meters.

            Returns:
                True if satellite added correctly.
                False if there was an error.
        """
        if name and geolong and geolat and elevation:
            if isinstance(name, str) and isinstance(geolong, float) and isinstance(geolat, float):
                station = ephem.Observer()
                station.lon = str(geolong)
                station.lat = str(geolat)
                station.elevation = elevation
                self.stations[name] = station
                return True
        return False

    def remove_station(self, name):
        """ Removes a satellite from the tracker.

            Args:
                name: friendly name of observation point, provided upon creation.

            Returns:
                True if satellite added correctly.
                False if there was an error.
        """
        if name in self.stations:
            del self.stations[name]
            return True
        return False

    def pinpoint(self, station_name, satellite_name, timestamp=None):
        """ Provides azimuth and altitude of tracked object.

            Args:
                station_name: friendly name of observation point.
                satellite_name: friendly name of satellite.
                time: timestamp we want to use for pinpointing the observed object.

            returns:
                Dictionary containing azimuth and altitude. Also contains "ok" for error detection.
        """
        if station_name in self.stations and satellite_name in self.satellites:
            station = self.stations[station_name]
            satellite = self.satellites[satellite_name]
        else:
            return {'ok': False}

        if timestamp is None:
            timestamp = datetime.now()

        station.date = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
        satellite.compute(station)
        return {'alt': satellite.alt, 'az': satellite.az,
            'rng': satellite.range, 'rng_vlct': satellite.range_velocity,
            'ok': True}

    def calculate_windows(self, station_name, satellite_name, time_start=None, time_end=None):
        """ Calculates windows of visibility of a satellite from an observation point.

            Args:
                station_name: friendly name of station observation window will be calculated for.
                satellite_name: friendly name of satellite we wish to observe.
                time_start: datetime object denoting start of calculation period.
                time_end: datetime object denoting end of calculation period.

            Returns:
                Dictionary containing observation window periods.
        """
        # return object
        windows = {'ok': True, 'windows': []}

        # get objects
        if station_name in self.stations and satellite_name in self.satellites:
            station = self.stations[station_name]
            satellite = self.satellites[satellite_name]
        else:
            return {'ok': False}

        # initialise window borders
        if time_start is None:
            time_start = datetime.now()
        if time_end is None:
            time_end = datetime.now() + timedelta(days=1)

        # calculate windows
        station.date = time_start.strftime("%Y-%m-%d %H:%M:%S.%f")
        #i = 0  # remove
        while True:
            #i += 1  # remove
            satellite.compute(station)
            window = station.next_pass(satellite)
            # Weird bug in ephem library's next_pass function
            # returns set time earlier than rise time, leads to infinite loop
            if not self.check_window_sanity(window):
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
                        'start': ephem.Date(window[0]).datetime(),
                        'end': ephem.Date(window[4]).datetime(),
                        'az_start': window[1]
                    })
                if ephem.Date(window[4]).datetime() > time_end:
                    # window end outside of window bounds; break
                    break
                else:
                    #if i > 100:  # remove
                        #break  # remove
                    time_start_new = ephem.Date(window[4]).datetime() + timedelta(seconds=1)
                    station.date = time_start_new.strftime("%Y-%m-%d %H:%M:%S.%f")
            else:
                # window start outside of window bounds
                break
        return windows

    def check_window_sanity(self, window):
        if ephem.Date(window[0]).datetime() > ephem.Date(window[4]).datetime():
            print(window)
            return False
        return True

    def calculate_all_windows(self, station_list, satellite_name, time_start=None, time_end=None):
        """ Calculates all windows of visibility of a satellite from all provided observation points.

            Args:
                station_list: list of friendly names of stations observation window will be calculated for.
                satellite_name: friendly name of satellite we wish to observe.
                time_start: datetime object denoting start of calculation period.
                time_end: datetime object denoting end of calculation period.

            Returns:
                Dictionary containing observation window periods.
        """
        # return object
        result_multi = {'stations': [], 'ok': True}

        if satellite_name not in self.satellites:
            return {'ok': False, 'reason': 'satellite not found in tracker'}

        # get objects
        for station_name in station_list:
            if isinstance(station_name, str) and station_name in self.stations:
                result = self.calculate_windows(station_name, satellite_name)
                result['station'] = station_name
                result_multi['stations'].append(result)
            else:
                result_multi['stations'].append({'station': '', 'ok': False, 'reason': 'station not found in tracker'})
        return result_multi

    def calculate_all_windows_multi(self, station_list, satellite_list, time_start=None, time_end=None):
        """ Calculates all windows of visibility of provided satellites from all provided observation points.

            Args:
                station_list: list of friendly names of stations observation window will be calculated for.
                satellite_list: list of friendly names of satellites we wish to observe.
                time_start: datetime object denoting start of calculation period.
                time_end: datetime object denoting end of calculation period.

            Returns:
                Dictionary containing observation window periods.
        """
        pass
