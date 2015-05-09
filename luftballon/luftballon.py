#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import sys
import time
import threading
import json

try:
    import aprslib
except:
    sys.stdout.write('Please install dependencies: aprslib\n')
    exit(0)

import trackersocket


INTERESTING_CALLSIGNS = ['J43VHF-11']
OBSERVER = (38.0171, 23.7312, 61)
TCP_IP = '127.0.0.1'
TCP_PORT = 5005


def calculate_azimuth_elevation(pointA, pointB):
    """
    Calculates the azimouth(bearing) and elevation between two points.

    The formulae used for azimuth (or bearing) is the following:
    θ = atan2(sin(Δlong).cos(lat2),
    cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

    Args:
        `pointA: The tuple representing the latitude/longitude/height for the
            first point. Latitude and longitude must be in decimal degrees and height in meters
        pointB: The tuple representing the latitude/longitude/height for the
            second point. Latitude and longitude must be in decimal degrees and height in meters

    Returns:
        The azimuth and elevation in degrees
    Returns Type:
        float, float
    """

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    # assuming spherical earth with radius 6,367,000m
    R = 6367000
    lat1 = math.radians(pointA[0])
    lon1 = math.radians(pointA[1])
    lat2 = math.radians(pointB[0])
    lon2 = math.radians(pointB[1])

    diffLat = math.radians(pointB[0] - pointA[0])
    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.degrees(math.atan2(x, y))

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    # initial_bearing = math.degrees(initial_bearing)

    azimuth = (initial_bearing + 360) % 360

    # calculations for elevation
    # calculations to fint the angle theta, between the 2 vectors
    # starting from the center of the earth pointing to base and target
    a = math.sin(diffLat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diffLong / 2) ** 2
    theta = 2 * math.asin(math.sqrt(a))

    hBase = R + pointA[2]
    hTarget = R + pointB[2]
    phi = math.pi - theta - math.atan2((hBase * math.sin(theta)), (hTarget - hBase * math.cos(theta)))
    altitude = math.degrees(phi) - 90

    return azimuth, altitude


def _test_calculate_azimuth_elevation():
    """Simple test case for calculate_azimuth_elevation function."""
    pointA = 37.6454331, 24.1062927, 10
    pointB = 37.6454333, 24.3085681, 30000
    print((calculate_azimuth_elevation(pointA, pointB)))


def grab_stdin():
    """
    Grabs input from stdin and if it recognises a desired callsign,
    points the antenna to its location.
    """
    for line in sys.stdin:
        callsign = is_interesting_aprs_packet(line)
        if callsign:
            luft_coords = parse_aprs_packet(line, callsign)
            azalt = calculate_azimuth_elevation(OBSERVER, luft_coords)
            print(azalt)
            point_antenna(azalt[0], azalt[1])


def is_interesting_aprs_packet(packet, list_of_handles=INTERESTING_CALLSIGNS):
    for callsign in list_of_handles:
        try:
            if packet.index(callsign) >= 0:
                return callsign
        except ValueError:
            pass
    return False


def parse_aprs_packet(packet, callsign):
    """Parses APRS packets and returns desired info."""
    parsed = aprslib.parse(packet)
    lat = parsed['latitude']
    lon = parsed['longitude']
    alt = parsed['altitude']
    timestamp = parsed['timestamp']
    print(lat, lon, alt, timestamp)
    return(lat, lon, alt, timestamp)


def point_antenna(azimuth, altitude):
    """Points antenna to provided azimuth altitude pair."""
    sock = trackersocket.trackersocket(TCP_IP, TCP_PORT)
    s = 'P ' + str(azimuth) + ' ' + str(altitude)
    print((s + str('\n')))
    sock.send(s + str('\n'))
    sock.disconnect()


if __name__ == "__main__":
    grab_stdin()
