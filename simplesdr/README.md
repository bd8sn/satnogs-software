# SimpleSDR

A simple SDR reader of a given frequency.

## Run

It depends on bottle and pyrtlsdr:

`pip install -r requirements.txt`

and it's accessible through a dead simple web api:

`python simplesdr.py`

example:

`http://localhost:8080/data/145`

will return data for 145MHz.


