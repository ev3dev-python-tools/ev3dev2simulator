from _queue import Empty
from queue import Queue

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

        self.should_reset = False
        self.values = {}


    def next_left_move_job(self) -> float:
        """
        Get the next move job for the left motor from the queue.
        :return: a MoveJob object containing the job.
        """

        try:
            return self.left_move_queue.get_nowait()
        except Empty:
            return None


    def next_right_move_job(self) -> float:
        """
        Get the next move job for the right motor from the queue.
        :return: a MoveJob object containing the job.
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


robot_state = RobotState()


def get_robot_state():
    return robot_state
