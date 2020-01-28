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

from ev3dev2.button import ButtonBase
from ev3dev2.sensor import Sensor
from ev3dev2simulator.connector.SensorConnector import SensorConnector
from ev3dev2simulator.util.Util import get_cm_multiplier, get_inch_multiplier


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
        """
        Wait for the touch sensor to be pressed down.
        """

        return self._wait(True, timeout_ms, sleep_ms)


    def wait_for_released(self, timeout_ms=None, sleep_ms=10):
        """
        Wait for the touch sensor to be released.
        """

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
        Reflected light intensity as a percentage (0 to 100). Light on sensor is red.
        """

        pass


    @property
    def ambient_light_intensity(self):
        """
        Ambient light intensity, as a percentage (0 to 100). Light on sensor is dimly lit blue.
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
        Red, green, and blue components of the detected color, as a tuple.

        Officially in the range 0-1020 but the values returned will never be
        that high. We do not yet know why the values returned are low, but
        pointing the color sensor at a well lit sheet of white paper will return
        values in the 250-400 range.
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
        self.mode = self.MODE_US_DIST_CM


    @property
    def distance_centimeters_continuous(self):
        """
        Measurement of the distance detected by the sensor,
        in centimeters.

        The sensor will continue to take measurements so
        they are available for future reads.

        Prefer using the equivalent :meth:`UltrasonicSensor.distance_centimeters` property.
        """

        self._ensure_mode(self.MODE_US_DIST_CM)

        value = self.connector.get_value()
        return value if value == -1 else value * get_cm_multiplier()


    @property
    def distance_centimeters_ping(self):
        """
        Measurement of the distance detected by the sensor,
        in centimeters.

        The sensor will take a single measurement then stop
        broadcasting.

        If you use this property too frequently (e.g. every
        100msec), the sensor will sometimes lock up and writing
        to the mode attribute will return an error. A delay of
        250msec between each usage seems sufficient to keep the
        sensor from locking up.
        """

        # This mode is special; setting the mode causes the sensor to send out
        # a "ping", but the mode isn't actually changed.

        self.mode = self.MODE_US_SI_CM

        value = self.connector.get_value()
        return value if value == -1 else value * get_cm_multiplier()


    @property
    def distance_centimeters(self):
        """
        Measurement of the distance detected by the sensor,
        in centimeters.

        Equivalent to :meth:`UltrasonicSensor.distance_centimeters_continuous`.
        """

        return self.distance_centimeters_continuous


    @property
    def distance_inches_continuous(self):
        """
        Measurement of the distance detected by the sensor,
        in inches.

        The sensor will continue to take measurements so
        they are available for future reads.

        Prefer using the equivalent :meth:`UltrasonicSensor.distance_inches` property.
        """

        self._ensure_mode(self.MODE_US_DIST_IN)

        value = self.connector.get_value()
        return value if value == -1 else value * get_inch_multiplier()


    @property
    def distance_inches_ping(self):
        """
        Measurement of the distance detected by the sensor,
        in inches.

        The sensor will take a single measurement then stop
        broadcasting.

        If you use this property too frequently (e.g. every
        100msec), the sensor will sometimes lock up and writing
        to the mode attribute will return an error. A delay of
        250msec between each usage seems sufficient to keep the
        sensor from locking up.
        """

        # This mode is special; setting the mode causes the sensor to send out
        # a "ping", but the mode isn't actually changed.

        self.mode = self.MODE_US_SI_IN

        value = self.connector.get_value()
        return value if value == -1 else value * get_inch_multiplier()


    @property
    def distance_inches(self):
        """
        Measurement of the distance detected by the sensor,
        in inches.

        Equivalent to :meth:`UltrasonicSensor.distance_inches_continuous`.
        """

        return self.distance_inches_continuous


    @property
    def other_sensor_present(self):
        """
        Boolean indicating whether another ultrasonic sensor could
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


class GyroSensor(Sensor):
    """
    LEGO EV3 gyro sensor.
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    #: Angle
    MODE_GYRO_ANG = 'GYRO-ANG'

    #: Rotational speed
    MODE_GYRO_RATE = 'GYRO-RATE'

    #: Raw sensor value
    MODE_GYRO_FAS = 'GYRO-FAS'

    #: Angle and rotational speed
    MODE_GYRO_G_A = 'GYRO-G&A'

    #: Calibration ???
    MODE_GYRO_CAL = 'GYRO-CAL'

    # Newer versions of the Gyro sensor also have an additional second axis
    # accessible via the TILT-ANG and TILT-RATE modes that is not usable
    # using the official EV3-G blocks
    MODE_TILT_ANG = 'TILT-ANG'
    MODE_TILT_RATE = 'TILT-RATE'

    MODES = (
        MODE_GYRO_ANG,
        MODE_GYRO_RATE,
        MODE_GYRO_FAS,
        MODE_GYRO_G_A,
        MODE_GYRO_CAL,
        MODE_TILT_ANG,
        MODE_TILT_RATE,
    )


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(GyroSensor, self).__init__(address, name_pattern, name_exact, driver_name='lego-ev3-gyro', **kwargs)

        pass


    @property
    def angle(self):
        """
        The number of degrees that the sensor has been rotated
        since it was put into this mode.
        """

        pass


    @property
    def rate(self):
        """
        The rate at which the sensor is rotating, in degrees/second.
        """

        pass


    @property
    def angle_and_rate(self):
        """
        Angle (degrees) and Rotational Speed (degrees/second).
        """

        pass


    @property
    def tilt_angle(self):
        pass


    @property
    def tilt_rate(self):
        pass


    def reset(self):
        """Resets the angle to 0.

        Caveats:
            - This function only resets the angle to 0, it does not fix drift.
            - This function only works on EV3, it does not work on BrickPi,
              PiStorms, or with any sensor multiplexors.
        """

        pass


    def wait_until_angle_changed_by(self, delta, direction_sensitive=False):
        """
        Wait until angle has changed by specified amount.

        If ``direction_sensitive`` is True we will wait until angle has changed
        by ``delta`` and with the correct sign.

        If ``direction_sensitive`` is False (default) we will wait until angle has changed
        by ``delta`` in either direction.
        """

        pass


