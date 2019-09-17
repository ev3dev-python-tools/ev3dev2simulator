from ev3dev2.Motor import SpeedPercent, MoveTank


def main(job_handler):
    # job_handler = get_job_handler()
    print('Starting User thread')
    #
    # for x in range(50):
    #     job_handler.put_move_job(MoveJob(0.6, 0.2))
    #
    # for x in range(50):
    #     job_handler.put_move_job(MoveJob(0.6, 0.6))
    # #
    # for x in range(50):
    #     job_handler.put_move_job(MoveJob(0, 1))

    # while True:
    #     print('RUNNINGG')

    print('MAININGGGG')
    m = MoveTank('OUTPUT_A', 'OUTPUT_B', job_handler)
    m.on_for_seconds(SpeedPercent(-40), SpeedPercent(-10), 2, block=False)

    # print('LEL')
    #
    # m.on_for_degrees(SpeedPercent(80), 200000, block=False)

    # for x in range(500):
    #     job_handler.put_move_job(MoveJob(0.6, 0.2))

    pass
