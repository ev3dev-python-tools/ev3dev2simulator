import sys

from ev3dev2.sensor import Sensor
from ev3dev2.util.SensorConnector import SensorConnector

if sys.version_info < (3, 4):
    raise SystemError('Must be using Python 3.4 or higher')


class MockColorSensor(Sensor):
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


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(MockColorSensor, self).__init__(address, name_pattern, name_exact, driver_name='lego-ev3-color', **kwargs)

        # See calibrate_white() for more details
        self.red_max = 300
        self.green_max = 300
        self.blue_max = 300

        self.connector = SensorConnector(self.address)


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
