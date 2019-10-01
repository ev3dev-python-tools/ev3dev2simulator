from ev3dev2.Motor import MoveTank, SpeedPercent
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound


def main():
    m = MoveTank('OUTPUT_A', 'OUTPUT_B')
    # m.on_for_degrees(SpeedPercent(60), SpeedPercent(60), 100, brake=True, block=False)
    # # # m.on_for_degrees(SpeedPercent(20), SpeedPercent(20), 1500, brake=True, block=False)
    # #
    # # time.sleep(1)
    # # m.stop(brake=False)
    #
    m.on_for_degrees(SpeedPercent(80), SpeedPercent(-80), 80, brake=True, block=False)
    # time.sleep(0.5)
    # m.stop(brake=False)

    m.on_for_degrees(SpeedPercent(5), SpeedPercent(5), 1000, brake=False, block=False)
    #
    s = Sound()
    s.speak('HALLOOOOOOOOOOO!')

    ts = UltrasonicSensor('INPUT_6')
    while True:
        print(str(ts.distance_centimeters))
