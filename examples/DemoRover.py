#!/usr/bin/env python3

from ev3devlogging import timedlog as log

from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2, INPUT_3
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound

class Rover:

    def __init__(self):
        self.s = Sound()
        self.cs = ColorSensor(INPUT_2)
        self.ts1 = TouchSensor(INPUT_1)
        self.ts4 = TouchSensor(INPUT_4)

        # self.us = UltrasonicSensor(INPUT_3)
        # self.us.mode = 'US-DIST-CM'

        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

    def reverseRotations(self, rotations):
        self.tank_drive.on_for_rotations(SpeedPercent(-35), SpeedPercent(-35), rotations, brake=False)

    def rotateDegrees(self, degrees):
        degrees = degrees * 2
        self.tank_drive.on_for_degrees(SpeedPercent(40), SpeedPercent(0), degrees, brake=False)

    def checkCollision(self):
        return self.ts1.is_pressed or self.ts4.is_pressed

    def run(self):
        self.tank_drive.on(SpeedPercent(30), SpeedPercent(30))
        while True:
            colorNr = self.cs.color
            if colorNr == 1: # black line
                log("border")
                self.tank_drive.stop()
                self.reverseRotations(1)
                self.rotateDegrees(150)
                self.tank_drive.on(SpeedPercent(30), SpeedPercent(30))
            elif (colorNr == 2 or colorNr == 4 or colorNr == 5) : # blue or yellow or red
                print("lake with color={color}".format(color=colorNr))
                log("lake")
                self.tank_drive.stop()
                self.rotateDegrees(90)
                self.tank_drive.on(SpeedPercent(30), SpeedPercent(30))
            elif  self.checkCollision():
                log("collision")
                self.tank_drive.stop()

                # self.s.speak("blyat.wav")
                self.reverseRotations(1)
                self.rotateDegrees(180)
                self.tank_drive.on(SpeedPercent(30), SpeedPercent(30))

Rover().run()
