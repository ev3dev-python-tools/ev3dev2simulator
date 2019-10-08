from ev3dev2.sensor import Sensor
from ev3dev2.simulator.connector.SensorConnector import SensorConnector
from ev3dev2.simulator.util.Util import get_cm_multiplier, get_inch_multiplier


class MockUltrasonicSensor(Sensor):
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


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(MockUltrasonicSensor, self).__init__(address, name_pattern, name_exact,
                                                   driver_name=['lego-ev3-us', 'lego-nxt-us'], **kwargs)

        self.connector = SensorConnector(address)


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
