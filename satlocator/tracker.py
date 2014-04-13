# -*- coding: utf-8 -*-
import ephem
from datetime import datetime
import time


class tracker:
    """ Handles tracking of satellites and orbiting bodies from given geolocations.
    """

    stations = []
    satellites = []

    def __init__(self):
        pass

    def add_satellite(tle1, tle2, tle3, friendly_name=None):
        """ Adds a satellite to the tracker.
        """
        pass

    def add_satellite_from_tle(tle_dict, friendly_name=None):
        """ Adds a satellite to the tracker.
        """
        pass

    def remove_satellite(friendly_name):
        """ Removes a satellite from the tracker.
        """
        pass

    def add_station(name, ):
        """ Adds a station or objervation point to the tracker.
        """
        pass

    def remove_station():
        """ Removes a satellite from the tracker.
        """
        pass

    def pinpoint(station_name, satellite_name, time=None):
        """ Provides azimuth and altitude of tracked object.
        """
        pass

    def calculate_windows(station_name, satellite_name, time_start=None, time_stop=None):
        """ Calculates windows of visibility of a satellite from an observation point.
        """
        pass

    def calculate_all_windows(station_list, satellite_name, time_start=None, time_stop=None):
        """ Calculates all windows of visibility of a satellite from all provided observation points.
        """
        pass

    def calculate_all_windows_multi(station_list, satellite_list, time_start=None, time_stop=None):
        """ Calculates all windows of visibility of provided satellites from all provided observation points.
        """
        pass

