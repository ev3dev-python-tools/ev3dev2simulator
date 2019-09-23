from _queue import Empty
from queue import Queue


class RobotState:
    """
    Class responsible for inner-thread communication. All jobs coming from the robot
    are stored in this class to be retrieved by the simulator for updating/rendering
    of the simulated robot.
    """


    def __init__(self):
        self.left_move_queue = Queue()
        self.right_move_queue = Queue()

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


    def put_left_move_job(self, job: float):
        """
        Add a new move job for the left motor to the queue.
        :param job: to add.
        """

        self.left_move_queue.put_nowait(job)


    def put_right_move_job(self, job: float):
        """
        Add a new move job for the left motor to the queue.
        :param job
        """

        self.right_move_queue.put_nowait(job)


    def clear_left_jobs(self):
        pass


    def clear_right_jobs(self):
        pass


robot_state = RobotState()


def get_robot_state():
    return robot_state
