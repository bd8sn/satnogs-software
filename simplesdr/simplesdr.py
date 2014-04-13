import json
import decimal
from bottle import route, run, abort
from rtlsdr import RtlSdr


@route('/data/:freq', method='GET')
def get_data(freq):
    sdr = RtlSdr()

    sdr.sample_rate = 2.048e6
    sdr.center_freq = int(decimal.Decimal(str(freq) + 'e6'))
    sdr.freq_correction = 60
    sdr.gain = 'auto'

    data = sdr.read_samples(512)

    if not data:
        abort(404, 'No data!')

    d = []
    for item in data:
        d.append(str(item))

    js = json.dumps(d)
    return js

run(host='localhost', port=8080)
