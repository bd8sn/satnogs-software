# -*- coding: utf-8 -*-
""" API for TLE service.

    Requires:

    gevent (optional)
        sudo aptitude install gevent

    gunicorn
        sudo aptitude install gunicorn

    Usage:
        gunicorn --workers 2 --log-level INFO api_tle:app
        gunicorn --workers 2 --log-level INFO --worker-class gevent --bind 127.0.0.1:8002 api_tle:app
        gunicorn --workers 2 --daemon --log-level INFO --worker-class gevent --bind 127.0.0.1:8002 api_tle:app

    Help:
        gunicorn --help
"""
import bottle
from bottle import route, error, post, get, run, static_file, abort, redirect, response, request, template
import spacetrack_apicall as apicall

TRACKER = apicall.apicaller()


@route('/hello')
def hello():
    return {"hello": "I am alive."}


@get('/login/:username/:password')
def login_get(username, password):
    if username and password:
        credentials = {'identity': username, 'password': password}
    else:
        error("Insuffient parameters.")
    TRACKER.login(credentials)
    return {"success": True}


@post('/login')
def login_post():
    return {"success": True}


@route('/raise_error')
def raise_error():
    abort(404, "error...")


@route('/redirect')
def redirect_to_hello():
    redirect('/hello')


@error(404)
def error404(error):
    return '404 error.'

if __name__ == "__main__":
    run(host='localhost', port=8080)

app = bottle.default_app()