class InfraredSensor(Sensor, ButtonBase):
    """
    LEGO EV3 infrared sensor.
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    #: Proximity
    MODE_IR_PROX = 'IR-PROX'

    #: IR Seeker
    MODE_IR_SEEK = 'IR-SEEK'

    #: IR Remote Control
    MODE_IR_REMOTE = 'IR-REMOTE'

    #: IR Remote Control. State of the buttons is coded in binary
    MODE_IR_REM_A = 'IR-REM-A'

    #: Calibration ???
    MODE_IR_CAL = 'IR-CAL'

    MODES = (
        MODE_IR_PROX,
        MODE_IR_SEEK,
        MODE_IR_REMOTE,
        MODE_IR_REM_A,
        MODE_IR_CAL
    )

    # The following are all of the various combinations of button presses for
    # the remote control.  The key/index is the number that will be written in
    # the attribute file to indicate what combination of buttons are currently
    # pressed.
    _BUTTON_VALUES = {
        0: [],
        1: ['top_left'],
        2: ['bottom_left'],
        3: ['top_right'],
        4: ['bottom_right'],
        5: ['top_left', 'top_right'],
        6: ['top_left', 'bottom_right'],
        7: ['bottom_left', 'top_right'],
        8: ['bottom_left', 'bottom_right'],
        9: ['beacon'],
        10: ['top_left', 'bottom_left'],
        11: ['top_right', 'bottom_right']
    }

    _BUTTONS = ('top_left', 'bottom_left', 'top_right', 'bottom_right', 'beacon')

    # Button codes for doing rapid check of remote status
    NO_BUTTON = 0
    TOP_LEFT = 1
    BOTTOM_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_RIGHT = 4
    TOP_LEFT_TOP_RIGHT = 5
    TOP_LEFT_BOTTOM_RIGHT = 6
    BOTTOM_LEFT_TOP_RIGHT = 7
    BOTTOM_LEFT_BOTTOM_RIGHT = 8
    BEACON = 9
    TOP_LEFT_BOTTOM_LEFT = 10
    TOP_RIGHT_BOTTOM_RIGHT = 11

    #: Handler for top-left button events on channel 1. See :meth:`InfraredSensor.process`.
    on_channel1_top_left = None
    #: Handler for bottom-left button events on channel 1. See :meth:`InfraredSensor.process`.
    on_channel1_bottom_left = None
    #: Handler for top-right button events on channel 1. See :meth:`InfraredSensor.process`.
    on_channel1_top_right = None
    #: Handler for bottom-right button events on channel 1. See :meth:`InfraredSensor.process`.
    on_channel1_bottom_right = None
    #: Handler for beacon button events on channel 1. See :meth:`InfraredSensor.process`.
    on_channel1_beacon = None

    #: Handler for top-left button events on channel 2. See :meth:`InfraredSensor.process`.
    on_channel2_top_left = None
    #: Handler for bottom-left button events on channel 2. See :meth:`InfraredSensor.process`.
    on_channel2_bottom_left = None
    #: Handler for top-right button events on channel 2. See :meth:`InfraredSensor.process`.
    on_channel2_top_right = None
    #: Handler for bottom-right button events on channel 2. See :meth:`InfraredSensor.process`.
    on_channel2_bottom_right = None
    #: Handler for beacon button events on channel 2. See :meth:`InfraredSensor.process`.
    on_channel2_beacon = None

    #: Handler for top-left button events on channel 3. See :meth:`InfraredSensor.process`.
    on_channel3_top_left = None
    #: Handler for bottom-left button events on channel 3. See :meth:`InfraredSensor.process`.
    on_channel3_bottom_left = None
    #: Handler for top-right button events on channel 3. See :meth:`InfraredSensor.process`.
    on_channel3_top_right = None
    #: Handler for bottom-right button events on channel 3. See :meth:`InfraredSensor.process`.
    on_channel3_bottom_right = None
    #: Handler for beacon button events on channel 3. See :meth:`InfraredSensor.process`.
    on_channel3_beacon = None

    #: Handler for top-left button events on channel 4. See :meth:`InfraredSensor.process`.
    on_channel4_top_left = None
    #: Handler for bottom-left button events on channel 4. See :meth:`InfraredSensor.process`.
    on_channel4_bottom_left = None
    #: Handler for top-right button events on channel 4. See :meth:`InfraredSensor.process`.
    on_channel4_top_right = None
    #: Handler for bottom-right button events on channel 4. See :meth:`InfraredSensor.process`.
    on_channel4_bottom_right = None
    #: Handler for beacon button events on channel 4. See :meth:`InfraredSensor.process`.
    on_channel4_beacon = None


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(InfraredSensor, self).__init__(address, name_pattern, name_exact, driver_name='lego-ev3-ir', **kwargs)


    def _normalize_channel(self, channel):
        pass


    @property
    def proximity(self):
        """
        An estimate of the distance between the sensor and objects in front of
        it, as a percentage. 100% is approximately 70cm/27in.
        """

        pass


    def heading(self, channel=1):
        """
        Returns heading (-25, 25) to the beacon on the given channel.
        """

        pass


    def distance(self, channel=1):
        """
        Returns distance (0, 100) to the beacon on the given channel.
        Returns None when beacon is not found.
        """

        pass


    def heading_and_distance(self, channel=1):
        """
        Returns heading and distance to the beacon on the given channel as a
        tuple.
        """

        pass


    def top_left(self, channel=1):
        """
        Checks if ``top_left`` button is pressed.
        """

        pass


    def bottom_left(self, channel=1):
        """
        Checks if ``bottom_left`` button is pressed.
        """

        pass


    def top_right(self, channel=1):
        """
        Checks if ``top_right`` button is pressed.
        """

        pass


    def bottom_right(self, channel=1):
        """
        Checks if ``bottom_right`` button is pressed.
        """

        pass


    def beacon(self, channel=1):
        """
        Checks if ``beacon`` button is pressed.
        """

        pass


    def buttons_pressed(self, channel=1):
        """
        Returns list of currently pressed buttons.

        Note that the sensor can only identify up to two buttons pressed at once.
        """

        pass


    def process(self):
        """
        Check for currenly pressed buttons. If the new state differs from the
        old state, call the appropriate button event handlers.

        To use the on_channel1_top_left, etc handlers your program would do something like:

        .. code:: python

            def top_left_channel_1_action(state):
                print("top left on channel 1: %s" % state)

            def bottom_right_channel_4_action(state):
                print("bottom right on channel 4: %s" % state)

            ir = InfraredSensor()
            ir.on_channel1_top_left = top_left_channel_1_action
            ir.on_channel4_bottom_right = bottom_right_channel_4_action

            while True:
                ir.process()
                time.sleep(0.01)

        """

        pass


class SoundSensor(Sensor):
    """
    LEGO NXT Sound Sensor
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    #: Sound pressure level. Flat weighting
    MODE_DB = 'DB'

    #: Sound pressure level. A weighting
    MODE_DBA = 'DBA'

    MODES = (
        MODE_DB,
        MODE_DBA,
    )


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(SoundSensor, self).__init__(address, name_pattern, name_exact, driver_name='lego-nxt-sound', **kwargs)


    @property
    def sound_pressure(self):
        """
        A measurement of the measured sound pressure level, as a
        percent. Uses a flat weighting.
        """

        pass


    @property
    def sound_pressure_low(self):
        """
        A measurement of the measured sound pressure level, as a
        percent. Uses A-weighting, which focuses on levels up to 55 dB.
        """

        pass


class LightSensor(Sensor):
    """
    LEGO NXT Light Sensor
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    #: Reflected light. LED on
    MODE_REFLECT = 'REFLECT'

    #: Ambient light. LED off
    MODE_AMBIENT = 'AMBIENT'

    MODES = (
        MODE_REFLECT,
        MODE_AMBIENT,
    )


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(LightSensor, self).__init__(address, name_pattern, name_exact, driver_name='lego-nxt-light', **kwargs)


    @property
    def reflected_light_intensity(self):
        """
        A measurement of the reflected light intensity, as a percentage.
        """

        pass


    @property
    def ambient_light_intensity(self):
        """
        A measurement of the ambient light intensity, as a percentage.
        """

        pass
