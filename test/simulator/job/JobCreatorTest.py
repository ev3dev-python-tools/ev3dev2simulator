import unittest

from simulator.job.JobCreator import JobCreator
from simulator.job.JobHandler import get_job_handler


class JobCreatorTest(unittest.TestCase):

    def test_create_jobs_left(self):
        job_handler = get_job_handler()
        job_creator = JobCreator(job_handler)

        job_creator.create_jobs(20, 100, 'hold', 'left')
        for i in range(300):
            job = job_handler.next_left_move_job()
            self.assertAlmostEqual(job.distance, 0.106, 3)

        self.assertIsNone(job_handler.next_left_move_job())
        self.assertIsNone(job_handler.next_right_move_job())


    def test_create_jobs_right(self):
        job_handler = get_job_handler()
        job_creator = JobCreator(job_handler)

        job_creator.create_jobs(80, 200, 'hold', 'right')
        for i in range(150):
            job = job_handler.next_right_move_job()
            self.assertAlmostEqual(job.distance, 0.426, 3)

        self.assertIsNone(job_handler.next_left_move_job())
        self.assertIsNone(job_handler.next_right_move_job())


    def test_create_jobs_coast(self):
        job_handler = get_job_handler()
        job_creator = JobCreator(job_handler)

        job_creator.create_jobs(20, 100, 'coast', 'left')
        for i in range(300):
            job = job_handler.next_left_move_job()
            self.assertAlmostEqual(job.distance, 0.106, 3)

        ppf = 0.106 - 0.05
        for i in range(2):
            job = job_handler.next_left_move_job()
            self.assertAlmostEqual(job.distance, ppf, 3)
            ppf -= 0.05

        self.assertIsNone(job_handler.next_left_move_job())
        self.assertIsNone(job_handler.next_right_move_job())


    def test_frames_required(self):
        job_creator = JobCreator(None)

        frames = job_creator._frames_required(20, 100)
        self.assertEqual(frames, 300)

        frames = job_creator._frames_required(33, 1000)
        self.assertEqual(frames, 1818)


    def test_to_pixels_per_frame(self):
        job_creator = JobCreator(None)

        ppf = job_creator._to_pixels_per_frame(100, 730)
        self.assertAlmostEqual(ppf, 2.332, 3)


    def test_to_pixels(self):
        job_creator = JobCreator(None)

        pixels = job_creator._to_pixels(720)
        self.assertAlmostEqual(pixels, 230)


if __name__ == '__main__':
    unittest.main()
