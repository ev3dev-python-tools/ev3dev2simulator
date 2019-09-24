import time

from ev3dev2.Motor import SpeedPercent, MoveTank


def main():
    m = MoveTank('OUTPUT_A', 'OUTPUT_B')
    m.on_for_degrees(SpeedPercent(60), SpeedPercent(60), 100, brake=True, block=False)
    # m.on_for_degrees(SpeedPercent(20), SpeedPercent(20), 1500, brake=True, block=False)

    time.sleep(3)
    m.stop(brake=False)

    # m.on_for_degrees(SpeedPercent(-80), SpeedPercent(80), 360, brake=True, block=False)
    # time.sleep(0.5)
    # m.stop(brake=False)
    #
    # m.on_for_degrees(SpeedPercent(60), SpeedPercent(60), 1000, brake=False, block=False)

    # cs = ColorSensor('INPUT_3')
    # while True:
    #     if cs.color != 0:
    #         print(cs.color)
