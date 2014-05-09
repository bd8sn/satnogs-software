# -*- coding: utf-8 -*-
""" This should never have reached gihub :P

    Look away people, look away...
"""
import math
import sys
import time
import threading
import json

import trackersocket

INTERESTING_HANDLES = ['J43VHF-11']
SAMPLE_PACKET = '2014-04-06 14:44:01 EEST: J43VHF-11>APRS,J43VAI*,qAR,SV3RF:/114358h3807.13N/02347.25EF000/000/A=000922/TEMP=20/VOLT=10744  j43vhf.wordpress.com'

HSGR = (38.0171, 23.7312, 61)

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

        Authored by manthos and azisi. All praise and blame on them ;)
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
    phi = math.pi - theta - math.atan((hBase * math.sin(theta)) / (hTarget - hBase * math.cos(theta)))
    altitude = math.degrees(phi) - 90

    # return calculated azimuth and alt
    return azimuth, altitude


def _test_calculate_azimuth_elevation():
    pointA = 37.6454331, 24.1062927, 10
    pointB = 37.6454333, 24.3085681, 30000
    print((calculate_azimuth_elevation(pointA, pointB)))


def grab_stdin():
    for line in sys.stdin:
        #print 'input was:',line
        if is_interesting_aprs_packet(line):
            luft_coords = parse_aprs_packet(line)
            azalt = calculate_azimuth_elevation(luft_coords)
            print(azalt)


def is_interesting_aprs_packet(packet, list_of_handles=INTERESTING_HANDLES):
    for callsign in list_of_handles:
        try:
            if packet.index(callsign) >= 0:
                return callsign
        except ValueError:
            pass
    return False


# SAMPLE_PACKET = '2014-04-06 14:44:01 EEST: J43VHF-11>APRS,J43VAI*,qAR,SV3RF:/114358h3807.13N/02347.25EF000/000/A=000922/TEMP=20/VOLT=10744  j43vhf.wordpress.com'
def parse_aprs_packet(packet, callsign):
    callsign = is_interesting_aprs_packet(packet)
    p_call = packet.index(callsign)
    p_path = p_call + len(callsign)
    if packet[p_path:][0] != '>':
        print('Error: > not found after callsign')
    else:
        p_message = p_path + 2 + packet[p_path + 1:].index('/')
        message = packet[p_message:]
        timestamp_luft = message[:6]
        if message[6] != 'h':
            print('Error: h not found after timestamp')
        else:
            lat = float(message[7:14].replace('.', '').replace(message[7:9], message[7:9] + '.'))
            lon = float(message[16:24].replace('.', '').replace(message[16:19], message[16:19] + '.'))
            elev = message[25 + 3 + message[25:].index('/A='):25 + 3 + 6 + message[25:].index('/A=')]

    return(lat, lon, elev, timestamp_luft)


def track_luftballon():
    pass


def main():
    #_test_calculate_azimuth_elevation()
    grab_stdin()

if __name__ == "__main__":
    main()