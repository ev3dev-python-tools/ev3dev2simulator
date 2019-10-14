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

from collections import OrderedDict
from ev3dev2 import Device


class Led(Device):
    """
    Any device controlled by the generic LED driver.
    See https://www.kernel.org/doc/Documentation/leds/leds-class.txt
    for more details.
    """

    SYSTEM_CLASS_NAME = 'leds'
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = [
        '_max_brightness',
        '_brightness',
        '_triggers',
        '_trigger',
        '_delay_on',
        '_delay_off',
        'desc',
    ]


    def __init__(self,
                 name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False,
                 desc=None, **kwargs):
        self.desc = desc
        super(Led, self).__init__(self.SYSTEM_CLASS_NAME, name_pattern, name_exact, **kwargs)
        self._max_brightness = None
        self._brightness = None
        self._triggers = None
        self._trigger = None
        self._delay_on = None
        self._delay_off = None


    def __str__(self):
        if self.desc:
            return self.desc
        else:
            return Device.__str__(self)


    @property
    def max_brightness(self):
        """
        Returns the maximum allowable brightness value.
        """

        pass


    @property
    def brightness(self):
        """
        Sets the brightness level. Possible values are from 0 to `max_brightness`.
        """

        pass


    @brightness.setter
    def brightness(self, value):

        pass


    @property
    def triggers(self):
        """
        Returns a list of available triggers.
        """

        pass


    @property
    def trigger(self):
        """
        Sets the LED trigger. A trigger is a kernel based source of LED events.
        Triggers can either be simple or complex. A simple trigger isn't
        configurable and is designed to slot into existing subsystems with
        minimal additional code. Examples are the `ide-disk` and `nand-disk`
        triggers.

        Complex triggers whilst available to all LEDs have LED specific
        parameters and work on a per LED basis. The `timer` trigger is an example.
        The `timer` trigger will periodically change the LED brightness between
        0 and the current brightness setting. The `on` and `off` time can
        be specified via `delay_{on,off}` attributes in milliseconds.
        You can change the brightness value of a LED independently of the timer
        trigger. However, if you set the brightness value to 0 it will
        also disable the `timer` trigger.
        """

        pass


    @trigger.setter
    def trigger(self, value):

        pass


    @property
    def delay_on(self):
        """
        The `timer` trigger will periodically change the LED brightness between
        0 and the current brightness setting. The `on` time can
        be specified via `delay_on` attribute in milliseconds.
        """

        pass


    @delay_on.setter
    def delay_on(self, value):

        pass


    @property
    def delay_off(self):
        """
        The `timer` trigger will periodically change the LED brightness between
        0 and the current brightness setting. The `off` time can
        be specified via `delay_off` attribute in milliseconds.
        """

        pass


    @delay_off.setter
    def delay_off(self, value):

        pass


    @property
    def brightness_pct(self):
        """
        Returns LED brightness as a fraction of max_brightness
        """

        pass


    @brightness_pct.setter
    def brightness_pct(self, value):

        pass


class Leds(object):

    def __init__(self):
        self.leds = OrderedDict()
        self.led_groups = OrderedDict()
        self.led_colors = LED_COLORS
        self.animate_thread_id = None
        self.animate_thread_stop = False

        for (key, value) in LEDS.items():
            self.leds[key] = Led(name_pattern=value, desc=key)

        for (key, value) in LED_GROUPS.items():
            self.led_groups[key] = []

            for led_name in value:
                self.led_groups[key].append(self.leds[led_name])


    def __str__(self):
        return self.__class__.__name__


    def set_color(self, group, color, pct=1):
        """
        Sets brightness of LEDs in the given group to the values specified in
        color tuple. When percentage is specified, brightness of each LED is
        reduced proportionally.

        Example::

            my_leds = Leds()
            my_leds.set_color('LEFT', 'AMBER')

        With a custom color::

            my_leds = Leds()
            my_leds.set_color('LEFT', (0.5, 0.3))
        """

        pass


    def set(self, group, **kwargs):
        """
        Set attributes for each LED in group.

        Example::

            my_leds = Leds()
            my_leds.set_color('LEFT', brightness_pct=0.5, trigger='timer')
        """

        pass


    def all_off(self):
        """
        Turn all LEDs off
        """

        pass


    def reset(self):
        """
        Put all LEDs back to their default color
        """

        pass


    def animate_stop(self):
        """
        Signal the current animation thread to exit and wait for it to exit
        """

        pass


    def animate_police_lights(self, color1, color2, group1='LEFT', group2='RIGHT', sleeptime=0.5, duration=5, block=True):
        """
        Cycle the ``group1`` and ``group2`` LEDs between ``color1`` and ``color2``
        to give the effect of police lights.  Alternate the ``group1`` and ``group2``
        LEDs every ``sleeptime`` seconds.

        Animate for ``duration`` seconds.  If ``duration`` is None animate for forever.

        Example:

        .. code-block:: python

            from ev3dev2.led import Leds
            leds = Leds()
            leds.animate_police_lights('RED', 'GREEN', sleeptime=0.75, duration=10)
        """

        pass


    def animate_flash(self, color, groups=('LEFT', 'RIGHT'), sleeptime=0.5, duration=5, block=True):
        """
        Turn all LEDs in ``groups`` off/on to ``color`` every ``sleeptime`` seconds

        Animate for ``duration`` seconds.  If ``duration`` is None animate for forever.

        Example:

        .. code-block:: python

            from ev3dev2.led import Leds
            leds = Leds()
            leds.animate_flash('AMBER', sleeptime=0.75, duration=10)
        """

        pass


    def animate_cycle(self, colors, groups=('LEFT', 'RIGHT'), sleeptime=0.5, duration=5, block=True):
        """
        Cycle ``groups`` LEDs through ``colors``. Do this in a loop where
        we display each color for ``sleeptime`` seconds.

        Animate for ``duration`` seconds.  If ``duration`` is None animate for forever.

        Example:

        .. code-block:: python

            from ev3dev2.led import Leds
            leds = Leds()
            leds.animate_cyle(('RED', 'GREEN', 'AMBER'))
        """

        pass


    def animate_rainbow(self, group1='LEFT', group2='RIGHT', increment_by=0.1, sleeptime=0.1, duration=5, block=True):
        """
        Gradually fade from one color to the next

        Animate for ``duration`` seconds.  If ``duration`` is None animate for forever.

        Example:

        .. code-block:: python

            from ev3dev2.led import Leds
            leds = Leds()
            leds.animate_rainbow()
        """

        pass
