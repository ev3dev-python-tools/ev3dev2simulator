import sys

from ev3dev2.util.ColorSensorConnector import ColorSensorConnector

if sys.version_info < (3, 4):
    raise SystemError('Must be using Python 3.4 or higher')

from ev3dev2.sensor import Sensor


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


    def __init__(self, address, sensor_handler, **kwargs):
        super(MockColorSensor, self).__init__(address, **kwargs)

        # See calibrate_white() for more details
        self.red_max = 300
        self.green_max = 300
        self.blue_max = 300

        self.connector = ColorSensorConnector(sensor_handler)


    @property
    def reflected_light_intensity(self):
        """
        Reflected light intensity as a percentage (0 to 100). Light on sensor is red.
        """
        self._ensure_mode(self.MODE_COL_REFLECT)
        return self.value(0)


    @property
    def ambient_light_intensity(self):
        """
        Ambient light intensity, as a percentage (0 to 100). Light on sensor is dimly lit blue.
        """
        self._ensure_mode(self.MODE_COL_AMBIENT)
        return self.value(0)


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
        # return self.value(0)
        return self.connector.get_color(self.address)


    @property
    def color_name(self):
        """
        Returns NoColor, Black, Blue, etc
        """
        return self.COLORS[self.color]


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
        self._ensure_mode(self.MODE_RGB_RAW)
        return self.value(0), self.value(1), self.value(2)


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
        (self.red_max, self.green_max, self.blue_max) = self.raw


    @property
    def rgb(self):
        """
        Same as raw() but RGB values are scaled to 0-255
        """
        (red, green, blue) = self.raw

        return (min(int((red * 255) / self.red_max), 255),
                min(int((green * 255) / self.green_max), 255),
                min(int((blue * 255) / self.blue_max), 255))


    @property
    def lab(self):
        """
        Return colors in Lab color space
        """
        RGB = [0, 0, 0]
        XYZ = [0, 0, 0]

        for (num, value) in enumerate(self.rgb):
            if value > 0.04045:
                value = pow(((value + 0.055) / 1.055), 2.4)
            else:
                value = value / 12.92

            RGB[num] = value * 100.0

        # http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
        # sRGB
        # 0.4124564  0.3575761  0.1804375
        # 0.2126729  0.7151522  0.0721750
        # 0.0193339  0.1191920  0.9503041
        X = (RGB[0] * 0.4124564) + (RGB[1] * 0.3575761) + (RGB[2] * 0.1804375)
        Y = (RGB[0] * 0.2126729) + (RGB[1] * 0.7151522) + (RGB[2] * 0.0721750)
        Z = (RGB[0] * 0.0193339) + (RGB[1] * 0.1191920) + (RGB[2] * 0.9503041)

        XYZ[0] = X / 95.047  # ref_X =  95.047
        XYZ[1] = Y / 100.0  # ref_Y = 100.000
        XYZ[2] = Z / 108.883  # ref_Z = 108.883

        for (num, value) in enumerate(XYZ):
            if value > 0.008856:
                value = pow(value, (1.0 / 3.0))
            else:
                value = (7.787 * value) + (16 / 116.0)

            XYZ[num] = value

        L = (116.0 * XYZ[1]) - 16
        a = 500.0 * (XYZ[0] - XYZ[1])
        b = 200.0 * (XYZ[1] - XYZ[2])

        L = round(L, 4)
        a = round(a, 4)
        b = round(b, 4)

        return (L, a, b)


    @property
    def hsv(self):
        """
        HSV: Hue, Saturation, Value
        H: position in the spectrum
        S: color saturation ("purity")
        V: color brightness
        """
        (r, g, b) = self.rgb
        maxc = max(r, g, b)
        minc = min(r, g, b)
        v = maxc

        if minc == maxc:
            return 0.0, 0.0, v

        s = (maxc - minc) / maxc
        rc = (maxc - r) / (maxc - minc)
        gc = (maxc - g) / (maxc - minc)
        bc = (maxc - b) / (maxc - minc)

        if r == maxc:
            h = bc - gc
        elif g == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc

        h = (h / 6.0) % 1.0

        return (h, s, v)


    @property
    def hls(self):
        """
        HLS: Hue, Luminance, Saturation
        H: position in the spectrum
        L: color lightness
        S: color saturation
        """
        (r, g, b) = self.rgb
        maxc = max(r, g, b)
        minc = min(r, g, b)
        l = (minc + maxc) / 2.0

        if minc == maxc:
            return 0.0, l, 0.0

        if l <= 0.5:
            s = (maxc - minc) / (maxc + minc)
        else:
            if 2.0 - maxc - minc == 0:
                s = 0
            else:
                s = (maxc - minc) / (2.0 - maxc - minc)

        rc = (maxc - r) / (maxc - minc)
        gc = (maxc - g) / (maxc - minc)
        bc = (maxc - b) / (maxc - minc)

        if r == maxc:
            h = bc - gc
        elif g == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc

        h = (h / 6.0) % 1.0

        return (h, l, s)


    @property
    def red(self):
        """
        Red component of the detected color, in the range 0-1020.
        """
        self._ensure_mode(self.MODE_RGB_RAW)
        return self.value(0)


    @property
    def green(self):
        """
        Green component of the detected color, in the range 0-1020.
        """
        self._ensure_mode(self.MODE_RGB_RAW)
        return self.value(1)


    @property
    def blue(self):
        """
        Blue component of the detected color, in the range 0-1020.
        """
        self._ensure_mode(self.MODE_RGB_RAW)
        return self.value(2)
