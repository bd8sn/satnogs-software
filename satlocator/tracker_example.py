# -*- coding: utf-8 -*-
""" An example of usage for the pinpointing functionality of the tracker module.
"""

import orbitaltracker
from datetime import datetime
import time
import trackersocket

SLEEP_TIME = 0.1  # in seconds

HSGR_COORDS = {
'lat': 38.017120,
'lon': 23.731230,
'elev': 132
}

PLUS_COORDS = {
'lat': 38.017120,
'lon': 23.731230,
'elev': 132
}

ISS_TLE = {
"TLE_LINE0": "0 ISS (ZARYA)",
"TLE_LINE1": "1 25544U 98067A   14103.32235382  .00083249  00000-0  14653-2 0   726",
"TLE_LINE2": "2 25544 051.6474 061.0213 0003735 283.8131 171.7524 15.49723829881268"
}

SEDSAT1_TLE = {
"TLE_LINE0": "0 SEDSAT 1",
"TLE_LINE1": "1 25509U 98061B   14101.59573229  .00001029  00000-0  18850-3 0  7270",
"TLE_LINE2": "2 25509 031.4330 177.6836 0350016 250.9805 255.0604 14.29464209807614"
}


def main():
    """ Sets up station and satellite to track.
    """
    observer = HSGR_COORDS
    sat_tle_dict = SEDSAT1_TLE
    # tracker init
    tr = orbitaltracker.orbitaltracker()
    tr.add_station('hsgr', observer['lat'], observer['lon'], observer['elev'])
    tr.add_satellite_from_tle(sat_tle_dict, '0 SEDSAT 1')

    # debug
    print((tr.stations))
    print((tr.satellites))

    # test below
    #track(tr)
    #windows(tr)
    track_and_send(tr)


def track(tr):
    """ Track satellite based on TLE. Does NOT communicate with antenna motors.
    """
    # track satellite
    for i in range(0, 1000000):
        p = tr.pinpoint('hsgr', '0 SEDSAT 1')
        if p['ok']:
            print((datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                'alt:', p['alt'], 'az:', p['az'],
                'v:', p['rng_vlct'], 'r:', p['rng']))
        time.sleep(SLEEP_TIME)


def track_and_send(tr):
    ''' Tracks given satellite and sends positioning commands to antenna.
    '''
    ### daemon command on beagle:
    ### rotctld -m 202 -v -r /dev/ttyACM0
    #import os

    # create and open socket
    sock = trackersocket.trackersocket()
    sock.connect('10.2.110.108', 4533)  # change to correct address
    # track satellite
    for i in range(0, 10000):
        p = tr.pinpoint('hsgr', '0 SEDSAT 1')
        if p['ok']:
            s = 'P ' + str((p['az'].conjugate())) + ' ' + str(p['alt'].conjugate())
            #print s + os.linesep
            print s + str('\n')
            sock.send(s + str('\n'))
            time.sleep(SLEEP_TIME)
    sock.disconnect()


def windows(tr):
    """ Calculate visibility windows for give satellite from given station.
    """
    # calculate visibility windows for next 24 hours
    print((tr.calculate_windows('hsgr', 'ISS')))


main()