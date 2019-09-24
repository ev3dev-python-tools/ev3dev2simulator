from ev3dev2.sound import Sound


def main():
    # m = MoveTank('OUTPUT_A', 'OUTPUT_B')
    # # m.on_for_degrees(SpeedPercent(60), SpeedPercent(60), 100, brake=True, block=False)
    # # # m.on_for_degrees(SpeedPercent(20), SpeedPercent(20), 1500, brake=True, block=False)
    # #
    # # time.sleep(1)
    # # m.stop(brake=False)
    #
    # m.on_for_degrees(SpeedPercent(80), SpeedPercent(-80), 80, brake=True, block=False)
    # # time.sleep(0.5)
    # # m.stop(brake=False)
    #
    # m.on_for_degrees(SpeedPercent(30), SpeedPercent(30), 1000, brake=False, block=False)
    #
    s = Sound()
    s.speak('HALLOOOOOOOOOOO!')

    print('fg')

    # cs = ColorSensor('INPUT_3')
    # while True:
    #     if cs.color != 0:
    #         print(cs.color)
