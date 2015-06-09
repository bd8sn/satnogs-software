#!/usr/bin/env python
 
import socket
import struct
import threading
import logging

from collections import deque

class rtltcp_client(threading.Thread):
    """
    Handles connectivity with rtl_tcp client
    rtl_tcp of 13 Nov 2014
    """

    BUFFER_SIZE = 1024*256

    # loop flag
    _stay_alive = False

    # lock for the socket (socket is not thread safe)
    socket_lock = threading.Lock()

    # logging device
    logger = logging.getLogger('client.rtl_tcp')


    def __init__(self, ip=None, port=None):
        logger = logging.getLogger('client.rtl_tcp')
        self.logger.info('Connecting rtl_tcp ..')
        threading.Thread.__init__(self)
        self.TCP_IP = ip
        self.TCP_PORT = port

        #max 256kB*1024 = 256 Mb maxlen=1024
        self._rcv_buffer = deque()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.TCP_IP, self.TCP_PORT))
        except:
            self.logger.warning('Error connecting socket')



    def isalive(self):
        """Returns if tracking loop is alive or not."""
        return (self._stay_alive)

    def stop(self):
        """Stops the loop softly."""
        self._stay_alive=False

    def run(self):
        self._stay_alive=True
        length=0
        while self._stay_alive:
            with self.socket_lock:
                data = self.s.recv(self.BUFFER_SIZE)
                self._rcv_buffer.append(data)
            length+=len(data)
            self.logger.debug("total samples: %d | last_length %d | buffer_length %d",length,len(data),len(self._rcv_buffer))

        self.logger.info('stopped')
        self.s.close()

    def send(self, message):
            with self.socket_lock:
                return self.s.sendall(message)

    def sendCommand(self, par_cmd, par_value):
        cmd = struct.pack('!BI', par_cmd, par_value)
        return self.send(cmd)

    def rcvbuffer_length(self):
        return len(self._rcv_buffer)

    def rcvbuffer_getNext(self):
        return self._rcv_buffer.popleft()

    def set_center_frequency(self, par_value):
        self.logger.info('set center frequency %d',par_value)
        return self.sendCommand(0x01, par_value)

    def set_sample_rate(self, par_value):
        self.logger.info('set sample rate %d',par_value)
        return self.sendCommand(0x02, par_value)

    def set_tuner_gain_mode(self, par_value):
        return self.sendCommand(0x03, par_value)

    def set_tuner_gain(self, par_value):
        return self.sendCommand(0x04, par_value)

    def set_freq_correction(self, par_value):
        return self.sendCommand(0x05, par_value)

    def set_tuner_if_gain(self, par_value):
        return self.sendCommand(0x06, par_value)

    def set_testmode(self, par_value):
        return self.sendCommand(0x07, par_value)

    def set_agc_mode(self, par_value):
        return self.sendCommand(0x08, par_value)

    def set_direct_sampling(self, par_value):
        return self.sendCommand(0x09, par_value)

    def set_offset_tuning(self, par_value):
        return self.sendCommand(0x0a, par_value)

    def set_xtal_freq(self, par_value):
        return self.sendCommand(0x0b, par_value)

    def set_tuner_xtal(self, par_value):
        return self.sendCommand(0x0c, par_value)

    def set_tuner_gain_by_index(self, par_value):
        self.logger.info('set gain by index %d',par_value)
        return self.sendCommand(0x0d, par_value)


if __name__=='__main__':
    logger = logging.getLogger('client')
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


    tcpclient = rtltcp_client('127.0.0.1',1234)
    tcpclient.start()

    tcpclient.set_center_frequency(100e6)
    tcpclient.set_sample_rate(750000)


    f = open('workfile.rtliq', 'w')

    import time

    try:
        while True:
            if tcpclient.rcvbuffer_length():
                while tcpclient.rcvbuffer_length():
                    f.write(tcpclient.rcvbuffer_getNext())
                    pass
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    logger.warning('Received CTRL-C ..')

    tcpclient.stop()

    pass
