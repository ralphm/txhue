# Copyright (c) 2015 Ralph Meijer <ralphm@ik.nu>
# See LICENSE.txt for details

from twisted.python import log

class BaseObject(object):
    """
    A base object.
    """
    raw = None
    SIMPLE_PROPS = None
    COMPLEX_PROPS = None
    LIST_PROPS = None

    @classmethod
    def fromDict(cls, data):
        """
        Fill this objects attributes from a dict for known properties.
        """
        obj = cls()
        obj.raw = data
        for name, value in data.iteritems():
            parser = getattr(cls, '_parse_{}'.format(name), None)
            if parser:
                value = parser(value)

            if cls.SIMPLE_PROPS and name in cls.SIMPLE_PROPS:
                setattr(obj, name, value)
            elif cls.COMPLEX_PROPS and name in cls.COMPLEX_PROPS:
                value = cls.COMPLEX_PROPS[name].fromDict(value)
                setattr(obj, name, value)
            elif cls.LIST_PROPS and name in cls.LIST_PROPS:
                print value
                value = [cls.LIST_PROPS[name].fromDict(item)
                         for item in value]
                setattr(obj, name, value)

        return obj


    def __repr__(self):
        bodyParts = []
        for name in dir(self):
            if self.SIMPLE_PROPS and name in self.SIMPLE_PROPS:
                if hasattr(self, name):
                    bodyParts.append("%s=%s" % (name,
                                                repr(getattr(self, name))))

            elif self.COMPLEX_PROPS and name in self.COMPLEX_PROPS:
                if hasattr(self, name):
                    bodyParts.append("%s=%s" % (name,
                                                repr(getattr(self, name))))
            elif self.LIST_PROPS and name in self.LIST_PROPS:
                if hasattr(self, name):
                    items = getattr(self, name)

                    itemBodyParts = []
                    for item in items:
                        itemBodyParts.append(repr(item))

                    itemBody = ',\n'.join(itemBodyParts)
                    lines = itemBody.splitlines()
                    itemBody = '\n    '.join(lines)

                    if itemBody:
                        itemBody = '\n    %s\n' % (itemBody,)

                    bodyParts.append("%s=[%s]" % (name, itemBody))

        body = ',\n'.join(bodyParts)
        lines = body.splitlines()
        body = '\n    '.join(lines)

        result = "%s(\n    %s\n)" % (self.__class__.__name__, body)
        return result



def stringToNone(value):
    if value == "none":
        return None
    else:
        return value



class Coordinates(BaseObject):
    """
    Indices for tweet entities.
    """
    x = None
    y = None

    @classmethod
    def fromDict(cls, data):
        obj = cls()
        obj.raw = data
        try:
            obj.x, obj.y = data
        except (TypeError, ValueError):
            log.err()
        return obj

    def __repr__(self):
        return "%s(x=%s, y=%s)" % (self.__class__.__name__,
                                         self.x, self.y)


class LightState(BaseObject):
    SIMPLE_PROPS = {
        'on',
        'bri',
        'hue',
        'sat',
        'ct',
        'alert',
        'effect',
        'colormode',
        'reachable',

        # action fields
        'transitiontime',
        'bri_inc',
        'sat_inc',
        'hue_inc',
        'ct_inc',
        'xy_inc',
        'scene',
    }
    COMPLEX_PROPS = {
        'xy': Coordinates
    }

    _parse_alert = staticmethod(stringToNone)
    _parse_effect = staticmethod(stringToNone)



class Light(BaseObject):
    SIMPLE_PROPS = {
        'name',
        'modelid',
        'swversion'
        'type',
        'uniqueid',
        'manufacturername',
        'luminaireuniqueid',
    }
    COMPLEX_PROPS = {
        'state': LightState,
    }



class Group(BaseObject):
    SIMPLE_PROPS = {
        'name',
        'type',
        'modelid',
        'lights',
    }

    COMPLEX_PROPS = {
        'action': LightState,
    }



class SensorConfig(BaseObject):
    """
    Sensor configuration.

    Note that there are various types of sensors. This object only covers
    common sensor configuration fields for switches and CLIP sensors.
    Additional fields can be accessed using the C{raw} attribute.
    """

    SIMPLE_PROPS = {
        'on',
        'reachable',
        'battery',
        'url',
    }


class SensorState(BaseObject):
    """
    Sensor state.

    Note that there are various types of sensors. This object only covers
    common sensor state fields for switches and CLIP sensors. Additional fields
    can be accessed using the C{raw} attribute.
    """
    SIMPLE_PROPS = {
        'buttonevent',
        'lastupdated',
    }

    _parse_lastupdated = staticmethod(stringToNone)



class Sensor(BaseObject):
    SIMPLE_PROPS = {
        'name',
        'modelid',
        'swversion'
        'type',
        'uniqueid',
        'manufacturername',
    }

    COMPLEX_PROPS = {
        'config': SensorConfig,
        'state': SensorState,
    }
