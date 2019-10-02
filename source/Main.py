from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2, INPUT_3
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound


# !/usr/bin/env python3

class Runner:

    def __init__(self):
        self.s = Sound()
        self.cs = ColorSensor(INPUT_2)
        self.ts1 = TouchSensor(INPUT_1)
        self.ts4 = TouchSensor(INPUT_4)

        self.us = UltrasonicSensor(INPUT_3)
        self.us.mode = 'US-DIST-CM'

        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

        self.drive()
        self.check()


    def reverseRotations(self, rotations):
        self.tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), rotations, brake=False)


    def rotateDegrees(self, degrees):
        degrees = degrees * 2
        self.tank_drive.on_for_degrees(SpeedPercent(40), SpeedPercent(0), degrees, brake=False)


    def drive(self):
        self.tank_drive.on(SpeedPercent(30), SpeedPercent(30))


    def checkCollision(self):
        if self.ts1.is_pressed or self.ts4.is_pressed:
            self.tank_drive.stop()

            # self.s.speak("blyat.wav")
            self.reverseRotations(1)
            self.rotateDegrees(180)

            self.drive()


    def checkColor(self):
        if self.cs.color == 6:
            self.tank_drive.stop()

            # self.s.speak("blyat.wav")
            self.reverseRotations(1)
            self.rotateDegrees(150)

            self.drive()


    def checkDistance(self):
        if -1 > self.us.value() < 180:
            self.tank_drive.stop()

            # self.s.speak("wow")
            self.reverseRotations(1)
            self.rotateDegrees(125)

            self.drive()


    def check(self):
        while True:
            self.checkCollision()
            self.checkColor()
            self.checkDistance()


def main():
    Runner()
