import sys
import time

from ev3dev2.sensor import Sensor
from ev3dev2.util.SensorConnector import SensorConnector

if sys.version_info < (3, 4):
    raise SystemError('Must be using Python 3.4 or higher')


class MockTouchSensor(Sensor):
    """
    Touch Sensor
    """

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    #: Button state
    MODE_TOUCH = 'TOUCH'
    MODES = (MODE_TOUCH,)


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(MockTouchSensor, self).__init__(address, name_pattern, name_exact,
                                              driver_name=['lego-ev3-touch', 'lego-nxt-touch'], **kwargs)

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
