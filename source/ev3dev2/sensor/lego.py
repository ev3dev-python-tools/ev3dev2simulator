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
import time

from ev3dev2.sensor import Sensor
from ev3dev2.simulator.connector.SensorConnector import SensorConnector
from ev3dev2.simulator.util.Util import get_cm_multiplier, get_inch_multiplier


class ColorSensor(Sensor):
    """
    LEGO EV3 color sensor.
    """

    __slots__ = ['red_max', 'green_max', 'blue_max', 'connector']

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    #: Reflected light. Red LED on.
    MODE_COL_REFLECT = 'COL-REFLECT'

    #: Ambient light. Blue LEDs on.
    MODE_COL_AMBIENT = 'COL-AMBIENT'

    #: Color. All LEDs rapidly cycling, appears white.
    MODE_COL_COLOR = 'COL-COLOR'

    #: Raw reflected. Red LED on
    MODE_REF_RAW = 'REF-RAW'

    #: Raw Color Components. All LEDs rapidly cycling, appears white.
    MODE_RGB_RAW = 'RGB-RAW'

    #: No color.
    COLOR_NOCOLOR = 0

    #: Black color.
    COLOR_BLACK = 1

    #: Blue color.
    COLOR_BLUE = 2

    #: Green color.
    COLOR_GREEN = 3

    #: Yellow color.
    COLOR_YELLOW = 4

    #: Red color.
    COLOR_RED = 5

    #: White color.
    COLOR_WHITE = 6

    #: Brown color.
    COLOR_BROWN = 7

    MODES = (
        MODE_COL_REFLECT,
        MODE_COL_AMBIENT,
        MODE_COL_COLOR,
        MODE_REF_RAW,
        MODE_RGB_RAW
    )

    COLORS = (
        'NoColor',
        'Black',
        'Blue',
        'Green',
        'Yellow',
        'Red',
        'White',
        'Brown',
    )


    def __init__(self, address, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(ColorSensor, self).__init__(address, name_pattern, name_exact, driver_name='lego-ev3-color', **kwargs)

        # See calibrate_white() for more details
        self.red_max = 300
        self.green_max = 300
        self.blue_max = 300

        self.connector = SensorConnector(address)


    @property
    def reflected_light_intensity(self):
        """
        Reflected light intensity as a percentage. Light on sensor is red.
        """

        pass


    @property
    def ambient_light_intensity(self):
        """
        Ambient light intensity. Light on sensor is dimly lit blue.
        """

        pass


    @property
    def color(self):
        """
        Color detected by the sensor, categorized by overall value.
          - 0: No color
          - 1: Black
          - 2: Blue
          - 3: Green
          - 4: Yellow
          - 5: Red
          - 6: White
          - 7: Brown
        """

        self._ensure_mode(self.MODE_COL_COLOR)
        return self.connector.get_value()


    @property
    def color_name(self):
        """
        Returns NoColor, Black, Blue, etc
        """

        return self.COLORS[self.connector.get_value()]


    @property
    def raw(self):
        """
        Red, green, and blue components of the detected color, officially in the
        range 0-1020 but the values returned will never be that high. We do not
        yet know why the values returned are low, but pointing the color sensor
        at a well lit sheet of white paper will return values in the 250-400 range.

        If this is an issue, check out the rgb() and calibrate_white() methods.
        """

        pass


    def calibrate_white(self):
        """
        The RGB raw values are on a scale of 0-1020 but you never see a value
        anywhere close to 1020.  This function is designed to be called when
        the sensor is placed over a white object in order to figure out what
        are the maximum RGB values the robot can expect to see.  We will use
        these maximum values to scale future raw values to a 0-255 range in
        rgb().

        If you never call this function red_max, green_max, and blue_max will
        use a default value of 300.  This default was selected by measuring
        the RGB values of a white sheet of paper in a well lit room.

        Note that there are several variables that influence the maximum RGB
        values detected by the color sensor
        - the distance of the color sensor to the white object
        - the amount of light in the room
        - shadows that the robot casts on the sensor
        """

        pass


    @property
    def rgb(self):
        """
        Same as raw() but RGB values are scaled to 0-255
        """

        pass


    @property
    def lab(self):
        """
        Return colors in Lab color space
        """

        pass


    @property
    def hsv(self):
        """
        HSV: Hue, Saturation, Value
        H: position in the spectrum
        S: color saturation ("purity")
        V: color brightness
        """

        pass


    @property
    def hls(self):
        """
        HLS: Hue, Luminance, Saturation
        H: position in the spectrum
        L: color lightness
        S: color saturation
        """

        pass


    @property
    def red(self):
        """
        Red component of the detected color, in the range 0-1020.
        """

        pass


    @property
    def green(self):
        """
        Green component of the detected color, in the range 0-1020.
        """

        pass


    @property
    def blue(self):
        """
        Blue component of the detected color, in the range 0-1020.
        """

        pass


    def value(self, n=0):
        """
        Returns the value or values measured by the sensor. Check num_values to
        see how many values there are. Values with N >= num_values will return
        an error. The values are fixed point numbers, so check decimals to see
        if you need to divide to get the actual value.
        """

        return self.color()


class TouchSensor(Sensor):
    """
    Touch Sensor
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    #: Button state
    MODE_TOUCH = 'TOUCH'
    MODES = (MODE_TOUCH,)


    def __init__(self, address, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(TouchSensor, self).__init__(address, name_pattern, name_exact, driver_name=['lego-ev3-touch', 'lego-nxt-touch'], **kwargs)

        self.connector = SensorConnector(address)


    @property
    def is_pressed(self):
        """
        A boolean indicating whether the current touch sensor is being
        pressed.
        """

        self._ensure_mode(self.MODE_TOUCH)
        return self.connector.get_value()


    @property
    def is_released(self):
        return not self.is_pressed


    def _wait(self, wait_for_press, timeout_ms, sleep_ms):
        tic = time.time()

        if sleep_ms:
            sleep_ms = float(sleep_ms / 1000)

        # The kernel does not supoort POLLPRI or POLLIN for sensors so we have
        # to drop into a loop and check often
        while True:

            if self.is_pressed == wait_for_press:
                return True

            if timeout_ms is not None and time.time() >= tic + timeout_ms / 1000:
                return False

            if sleep_ms:
                time.sleep(sleep_ms)


    def wait_for_pressed(self, timeout_ms=None, sleep_ms=10):
        return self._wait(True, timeout_ms, sleep_ms)


    def wait_for_released(self, timeout_ms=None, sleep_ms=10):
        return self._wait(False, timeout_ms, sleep_ms)


    def wait_for_bump(self, timeout_ms=None, sleep_ms=10):
        """
        Wait for the touch sensor to be pressed down and then released.
        Both actions must happen within timeout_ms.
        """
        start_time = time.time()

        if self.wait_for_pressed(timeout_ms, sleep_ms):
            if timeout_ms is not None:
                timeout_ms -= int((time.time() - start_time) * 1000)
            return self.wait_for_released(timeout_ms, sleep_ms)

        return False


    def value(self, n=0):
        """
        Returns the value or values measured by the sensor. Check num_values to
        see how many values there are. Values with N >= num_values will return
        an error. The values are fixed point numbers, so check decimals to see
        if you need to divide to get the actual value.
        """

        return self.is_pressed()


class UltrasonicSensor(Sensor):
    """
    LEGO EV3 ultrasonic sensor.
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    #: Continuous measurement in centimeters.
    MODE_US_DIST_CM = 'US-DIST-CM'

    #: Continuous measurement in inches.
    MODE_US_DIST_IN = 'US-DIST-IN'

    #: Listen.
    MODE_US_LISTEN = 'US-LISTEN'

    #: Single measurement in centimeters.
    MODE_US_SI_CM = 'US-SI-CM'

    #: Single measurement in inches.
    MODE_US_SI_IN = 'US-SI-IN'

    MODES = (
        MODE_US_DIST_CM,
        MODE_US_DIST_IN,
        MODE_US_LISTEN,
        MODE_US_SI_CM,
        MODE_US_SI_IN,
    )


    def __init__(self, address, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(UltrasonicSensor, self).__init__(address, name_pattern, name_exact, driver_name=['lego-ev3-us', 'lego-nxt-us'], **kwargs)

        self.connector = SensorConnector(address)


    @property
    def distance_centimeters_continuous(self):
        self._ensure_mode(self.MODE_US_DIST_CM)

        value = self.connector.get_value()
        return value if value == -1 else value * get_cm_multiplier()


    @property
    def distance_centimeters_ping(self):
        self.mode = self.MODE_US_SI_CM

        value = self.connector.get_value()
        return value if value == -1 else value * get_cm_multiplier()


    @property
    def distance_centimeters(self):
        """
        Measurement of the distance detected by the sensor,
        in centimeters.
        """
        return self.distance_centimeters_continuous


    @property
    def distance_inches_continuous(self):
        self._ensure_mode(self.MODE_US_DIST_IN)

        value = self.connector.get_value()
        return value if value == -1 else value * get_inch_multiplier()


    @property
    def distance_inches_ping(self):
        self._ensure_mode(self.MODE_US_DIST_IN)

        value = self.connector.get_value()
        return value if value == -1 else value * get_inch_multiplier()


    @property
    def distance_inches(self):
        """
        Measurement of the distance detected by the sensor,
        in inches.
        """
        return self.distance_inches_continuous


    @property
    def other_sensor_present(self):
        """
        Value indicating whether another ultrasonic sensor could
        be heard nearby.
        """

        pass


    def value(self, n=0):
        """
        Returns the value or values measured by the sensor. Check num_values to
        see how many values there are. Values with N >= num_values will return
        an error. The values are fixed point numbers, so check decimals to see
        if you need to divide to get the actual value.
        """

        if self.mode == self.MODE_US_DIST_CM \
                or self.mode == self.MODE_US_SI_IN:
            return self.distance_centimeters_continuous * 10

        elif self.mode == self.MODE_US_DIST_IN \
                or self.mode == self.MODE_US_SI_IN:
            return self.distance_inches_continuous * 10
