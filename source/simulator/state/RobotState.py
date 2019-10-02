import threading
from _queue import Empty
from queue import Queue
from typing import Any

from simulator.robot import BodyPart
from simulator.util.Util import load_config


class RobotState:
    """
    Class responsible for inner-thread communication. All jobs coming from the robot
    are stored in this class to be retrieved by the simulator for updating/rendering
    of the simulated robot.
    """


    def __init__(self):
        cfg = load_config()

        self.address_motor_center = cfg['alloc_settings']['motor']['center']
        self.address_motor_left = cfg['alloc_settings']['motor']['left']
        self.address_motor_right = cfg['alloc_settings']['motor']['right']

        self.left_move_queue = Queue()
        self.right_move_queue = Queue()
        self.sound_queue = Queue()

        self.should_reset = False

        self.values = {}
        self.locks = {}


    def next_left_move_job(self) -> float:
        """
        Get the next move job for the left motor from the queue.
        :return: a floating point number representing the job move distance.
        """

        try:
            return self.left_move_queue.get_nowait()
        except Empty:
            return None


    def next_right_move_job(self) -> float:
        """
        Get the next move job for the right motor from the queue.
        :return: a floating point number representing the job move distance.
        """

        try:
            return self.right_move_queue.get_nowait()
        except Empty:
            return None


    def put_move_job(self, job: float, side: str):
        """
        Add a new move job to the queue for the motor corresponding to the given side.
        :param job: to add.
        :param side: the motor is located.
        """

        if side == 'left':
            self.left_move_queue.put_nowait(job)
        else:
            self.right_move_queue.put_nowait(job)


    def clear_move_jobs(self, side: str):
        if side == 'left':
            self._clear_left_move_jobs()
        else:
            self._clear_right_move_jobs()


    def _clear_left_move_jobs(self):
        while not self.left_move_queue.empty():
            self.left_move_queue.get_nowait()


    def _clear_right_move_jobs(self):
        while not self.right_move_queue.empty():
            self.right_move_queue.get_nowait()


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


    def reset(self):

        self._clear_left_move_jobs()
        self._clear_right_move_jobs()

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


    def load_sensor(self, sensor: BodyPart):
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


robot_state = RobotState()


def get_robot_state():
    return robot_state
