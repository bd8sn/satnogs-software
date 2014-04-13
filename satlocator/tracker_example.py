# -*- coding: utf-8 -*-
""" An example of usage for the pinpointing functionality of the tracker module.
"""

import tracker
from datetime import datetime
import time

SLEEP_TIME = 0.0005  # in seconds

HSGR_COORDS = {
'lat': 38.017120,
'lon': 23.731230,
'elev': 132
}

ISS_TLE = {
"TLE_LINE0": "0 ISS (ZARYA)",
"TLE_LINE1": "1 25544U 98067A   14103.32235382  .00083249  00000-0  14653-2 0   726",
"TLE_LINE2": "2 25544 051.6474 061.0213 0003735 283.8131 171.7524 15.49723829881268"
}


def main():
    observer = HSGR_COORDS
    sat_tle_dict = ISS_TLE
    # tracker init
    tr = tracker.tracker()
    tr.add_station('hsgr', observer['lat'], observer['lon'], observer['elev'])
    tr.add_satellite_from_tle(sat_tle_dict, 'ISS')

    # debug
    print((tr.stations))
    print((tr.satellites))

    # track satellite
    for i in range(0, 1000000):
        p = tr.pinpoint('hsgr', 'ISS')
        if p['ok']:
            print((datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                'alt:', p['alt'], 'az:', p['az'],
                'v:', p['rng_vlct'], 'r:', p['rng']))
        time.sleep(SLEEP_TIME)

main()