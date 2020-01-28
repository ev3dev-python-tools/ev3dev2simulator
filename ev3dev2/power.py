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

import sys

if sys.version_info < (3, 4):
    raise SystemError('Must be using Python 3.4 or higher')

from ev3dev2 import Device


class PowerSupply(Device):
    """
    A generic interface to read data from the system's power_supply class.
    Uses the built-in legoev3-battery if none is specified.
    """

    SYSTEM_CLASS_NAME = 'power_supply'
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = [
        '_measured_current',
        '_measured_voltage',
        '_max_voltage',
        '_min_voltage',
        '_technology',
        '_type',
    ]


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        if address is not None:
            kwargs['address'] = address
        super(PowerSupply, self).__init__(self.SYSTEM_CLASS_NAME, name_pattern, name_exact, **kwargs)

        pass


    @property
    def measured_current(self):
        """
        The measured current that the battery is supplying (in microamps)
        """

        pass


    @property
    def measured_voltage(self):
        """
        The measured voltage that the battery is supplying (in microvolts)
        """

        pass


    @property
    def max_voltage(self):
        """
        """

        pass


    @property
    def min_voltage(self):
        """
        """

        pass


    @property
    def technology(self):
        """
        """

        pass


    @property
    def type(self):
        """
        """

        pass


    @property
    def measured_amps(self):
        """
        The measured current that the battery is supplying (in amps)
        """

        pass


    @property
    def measured_volts(self):
        """
        The measured voltage that the battery is supplying (in volts)
        """

        pass
