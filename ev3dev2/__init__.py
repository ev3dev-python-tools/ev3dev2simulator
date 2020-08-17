# -----------------------------------------------------------------------------
# Copyright (c) 2015 Ralph Hempel <rhempel@hempeldesigngroup.com>
# Copyright (c) 2015 Anton Vanhoucke <antonvh@gmail.com>
# Copyright (c) 2015 Denis Demidov <dennis.demidov@gmail.com>
# Copyright (c) 2015 Eric Pascual <eric@pobot.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------
import re
import sys

from ev3dev2simulator.connector.device_connector import DeviceConnector


def is_micropython():
    return sys.implementation.name == "micropython"


def get_current_platform():
    """
    Look in /sys/class/board-info/ to determine the platform type.

    This can return 'ev3', 'evb', 'pistorms', 'brickpi', 'brickpi3' or 'fake'.
    """

    pass


# -----------------------------------------------------------------------------
def list_device_names(class_path, name_pattern, **kwargs):
    """
    This is a generator function that lists names of all devices matching the
    provided parameters.

    Parameters:
        class_path: class path of the device, a subdirectory of /sys/class.
            For example, '/sys/class/tacho-motor'.
        name_pattern: pattern that device name should match.
            For example, 'sensor*' or 'motor*'. Default value: '*'.
        keyword arguments: used for matching the corresponding device
            attributes. For example, address='outA', or
            driver_name=['lego-ev3-us', 'lego-nxt-us']. When argument value
            is a list, then a match against any entry of the list is
            enough.
    """

    pass


def library_load_warning_message(library_name, dependent_class):
    pass


class DeviceNotFound(Exception):
    pass


class Device(object):
    """The ev3dev device base class"""

    __slots__ = [
        '_path',
        '_device_index',
        '_attr_cache',
        'kwargs',
    ]

    DEVICE_ROOT_PATH = '/sys/class'

    _DEVICE_INDEX = re.compile(r'^.*(\d+)$')


    def __init__(self, class_name, name_pattern='*', name_exact=False, **kwargs):
        """Spin through the Linux sysfs class for the device type and find
        a device that matches the provided name pattern and attributes (if any).

        Parameters:
            class_name: class name of the device, a subdirectory of /sys/class.
                For example, 'tacho-motor'.
            name_pattern: pattern that device name should match.
                For example, 'sensor*' or 'motor*'. Default value: '*'.
            name_exact: when True, assume that the name_pattern provided is the
                exact device name and use it directly.
            keyword arguments: used for matching the corresponding device
                attributes. For example, address='outA', or
                driver_name=['lego-ev3-us', 'lego-nxt-us']. When argument value
                is a list, then a match against any entry of the list is
                enough.

        Example::

            d = ev3dev.Device('tacho-motor', address='outA')
            s = ev3dev.Device('lego-sensor', driver_name=['lego-ev3-us', 'lego-nxt-us'])

        If there was no valid connected device, an error is thrown.
        """

        self.kwargs = kwargs
        self._attr_cache = {}
        self.connector = DeviceConnector(self.kwargs.get('address'), class_name)
        self.kwargs['address'] = self.connector.request_device_config(kwargs)



    def __str__(self):
        if 'address' in self.kwargs:
            return "%s(%s)" % (self.__class__.__name__, self.kwargs.get('address'))
        else:
            return self.__class__.__name__


    def __repr__(self):
        return self.__str__()


    # This allows us to sort lists of Device objects
    def __lt__(self, other):
        return str(self) < str(other)


    def _attribute_file_open(self, name):
        pass


    def _get_attribute(self, attribute, name):
        """Device attribute getter"""
        return attribute, self.kwargs.get(name)


    def _set_attribute(self, attribute, name, value):
        """Device attribute setter"""
        pass


    def _raise_friendly_access_error(self, driver_error, attribute, value):
        pass


    def get_attr_int(self, attribute, name):
        pass


    def get_cached_attr_int(self, filehandle, keyword):
        pass


    def set_attr_int(self, attribute, name, value):
        pass


    def set_attr_raw(self, attribute, name, value):
        pass


    def get_attr_string(self, attribute, name):
        return self._get_attribute(attribute, name)


    def get_cached_attr_string(self, filehandle, keyword):
        pass


    def set_attr_string(self, attribute, name, value):
        pass


    def get_attr_line(self, attribute, name):
        pass


    def get_attr_set(self, attribute, name):
        pass


    def get_cached_attr_set(self, filehandle, keyword):
        pass


    def get_attr_from_set(self, attribute, name):
        pass


    @property
    def device_index(self):
        pass


def list_devices(class_name, name_pattern, **kwargs):
    """
    This is a generator function that takes same arguments as `Device` class
    and enumerates all devices present in the system that match the provided
    arguments.

    Parameters:
        class_name: class name of the device, a subdirectory of /sys/class.
            For example, 'tacho-motor'.
        name_pattern: pattern that device name should match.
            For example, 'sensor*' or 'motor*'. Default value: '*'.
        keyword arguments: used for matching the corresponding device
            attributes. For example, address='outA', or
            driver_name=['lego-ev3-us', 'lego-nxt-us']. When argument value
            is a list, then a match against any entry of the list is
            enough.
    """

    pass
