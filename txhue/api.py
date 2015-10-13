# Copyright (c) 2015 Ralph Meijer <ralphm@ik.nu>
# See LICENSE.txt for details

"""
Twisted Hue.
"""

import json
from twisted.internet import defer

class _API(object):
    """
    Basic Hue API.
    """

    def __init__(self, treq, baseURL, username=None):
        self.treq = treq
        self.baseURL = baseURL
        self.username = username


    def get(self, endpoint=None):
        return self.request('GET', endpoint)


    def post(self, endpoint, data=None):
        return self.request('POST', endpoint, data=data)


    def put(self, endpoint, data=None):
        return self.request('PUT', endpoint, data=data)


    def delete(self, endpoint):
        return self.request('DELETE', endpoint)


    def request(self, method, endpoint, data=None):
        """
        Make a request to the Hue bridge.

        @param method: The HTTP request method.
        @type method: C{bytes}

        @param endpoint: The API endpoint. Note that, if not empty, it must
        start with a slash (C{/}). The Hue API consistently uses endpoints
        prefixed with slashes in API responses, schedules and rules.
        """
        url = self.baseURL + 'api'
        if endpoint or method == 'GET':
            url = '{url}/{username}'.format(url=url, username=self.username)
        if endpoint:
            if not endpoint.startswith('/'):
                return defer.fail(
                    ValueError("Endpoint {0!r} does not start with a slash"
                                   .format(endpoint)))
            url += endpoint

        if data is not None:
            data = json.dumps(data)

        d = self.treq.request(method, url, data=data)
        d.addCallback(self.treq.json_content)
        return d
