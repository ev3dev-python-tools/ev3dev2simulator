from ev3dev2.util.Singleton import Singleton
from simulator.util.Util import load_config
from source.simulator.job.MoveJob import MoveJob


class JobCreator(metaclass=Singleton):

    def __init__(self, job_handler):
        cfg = load_config()
        self.frames_per_second = cfg['exec_settings']['frames_per_second']
        self.job_handler = job_handler

    def create_arm_job(self):
        pass

    def create_single_job_left(self,
                               velocity: float,
                               distance: float):
        frames = self._frames_required(velocity, distance)
        pixels_per_frame = self._to_pixels_per_frame(frames, distance)

        self.create_jobs(frames, pixels_per_frame, 0)

    def create_single_job_right(self,
                                velocity: float,
                                distance: float):
        frames = self._frames_required(velocity, distance)
        pixels_per_frame = self._to_pixels_per_frame(frames, distance)

        self.create_jobs(frames, 0, pixels_per_frame)

    def create_dual_job(self,
                        velocity_max: float,
                        distance_left: float,
                        distance_right: float):
        distance_max = max(distance_left, distance_right)
        frames = self._frames_required(velocity_max, distance_max)

        ppf_left = self._to_pixels_per_frame(frames, distance_left)
        ppf_right = self._to_pixels_per_frame(frames, distance_right)

        self.create_jobs(frames, ppf_left, ppf_right)

    def _to_pixels_per_frame(self, frames, distance):
        pixel_distance = self._to_pixels(distance)
        return pixel_distance / frames

    def _to_pixels(self, distance: float):
        return distance / 1

    def _frames_required(self, velocity, distance):
        seconds = distance / velocity
        return int(round(seconds * self.frames_per_second))

    def create_jobs(self, frames, ppf_left, ppf_right):
        for i in range(frames):
            self.job_handler.put_move_job(MoveJob(ppf_left, ppf_right))
