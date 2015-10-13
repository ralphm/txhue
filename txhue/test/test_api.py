# Copyright (c) 2015 Ralph Meijer <ralphm@ik.nu>
# See LICENSE.txt for details

"""
Tests for L{txhue}.
"""

import json

from twisted.internet import defer
from twisted.trial import unittest

from txhue import api


class TreqStub(object):
    """
    Stub providing part of the Treq API.
    """

    def request(self, method, url, **kwargs):
        self.method = method
        self.url = url
        self.kwargs = kwargs

        self.deferred = defer.Deferred()
        return self.deferred


    def json_content(self, response):
        return defer.succeed(response)



class APITest(unittest.TestCase):
    """
    Tests for L{txhue._API).
    """

    def setUp(self):
        self.treq = TreqStub()
        self.api = api._API(self.treq,
                             baseURL=b'http://127.0.0.1/',
                             username=b'test')


    def test_get(self):
        responseData = {u'1': {u'name': u'Bedroom'},
                        u'2': {u'name': u'Kitchen'}}

        def cb(response):
            self.assertEqual(response, responseData)

        d = self.api.get(b'/lights')
        d.addCallback(cb)

        self.assertEqual(b'GET', self.treq.method)
        self.assertEqual(b'http://127.0.0.1/api/test/lights', self.treq.url)
        d.callback(responseData)
        return d


    def test_getWithoutSlash(self):
        """
        Non-empty endpoints without a slash are not valid.
        """
        def checkException(exc):
            self.assertEquals("Endpoint 'lights' does not start with a slash",
                              str(exc))

        d = self.assertFailure(self.api.get(b'lights'), ValueError)
        d.addCallback(checkException)
        return d


    def test_getFullState(self):
        responseData = {u'1': {u'name': u'Bedroom'},
                        u'2': {u'name': u'Kitchen'}}

        def cb(response):
            self.assertEqual(response, responseData)

        d = self.api.get()
        d.addCallback(cb)

        self.assertEqual(b'GET', self.treq.method)
        self.assertEqual(b'http://127.0.0.1/api/test', self.treq.url)
        d.callback(responseData)
        return d


    def test_post(self):
        requestData = {u'time': '2011-03-30T14:24:40',
                       u'command': {
                           u'body': {u'on': True},
                           u'method': u'PUT',
                           u'address': u'/api/<username>/groups/1/action'
                           },
                       u'name': u'Wake up',
                       u'description': u'My wake up alarm'
                       }

        responseData = [{u'success':{u'id': u'2'}}]

        def cb(response):
            self.assertEqual(response, responseData)

        d = self.api.post(b'/schedules', data=requestData)
        d.addCallback(cb)

        self.assertEqual(b'POST', self.treq.method)
        self.assertEqual(b'http://127.0.0.1/api/test/schedules', self.treq.url)
        self.assertEqual(requestData,
                         json.loads(self.treq.kwargs['data']))
        d.callback(responseData)
        return d


    def test_postNoData(self):
        requestData = None
        responseData = [{u'success':
                            {u'/lights': u'Searching for new devices'}}]

        def cb(response):
            self.assertEqual(response, responseData)

        d = self.api.post(b'/lights', data=requestData)
        d.addCallback(cb)

        self.assertEqual(b'POST', self.treq.method)
        self.assertEqual(b'http://127.0.0.1/api/test/lights', self.treq.url)
        self.assertIdentical(None, self.treq.kwargs['data'])
        d.callback(responseData)
        return d


    def test_put(self):
        requestData = {u'name': u'Bedroom Light'}
        responseData = [{u'success': {u'/lights/1/name': u'Bedroom Light'}}]

        def cb(response):
            self.assertEqual(response, responseData)

        d = self.api.put(b'/lights/1', data=requestData)
        d.addCallback(cb)

        self.assertEqual(b'PUT', self.treq.method)
        self.assertEqual(b'http://127.0.0.1/api/test/lights/1', self.treq.url)
        self.assertEqual(requestData,
                         json.loads(self.treq.kwargs['data']))
        d.callback(responseData)
        return d


    def test_putCreateUser(self):
        requestData = {u'devicetype': u'iPhone', u'username': u'1234567890'}
        responseData = [{u'success':{u'username': u'1234567890'}}]

        def cb(response):
            self.assertEqual(response, responseData)

        d = self.api.put(None, data=requestData)
        d.addCallback(cb)

        self.assertEqual(b'PUT', self.treq.method)
        self.assertEqual(b'http://127.0.0.1/api', self.treq.url)
        self.assertEqual(requestData,
                         json.loads(self.treq.kwargs['data']))
        d.callback(responseData)
        return d


    def test_delete(self):
        responseData = [{u'success': u'/schedules/1 deleted.'}]

        def cb(response):
            self.assertEqual(response, responseData)

        d = self.api.delete(b'/schedules/2')
        d.addCallback(cb)

        self.assertEqual(b'DELETE', self.treq.method)
        self.assertEqual(b'http://127.0.0.1/api/test/schedules/2',
                         self.treq.url)
        self.assertIdentical(None, self.treq.kwargs['data'])
        d.callback(responseData)
        return d
