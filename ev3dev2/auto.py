from ev3dev2 import *

# simulator simulates 'ev3'
platform = 'ev3'
if platform == 'ev3':
    from ev3dev2._platform.ev3 import INPUT_1, INPUT_2, INPUT_3, INPUT_4
    from ev3dev2._platform.ev3 import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
    from ev3dev2._platform.ev3 import LEDS, LED_GROUPS, LED_COLORS


from ev3dev2.button import *
from ev3dev2.console import *
from ev3dev2.display import *
from ev3dev2.fonts import *
from ev3dev2.led import *
from ev3dev2.motor import *
from ev3dev2.port import *
from ev3dev2.power import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import *
