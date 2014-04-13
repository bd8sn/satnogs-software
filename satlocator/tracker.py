# -*- coding: utf-8 -*-
import ephem
from datetime import datetime
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
        self.satellites['friendly_name'] = sat_ephem
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

    def pinpoint(self, station_name, satellite_name, time=datetime.now()):
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

        station.date = time.strftime("%Y-%m-%d %H:%M:%S.%f")
        satellite.compute(station)
        return {'alt:': satellite.alt, 'az:': satellite.az, 'ok': True}

    def calculate_windows(self, station_name, satellite_name, time_start=None, time_stop=None):
        """ Calculates windows of visibility of a satellite from an observation point.
        """
        pass

    def calculate_all_windows(self, station_list, satellite_name, time_start=None, time_stop=None):
        """ Calculates all windows of visibility of a satellite from all provided observation points.
        """
        pass

    def calculate_all_windows_multi(self, station_list, satellite_list, time_start=None, time_stop=None):
        """ Calculates all windows of visibility of provided satellites from all provided observation points.
        """
        pass

