from ev3dev2.Motor import SpeedPercent, MoveSteering


def main(job_handler):
    m = MoveSteering('OUTPUT_A', 'OUTPUT_B', job_handler)
    m.on_for_degrees(100, SpeedPercent(1), 720, brake=False, block=True)
    print('MAININGGGG')

    pass
