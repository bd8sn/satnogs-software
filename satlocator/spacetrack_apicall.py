# -*- coding: utf-8 -*-
import requests


class apicaller:
    """ Class handling API calls to Space Track
    """
    _login_credentials = None
    _cookies = None

    url_base = "https://www.space-track.org/"
    url_login = "ajaxauth/login"
    url_logout = "ajaxauth/logout"
    url_request = "basicspacedata/query/class/tle/format/json/NORAD_CAT_ID/25544/orderby/EPOCH desc/limit/22"
    #"basicspacedata/query/class/boxscore/format/json"
    #"basicspacedata/query/class/tle/orderby/TLE_LINE0 asc/limit/100/metadata/false"

    def __init__(self, credentials=None):
        if credentials is not None:
            self._login_credentials = credentials

    def login(self, credentials=None):
        if self._valid_credentials(credentials):
            pass
        elif self._login_credentials is not None:
            credentials = self._login_credentials
        else:
            print(("error:", "cookie:", "wrong flavour"))
            return False

        url = self.url_base + self.url_login
        r = requests.post(url, data=self._login_credentials)
        if r.status_code == requests.codes.ok:
            self._cookies = r.cookies.get_dict()
            return True
        else:
            print(("error:", "login:", r.text))
            return False

    def logout(self):
        url = self.url_base + self.url_logout
        r = requests.get(url, cookies=self._cookies)
        if r.text == '"Successfully logged out"':
            return True
        return False

    def request(self, payload=None):
        if payload is None:
            url = self.url_base + self.url_request
        else:
            url = self.url_base + payload
        r = requests.get(url, cookies=self._cookies)
        return r.json()

    def _valid_credentials(self, credentials):
        if isinstance(credentials, dict):
            if 'identity' in credentials and 'password' in credentials:
                return True
        return False

    def request_sequence(self, credentials=None, payload=None):
        if credentials:
            self._login_credentials = credentials
        self.login(credentials=self._login_credentials)
        r = self.request(payload=payload)
        self.logout()
        return r.json()