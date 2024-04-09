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
import _thread
from collections import OrderedDict
from time import sleep

from ev3dev2 import Device
from ev3dev2._platform.ev3 import LEDS, LED_GROUPS, LED_COLORS, LED_DEFAULT_COLOR
from ev3dev2simulator.connector.led_connector import LedConnector
from ev3dev2.stopwatch import StopWatch


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
        'connector',
    ]


    def __init__(self,
                 name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False,
                 desc=None, **kwargs):
        self.desc = desc
        super(Led, self).__init__(self.SYSTEM_CLASS_NAME, name_pattern, name_exact, **kwargs)
        self._max_brightness = 1
        self._brightness = None
        self._triggers = None
        self._trigger = None
        self._delay_on = None
        self._delay_off = None

        self.connector = LedConnector(name_pattern)


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

        return self._max_brightness


    @property
    def brightness(self):
        """
        Sets the brightness level. Possible values are from 0 to `max_brightness`.
        """

        return self._brightness


    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self.connector.enable(self._brightness)



    @property
    def triggers(self):
        """
        Returns a list of available triggers.
        """
        self._triggers, value = self.get_attr_set(self._triggers, 'trigger')
        return value


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
        # Workaround for ev3dev/ev3dev#225.
        # 'delay_on' and 'delay_off' attributes are created when trigger is set
        # to 'timer', and destroyed when it is set to anything else.
        # This means the file cache may become outdated, and we may have to
        # reopen the file.

        pass


    @property
    def delay_off(self):
        """
        The `timer` trigger will periodically change the LED brightness between
        0 and the current brightness setting. The `off` time can
        be specified via `delay_off` attribute in milliseconds.
        """

        # Workaround for ev3dev/ev3dev#225.
        # 'delay_on' and 'delay_off' attributes are created when trigger is set
        # to 'timer', and destroyed when it is set to anything else.
        # This means the file cache may become outdated, and we may have to
        # reopen the file.

        pass


    @delay_off.setter
    def delay_off(self, value):
        # Workaround for ev3dev/ev3dev#225.
        # 'delay_on' and 'delay_off' attributes are created when trigger is set
        # to 'timer', and destroyed when it is set to anything else.
        # This means the file cache may become outdated, and we may have to
        # reopen the file.

        pass


    @property
    def brightness_pct(self):
        """
        Returns LED brightness as a fraction of max_brightness
        """
        return float(self.brightness) / self.max_brightness


    @brightness_pct.setter
    def brightness_pct(self, value):
        self.brightness = value * self.max_brightness


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
        # If this is a platform without LEDs there is nothing to do
        if not self.leds:
            return

        color_tuple = color
        if isinstance(color, str):
            assert color in self.led_colors, \
                "%s is an invalid LED color, valid choices are %s" % \
                (color, ', '.join(self.led_colors.keys()))
            color_tuple = self.led_colors[color]

        assert group in self.led_groups, \
            "%s is an invalid LED group, valid choices are %s" % \
            (group, ', '.join(self.led_groups.keys()))

        for led, value in zip(self.led_groups[group], color_tuple):
            led.brightness_pct = value * pct


    def set(self, group, **kwargs):
        """
        Set attributes for each LED in group.

        Example::

            my_leds = Leds()
            my_leds.set_color('LEFT', brightness_pct=0.5, trigger='timer')
        """

        # If this is a platform without LEDs there is nothing to do
        if not self.leds:
            return

        assert group in self.led_groups, \
            "%s is an invalid LED group, valid choices are %s" % \
            (group, ', '.join(self.led_groups.keys()))

        for led in self.led_groups[group]:
            for k in kwargs:
                setattr(led, k, kwargs[k])


    def all_off(self):
        """
        Turn all LEDs off
        """

        # If this is a platform without LEDs there is nothing to do
        if not self.leds:
            return

        for led in self.leds.values():
            led.brightness = 0


    def reset(self):
        """
        Put all LEDs back to their default color
        """

        if not self.leds:
            return

        self.animate_stop()

        for group in self.led_groups:
            self.set_color(group, LED_DEFAULT_COLOR)


    def animate_stop(self):
        """
        Signal the current animation thread to exit and wait for it to exit
        """

        if self.animate_thread_id:
            self.animate_thread_stop = True

            while self.animate_thread_id:
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


        def _animate_police_lights():
            self.all_off()
            even = True
            duration_ms = duration * 1000
            stopwatch = StopWatch()
            stopwatch.start()

            while True:
                if even:
                    self.set_color(group1, color1)
                    self.set_color(group2, color2)
                else:
                    self.set_color(group1, color2)
                    self.set_color(group2, color1)

                if self.animate_thread_stop or stopwatch.value_ms >= duration_ms:
                    break

                even = not even
                sleep(sleeptime)

            self.animate_thread_stop = False
            self.animate_thread_id = None


        self.animate_stop()

        if block:
            _animate_police_lights()
        else:
            self.animate_thread_id = _thread.start_new_thread(_animate_police_lights, ())


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


        def _animate_flash():
            even = True
            duration_ms = duration * 1000
            stopwatch = StopWatch()
            stopwatch.start()

            while True:
                if even:
                    for group in groups:
                        self.set_color(group, color)
                else:
                    self.all_off()

                if self.animate_thread_stop or stopwatch.value_ms >= duration_ms:
                    break

                even = not even
                sleep(sleeptime)

            self.animate_thread_stop = False
            self.animate_thread_id = None


        self.animate_stop()

        if block:
            _animate_flash()
        else:
            self.animate_thread_id = _thread.start_new_thread(_animate_flash, ())


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


        def _animate_cycle():
            index = 0
            max_index = len(colors)
            duration_ms = duration * 1000
            stopwatch = StopWatch()
            stopwatch.start()

            while True:
                for group in groups:
                    self.set_color(group, colors[index])

                index += 1

                if index == max_index:
                    index = 0

                if self.animate_thread_stop or stopwatch.value_ms >= duration_ms:
                    break

                sleep(sleeptime)

            self.animate_thread_stop = False
            self.animate_thread_id = None


        self.animate_stop()

        if block:
            _animate_cycle()
        else:
            self.animate_thread_id = _thread.start_new_thread(_animate_cycle, ())


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


        def _animate_rainbow():
            # state 0: (LEFT,RIGHT) from (0,0) to (1,0)...RED
            # state 1: (LEFT,RIGHT) from (1,0) to (1,1)...AMBER
            # state 2: (LEFT,RIGHT) from (1,1) to (0,1)...GREEN
            # state 3: (LEFT,RIGHT) from (0,1) to (0,0)...OFF
            state = 0
            left_value = 0
            right_value = 0
            MIN_VALUE = 0
            MAX_VALUE = 1
            self.all_off()
            duration_ms = duration * 1000
            stopwatch = StopWatch()
            stopwatch.start()

            while True:

                if state == 0:
                    left_value += increment_by
                elif state == 1:
                    right_value += increment_by
                elif state == 2:
                    left_value -= increment_by
                elif state == 3:
                    right_value -= increment_by
                else:
                    raise Exception("Invalid state {}".format(state))

                # Keep left_value and right_value within the MIN/MAX values
                left_value = min(left_value, MAX_VALUE)
                right_value = min(right_value, MAX_VALUE)
                left_value = max(left_value, MIN_VALUE)
                right_value = max(right_value, MIN_VALUE)

                self.set_color(group1, (left_value, right_value))
                self.set_color(group2, (left_value, right_value))

                if state == 0 and left_value == MAX_VALUE:
                    state = 1
                elif state == 1 and right_value == MAX_VALUE:
                    state = 2
                elif state == 2 and left_value == MIN_VALUE:
                    state = 3
                elif state == 3 and right_value == MIN_VALUE:
                    state = 0

                if self.animate_thread_stop or stopwatch.value_ms >= duration_ms:
                    break

                sleep(sleeptime)

            self.animate_thread_stop = False
            self.animate_thread_id = None


        self.animate_stop()

        if block:
            _animate_rainbow()
        else:
            self.animate_thread_id = _thread.start_new_thread(_animate_rainbow, ())
