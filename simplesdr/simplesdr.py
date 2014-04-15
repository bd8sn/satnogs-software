import json
import decimal
from bottle import Bottle, run, request, response
from rtlsdr import RtlSdr


app = Bottle()


@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route('/data/:freq', method='GET')
def get_data(freq):
    sdr = RtlSdr()

    sdr.sample_rate = 2.048e6
    sdr.center_freq = int(decimal.Decimal(str(freq) + 'e6'))
    sdr.freq_correction = 60
    sdr.gain = 'auto'

    data = sdr.read_samples(512)

    if not data.any():
        app.abort(404, 'No data!')

    d = []
    for item in data:
        d.append(str(item))

    js = json.dumps(d)
    return js


if __name__ == "__main__":
    app.run(host='localhost', port=9000)

