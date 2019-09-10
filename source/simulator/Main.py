from source.simulator.job.JobHandler import JobHandler
from source.simulator.job.MoveJob import MoveJob


def main(job_handler: JobHandler):
    print('Starting User thread')

    for x in range(100):
        job_handler.put_move_job(MoveJob(1, 0, 0))

    for x in range(100):
        job_handler.put_move_job(MoveJob(0, 1, 2))

    pass
