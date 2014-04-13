# SimpleSDR

A simple SDR reader of a given frequency.

## Run

System dependencies:

`yum install gr-osmosdr`

Python dependencies (that can be installed inside a virtualenv):

`pip install -r requirements.txt`

and it's accessible through a dead simple web api:

`gunicorn --workers 2 -b 127.0.0.1:9000 --log-level INFO simplesdr:app`

example:

`http://localhost:9000/data/145`

will return data for 145MHz.


