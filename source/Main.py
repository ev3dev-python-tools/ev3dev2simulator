from source.job.JobHandler import JobHandler
from source.job.MoveJob import MoveJob
from source.job.RotateJob import RotateJob


def main(job_handler: JobHandler):
    print('Starting User thread')

    for x in range(60):
        job_handler.put_move_job(MoveJob(1, 0))

    for x in range(60):
        job_handler.put_move_job(MoveJob(0, 1))

    for x in range(60):
        job_handler.put_rotate_job(RotateJob(1))

    pass
