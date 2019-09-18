from ev3dev2.util.Singleton import Singleton
from simulator.util.Util import load_config
from source.simulator.job.MoveJob import MoveJob

COASTING_SUB = 0.03


class JobCreator(metaclass=Singleton):
    """
    The JobCreator class is responsible for creating movement jobs for the simulated robot.
    These jobs are processed by the simulator every update. The Python Arcade library used
    for the simulator provides a logic update every frame. Meaning 'frames_per_second' number of jobs
    are processed per second.
    """


    def __init__(self, job_handler):
        cfg = load_config()

        self.frames_per_second = cfg['exec_settings']['frames_per_second']
        self.wheel_circumference = cfg['wheel_settings']['circumference']

        self.job_handler = job_handler


    def create_jobs(self, speed: float, distance: float, stop_action: str, side: str) -> float:
        """
        Create the jobs required to rotate the motor of the robot for a distance at a speed.
        :param speed: in degrees per second.
        :param distance: in degrees.
        :param stop_action: of the motor, this can be 'hold' or 'coast'.
        :param side: location of the motor, 'left', 'right' or 'center'.
        """

        frames = self._frames_required(speed, distance)
        pixels_per_frame = self._to_pixels_per_frame(frames, distance)

        self._create_move_jobs(frames, pixels_per_frame, side)

        if stop_action == 'coast':
            coast_frames = int(round(pixels_per_frame / COASTING_SUB))
            self._create_move_jobs_coast(coast_frames, pixels_per_frame, side)

            return (frames + coast_frames) / self.frames_per_second

        return frames / self.frames_per_second


    def _frames_required(self, speed: float, distance: float) -> int:
        """
        Calculate the number of frames required to rotate a motor for a distance at a speed.
        :param speed: in degrees per second.
        :param distance: in degrees.
        :return: an integer representing the number of frames.
        """

        seconds = abs(distance) / abs(speed)
        return int(round(seconds * self.frames_per_second))


    def _to_pixels_per_frame(self, frames: int, distance: float) -> float:
        """
        Calculate the number of pixels required per frame to rotate a motor a distance within frames.
        :param frames: available.
        :param distance: in degrees.
        :return: an floating point number representing the number of pixels per frame.
        """

        pixel_distance = self._to_pixels(distance)
        return pixel_distance / frames


    def _to_pixels(self, distance: float) -> float:
        """
        Convert a distance in degrees to a distance in pixels. Calculation is done
        based on the circumference of the wheel attached to the motor.
        :param distance: in degrees.
        :return: an integer representing the distance in pixels.
        """

        return self.wheel_circumference * (distance / 360)


    def _create_move_jobs(self, frames: int, ppf: float, side: str):
        """
        Create a movement job for the motor for every frame.
        :param frames: to create jobs for.
        :param ppf: distance in pixels per frame.
        :param side: location of the motor, 'left', 'right' or 'center'.
        """

        for i in range(frames):
            if side == 'left':
                self.job_handler.put_left_move_job(MoveJob(ppf))
            else:
                self.job_handler.put_right_move_job(MoveJob(ppf))


    def _create_move_jobs_coast(self, frames: int, ppf: float, side: str):
        """
        Create a number of move jobs for the motor based on coasting speed subtraction.
        Every move job contains a smaller travel distance until the motor does not move anymore.
        :param frames: to create jobs for.
        :param ppf: speed in pixels per frame before coasting starts.
        :param side: location of the motor, 'left', 'right' or 'center'.
        """

        for i in range(frames):
            ppf = max(ppf - COASTING_SUB, 0)

            if side == 'left':
                self.job_handler.put_left_move_job(MoveJob(ppf))
            else:
                self.job_handler.put_right_move_job(MoveJob(ppf))
