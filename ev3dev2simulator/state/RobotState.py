import threading
from queue import Queue, Empty
from typing import Any, Tuple

from ev3dev2simulator.config.config import get_config


class RobotState:
    """
    Class responsible for inner-thread communication. All jobs coming from the robot
    are stored in this class to be retrieved by the simulator for updating/rendering
    of the simulated robot.
    """


    def __init__(self):
        cfg = get_config().get_data()
        large_sim_type = get_config().is_large_sim_type()

        self.address_motor_center = cfg['alloc_settings']['motor']['center'] if large_sim_type else ''
        self.address_motor_left = cfg['alloc_settings']['motor']['left']
        self.address_motor_right = cfg['alloc_settings']['motor']['right']

        self.center_motor_queue = Queue()
        self.left_motor_queue = Queue()
        self.right_motor_queue = Queue()
        self.sound_queue = Queue()

        self.left_brick_left_led_color = 1
        self.left_brick_right_led_color = 1

        self.right_brick_left_led_color = 1
        self.right_brick_right_led_color = 1

        self.should_reset = False

        self.values = {}
        self.locks = {}

        self.motor_lock = threading.Lock()


    def put_center_motor_job(self, job: float):
        """
        Add a new move job to the queue for the center motor.
        :param job: to add.
        """

        self.center_motor_queue.put_nowait(job)


    def put_left_motor_job(self, job: float):
        """
        Add a new move job to the queue for the left motor.
        :param job: to add.
        """

        self.left_motor_queue.put_nowait(job)


    def put_right_motor_job(self, job: float):
        """
        Add a new move job to the queue for the right motor.
        :param job: to add.
        """

        self.right_motor_queue.put_nowait(job)


    def next_motor_jobs(self) -> Tuple[float, float, float]:
        """
        Get the next move jobs for the left and right motor from the queues.
        :return: a floating point numbers representing the job move distances.
        """

        self.motor_lock.acquire()

        try:
            center = self.center_motor_queue.get_nowait()
        except Empty:
            center = None

        try:
            left = self.left_motor_queue.get_nowait()
        except Empty:
            left = None

        try:
            right = self.right_motor_queue.get_nowait()
        except Empty:
            right = None

        self.motor_lock.release()
        return center, left, right


    def clear_motor_jobs(self, side: str):
        self.motor_lock.acquire()

        if side == 'center':
            self.center_motor_queue = Queue()
        elif side == 'left':
            self.left_motor_queue = Queue()
        else:
            self.right_motor_queue = Queue()

        self.motor_lock.release()


    def put_sound_job(self, job: str):
        """
        Add a new sound job to the queue to be displayed.
        :param job: to add.
        """

        self.sound_queue.put_nowait(job)


    def next_sound_job(self) -> str:
        """
        Get the next sound job from the queue.
        :return: a str representing the sound as text to be displayed.
        """

        try:
            return self.sound_queue.get_nowait()
        except Empty:
            return None


    def set_led_color(self, brick_name, led_id, color):
        if brick_name == 'left_brick:':
            if led_id == 'led0':
                self.left_brick_left_led_color = color
            else:
                self.left_brick_right_led_color = color

        else:
            if led_id == 'led0':
                self.right_brick_left_led_color = color
            else:
                self.right_brick_right_led_color = color


    def reset(self):
        """
        Reset the data of this State
        :return:
        """

        self.clear_motor_jobs('center')
        self.clear_motor_jobs('left')
        self.clear_motor_jobs('right')

        self.values.clear()
        self.should_reset = False


    def get_motor_side(self, address: str) -> str:
        """
        Get the location of the motor on the actual robot based on its address.
        :param address: of the motor
        :return 'center', 'left' or 'right'
        """

        if self.address_motor_center == address:
            return 'center'

        if self.address_motor_left == address:
            return 'left'

        if self.address_motor_right == address:
            return 'right'


    def load_sensor(self, sensor):
        """
        Load the given sensor adding its default value to this state.
        Also create a lock for the given sensor.
        :param sensor: to load.
        """

        self.values[sensor.address] = sensor.get_default_value()
        self.locks[sensor.address] = threading.Lock()


    def release_locks(self):
        """
        Release all the locked sensor locks. This re-allows for reading
        the sensor values.
        """

        for lock in self.locks.values():
            if lock.locked():
                lock.release()


    def get_value(self, address: str) -> Any:
        """
        Get the value of a sensor by its address. Blocks if the lock of
        the requested sensor is not available.
        :param address: of the sensor to get the value from.
        :return: the value of the sensor.
        """

        self.locks[address].acquire()
        return self.values[address]
