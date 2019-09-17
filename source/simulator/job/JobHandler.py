from _queue import Empty
from queue import Queue

from source.simulator.job.MoveJob import MoveJob


class JobHandler:
    """
    Class responsible for inner-thread communication. All jobs coming from the robot
    are stored in this class to be retrieved by the simulator for updating/rendering
    of the simulated robot.
    """


    def __init__(self):
        self.left_move_queue = Queue()
        self.right_move_queue = Queue()


    def next_left_move_job(self) -> MoveJob:
        """
        Get the next move job for the left motor from the queue.
        :return: a MoveJob object containing the job.
        """

        try:
            return self.left_move_queue.get_nowait()
        except Empty:
            return None


    def next_right_move_job(self) -> MoveJob:
        """
        Get the next move job for the right motor from the queue.
        :return: a MoveJob object containing the job.
        """

        try:
            return self.right_move_queue.get_nowait()
        except Empty:
            return None


    def put_left_move_job(self, job: MoveJob):
        """
        Add a new move job for the left motor to the queue.
        :param job: to add.
        """

        self.left_move_queue.put_nowait(job)


    def put_right_move_job(self, job: MoveJob):
        """
        Add a new move job for the left motor to the queue.
        :param job
        """

        self.right_move_queue.put_nowait(job)


job_handler = JobHandler()


def get_job_handler():
    return job_handler
