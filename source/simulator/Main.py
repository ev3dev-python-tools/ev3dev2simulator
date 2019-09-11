from simulator.job.MoveJob import MoveJob
from source.simulator.job.JobHandler import JobHandler


def main():
    job_handler = JobHandler()
    # print('Starting User thread')
    #
    for x in range(100):
        job_handler.put_move_job(MoveJob(0.6, 0.2))

    for x in range(100):
        job_handler.put_move_job(MoveJob(0.6, 0.6))
    #
    # for x in range(100):
    #     job_handler.put_move_job(MoveJob(0, 1, 2))

    # m = Motor('OUTPUT_1')
    # m.on_for_degrees(SpeedPercent(10), 200, block=False)

    pass
