# -*- coding: utf-8 -*-
""" Class to facilitate tracking loop.
"""

import trackersocket
import orbital
import time
import threading


class TrackerWorker():

    # socket to connect to
    _IP = '127.0.0.1'  # default is localhost
    _PORT = 4533  # default receiver port

    # sleep time of loop
    SLEEP_TIME = 0.1  # in seconds  # TODO: get this from config?
    # loop flag
    _stay_alive = False

    observer_dict = {}
    satellite_dict = {}

    def __init__(self, ip=None, port=None):
        if ip is not None:
            self._IP = ip
        if port is not None:
            self._PORT = port

    def isalive(self):
        """ Returns if tracking loop is alive or not.
        """
        return self._stay_alive

    def trackobject(self, observer_dict, satellite_dict):
        """ Sets tracking object.
            Can also be called while tracking, to change observed object.
        """
        self.observer_dict = observer_dict
        self.satellite_dict = satellite_dict

    def trackstart(self):
        """ Starts the thread that communicates tracking info to remote socket.

            Stops by calling trackstop()
        """
        self.stay_alive = True
        t = threading.Thread(target=self._communicate_tracking_info)
        t.daemon = True
        t.start()
        return True

    def _communicate_tracking_info(self):
        """ Runs as a daemon thread, communicating tracking info to remote socket.

            Uses observer and satellite objects set by trackobject().

            Will exit if altitude is less than zero (below the horizon).
        """
        sock = trackersocket.trackersocket()
        sock.connect(self._IP, self._PORT)  # change to correct address
        # track satellite
        while self._stay_alive:
            p = orbital.pinpoint(self.observer_dict, self.satellite_dict)
            if p['ok']:
                if p['alt'] < 0:
                    # break
                    self._stay_alive = False
                else:
                    s = 'P ' + str((p['az'].conjugate())) + ' ' + str(p['alt'].conjugate())
                    #print s + str('\n')
                    sock.send(s + str('\n'))
                    time.sleep(self.SLEEP_TIME)
        # exiting
        sock.disconnect()

    def trackstop(self):
        """ Sets object flag to false and stops the tracking thread.
        """
        self._stay_alive = False
