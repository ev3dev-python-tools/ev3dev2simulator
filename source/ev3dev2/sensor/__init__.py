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
import numbers

from ev3dev2 import Device


class Sensor(Device):
    """
    The sensor class provides a uniform interface for using most of the
    sensors available for the EV3. The various underlying device drivers will
    create a `lego-sensor` device for interacting with the sensors.

    Sensors are primarily controlled by setting the `mode` and monitored by
    reading the `value<N>` attributes. Values can be converted to floating point
    if needed by `value<N>` / 10.0 ^ `decimals`.

    Since the name of the `sensor<N>` device node does not correspond to the port
    that a sensor is plugged in to, you must look at the `address` attribute if
    you need to know which port a sensor is plugged in to. However, if you don't
    have more than one sensor of each type, you can just look for a matching
    `driver_name`. Then it will not matter which port a sensor is plugged in to - your
    program will still work.
    """

    SYSTEM_CLASS_NAME = 'lego-sensor'
    SYSTEM_DEVICE_NAME_CONVENTION = 'sensor*'
    __slots__ = [
        '_address',
        '_command',
        '_commands',
        '_decimals',
        '_driver_name',
        '_mode',
        '_modes',
        '_num_values',
        '_units',
        '_value',
        '_bin_data_format',
        '_bin_data_size',
        '_bin_data',
        '_mode_scale'
    ]


    def __init__(self, address, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        if address is not None:
            kwargs['address'] = address
        super(Sensor, self).__init__(self.SYSTEM_CLASS_NAME, name_pattern, name_exact, **kwargs)

        self._address = None
        self._command = None
        self._commands = None
        self._decimals = None
        self._driver_name = None
        self._mode = None
        self._modes = None
        self._num_values = None
        self._units = None
        self._value = [None, None, None, None, None, None, None, None]

        self._bin_data_format = None
        self._bin_data_size = None
        self._bin_data = None
        self._mode_scale = {}


    def _scale(self, mode):
        """
        Returns value scaling coefficient for the given mode.
        """
        if mode in self._mode_scale:
            scale = self._mode_scale[mode]
        else:
            scale = 10 ** (-self.decimals)
            self._mode_scale[mode] = scale

        return scale


    @property
    def address(self):
        """
        Returns the name of the port that the sensor is connected to, e.g. `ev3:in1`.
        I2C sensors also include the I2C address (decimal), e.g. `ev3:in1:i2c8`.
        """

        return self._address


    @property
    def command(self):
        """
        Sends a command to the sensor.
        """
        raise Exception("command is a write-only property!")


    @command.setter
    def command(self, value):
        self._command = value


    @property
    def commands(self):
        """
        Returns a list of the valid commands for the sensor.
        Returns -EOPNOTSUPP if no commands are supported.
        """

        return self._commands


    @property
    def decimals(self):
        """
        Returns the number of decimal places for the values in the `value<N>`
        attributes of the current mode.
        """

        return self._decimals


    @property
    def driver_name(self):
        """
        Returns the name of the sensor device/driver. See the list of [supported
        sensors] for a complete list of drivers.
        """

        return self._driver_name


    @property
    def mode(self):
        """
        Returns the current mode. Writing one of the values returned by `modes`
        sets the sensor to that mode.
        """

        return self._mode


    @mode.setter
    def mode(self, value):
        self._mode = value


    @property
    def modes(self):
        """
        Returns a list of the valid modes for the sensor.
        """

        return self._modes


    @property
    def num_values(self):
        """
        Returns the number of `value<N>` attributes that will return a valid value
        for the current mode.
        """

        return self._num_values


    @property
    def units(self):
        """
        Returns the units of the measured value for the current mode. May return
        empty string
        """

        return self._units


    def value(self, n=0):
        """
        Returns the value or values measured by the sensor. Check num_values to
        see how many values there are. Values with N >= num_values will return
        an error. The values are fixed point numbers, so check decimals to see
        if you need to divide to get the actual value.
        """
        if isinstance(n, numbers.Real):
            n = int(n)
        elif isinstance(n, str):
            n = int(n)

        return self._value[n]


    @property
    def bin_data_format(self):
        """
        Returns the format of the values in `bin_data` for the current mode.
        Possible values are:

        - `u8`: Unsigned 8-bit integer (byte)
        - `s8`: Signed 8-bit integer (sbyte)
        - `u16`: Unsigned 16-bit integer (ushort)
        - `s16`: Signed 16-bit integer (short)
        - `s16_be`: Signed 16-bit integer, big endian
        - `s32`: Signed 32-bit integer (int)
        - `float`: IEEE 754 32-bit floating point (float)
        """

        return self._bin_data_format


    def _ensure_mode(self, mode):
        if self.mode != mode:
            self.mode = mode
