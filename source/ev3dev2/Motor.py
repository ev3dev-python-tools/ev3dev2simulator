# -----------------------------------------------------------------------------
# Copyright (c) 2015 Ralph Hempel <rhempel@hempeldesigngroup.com>
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

import sys

from ev3dev2.MockMotor import MockMotor

if sys.version_info < (3, 4):
    raise SystemError('Must be using Python 3.4 or higher')

# python3 uses collections
# micropython uses ucollections
# try:
# except ImportError:
#     from ucollections import OrderedDict

from logging import getLogger

# from ev3dev2 import get_current_platform, Device, list_device_names

# from ev3dev2.stopwatch import StopWatch

log = getLogger(__name__)

# The number of milliseconds we wait for the state of a motor to
# update to 'running' in the "on_for_XYZ" methods of the Motor class
WAIT_RUNNING_TIMEOUT = 100


# OUTPUT ports have platform specific values that we must import
# platform = get_current_platform()


# if platform == 'ev3':
#     from ev3dev2._platform.ev3 import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
#
# elif platform == 'evb':
#     from ev3dev2._platform.evb import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
#
# elif platform == 'pistorms':
#     from ev3dev2._platform.pistorms import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
#
# elif platform == 'brickpi':
#     from ev3dev2._platform.brickpi import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
#
# elif platform == 'brickpi3':
#     from ev3dev2._platform.brickpi3 import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, \
#         OUTPUT_E, OUTPUT_F, OUTPUT_G, OUTPUT_H, \
#         OUTPUT_I, OUTPUT_J, OUTPUT_K, OUTPUT_L, \
#         OUTPUT_M, OUTPUT_N, OUTPUT_O, OUTPUT_P
#
# elif platform == 'fake':
#     from ev3dev2._platform.fake import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
#
# else:
#     raise Exception("Unsupported platform '%s'" % platform)


class SpeedValue(object):
    """
    A base class for other unit types. Don't use this directly; instead, see
    :class:`SpeedPercent`, :class:`SpeedRPS`, :class:`SpeedRPM`,
    :class:`SpeedDPS`, and :class:`SpeedDPM`.
    """

    def __eq__(self, other):
        return self.to_native_units() == other.to_native_units()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.to_native_units() < other.to_native_units()

    def __le__(self, other):
        return self.to_native_units() <= other.to_native_units()

    def __gt__(self, other):
        return self.to_native_units() > other.to_native_units()

    def __ge__(self, other):
        return self.to_native_units() >= other.to_native_units()

    def __rmul__(self, other):
        return self.__mul__(other)


class SpeedPercent(SpeedValue):
    """
    Speed as a percentage of the motor's maximum rated speed.
    """

    def __init__(self, percent):
        assert -100 <= percent <= 100, \
            "{} is an invalid percentage, must be between -100 and 100 (inclusive)".format(percent)

        self.percent = percent

    def __str__(self):
        return str(self.percent) + "%"

    def __mul__(self, other):
        assert isinstance(other, (float, int)), "{} can only be multiplied by an int or float".format(self)
        return SpeedPercent(self.percent * other)

    def to_native_units(self, motor):
        """
        Return this SpeedPercent in native motor units
        """
        return self.percent / 100 * motor.max_speed


class SpeedNativeUnits(SpeedValue):
    """
    Speed in tacho counts per second.
    """

    def __init__(self, native_counts):
        self.native_counts = native_counts

    def __str__(self):
        return "{:.2f}".format(self.native_counts) + " counts/sec"

    def __mul__(self, other):
        assert isinstance(other, (float, int)), "{} can only be multiplied by an int or float".format(self)
        return SpeedNativeUnits(self.native_counts * other)

    def to_native_units(self, motor=None):
        """
        Return this SpeedNativeUnits as a number
        """
        return self.native_counts


class Motor(MockMotor):

    def __init__(self, address, **kwargs):
        super(Motor, self).__init__(address)


class LargeMotor(Motor):
    """
    EV3/NXT large servo motor.

    Same as :class:`Motor`, except it will only successfully initialize if it finds a "large" motor.
    """

    SYSTEM_CLASS_NAME = Motor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = []

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(LargeMotor, self).__init__(address, name_pattern, name_exact,
                                         driver_name=['lego-ev3-l-motor', 'lego-nxt-motor'], **kwargs)
