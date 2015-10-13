# Copyright (c) 2015 Ralph Meijer <ralphm@ik.nu>
# See LICENSE.txt for details

"""
Tests for L{txhue.object}.
"""

from twisted.trial import unittest

from txhue.object import Group
from txhue.object import Light
from txhue.object import LightState
from txhue.object import Sensor
from txhue.object import SensorConfig
from txhue.object import SensorState

class LightStateTests(unittest.TestCase):

    def setUp(self):
        self.input = {
            "hue": 50000,
            "on": True,
            "effect": "none",
            "alert": "none",
            "bri": 200,
            "sat": 200,
            "ct": 500,
            "xy": [0.5, 0.5],
            "reachable": True,
            "colormode": "hs"
        }

    def test_fromDict(self):
        result = LightState.fromDict(self.input)
        self.assertEquals(50000, result.hue)


    def test_fromDictXY(self):
        result = LightState.fromDict(self.input)
        self.assertEquals(0.5, result.xy.x)


    def test_fromDictAlertNone(self):
        """
        If alert is C{'none'}, the corresponding attribute has C{None}.
        """
        result = LightState.fromDict(self.input)
        self.assertIs(None, result.alert)


    def test_fromDictEffectNone(self):
        """
        If effect is C{'none'}, the corresponding attribute has C{None}.
        """
        result = LightState.fromDict(self.input)
        self.assertIs(None, result.effect)


    def test_fromDictStringNone(self):
        """
        A string field not using L{txhue.object.stringToNone} is not C{None}.
        """
        self.input['colormode'] = 'none'
        result = LightState.fromDict(self.input)
        self.assertIsNot(None, result.colormode)



class LightTests(unittest.TestCase):

    def test_basic(self):
        input = {
            "state": {
                "hue": 50000,
                "on": True,
                "effect": "none",
                "alert": "none",
                "bri": 200,
                "sat": 200,
                "ct": 500,
                "xy": [0.5, 0.5],
                "reachable": True,
                "colormode": "hs"
            },
            "type": "Living Colors",
            "name": "LC 1",
            "modelid": "LC0015",
            "swversion": "1.0.3"
        }
        result = Light.fromDict(input)
        self.assertEquals('LC0015', result.modelid)
        self.assertEquals(50000, result.state.hue)



class GroupTests(unittest.TestCase):

    def setUp(self):
        self.input = {
            "action": {
                "on": True,
                "hue": 0,
                "effect": "none",
                "bri": 100,
                "sat": 100,
                "ct": 500,
                "xy": [0.5, 0.5]
            },
            "lights": [
                "1",
                "2"
            ],
            "name": "bedroom",
        }

    def test_basic(self):
        result = Group.fromDict(self.input)
        self.assertEquals('bedroom', result.name)


    def test_lights(self):
        result = Group.fromDict(self.input)
        self.assertEquals(["1", "2"], result.lights)

    def test_action(self):
        result = Group.fromDict(self.input)
        self.assertEquals(100, result.action.bri)



class SensorStateTests(unittest.TestCase):
    def setUp(self):
        self.input = {
            "buttonevent": 0,
            "lastupdated": "none"
        }


    def test_basic(self):
        result = SensorState.fromDict(self.input)
        self.assertEquals(0, result.buttonevent)


    def test_lastupdatedNone(self):
        result = SensorState.fromDict(self.input)
        self.assertIs(None, result.lastupdated)



class SensorConfigTests(unittest.TestCase):
    def setUp(self):
        self.input = {
            "on": True,
            "long": "none",
            "lat": "none",
            "sunriseoffset": 50,
            "sunsetoffset": 50
        }


    def test_basic(self):
        result = SensorConfig.fromDict(self.input)
        self.assertIs(True, result.on)


    def test_longInRaw(self):
        result = SensorConfig.fromDict(self.input)
        self.assertEquals('none', result.raw['long'])



class SensorTests(unittest.TestCase):
    def setUp(self):
        self.input = {
            "state": {
                "buttonevent": 0,
                "lastupdated": "none"
            },
            "config": {
                "on": True
            },
            "name": "Tap Switch 2",
            "type": "ZGPSwitch",
            "modelid": "ZGPSWITCH",
            "manufacturername": "Philips",
            "uniqueid": "00:00:00:00:00:40:03:50-f2"
        }

    def test_basic(self):
        result = Sensor.fromDict(self.input)
        self.assertEquals('Tap Switch 2', result.name)
        self.assertEquals(0, result.state.buttonevent)
        self.assertIs(True, result.config.on)
