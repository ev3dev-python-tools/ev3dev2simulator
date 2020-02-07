# ev3dev2simulator: simulator for the EV3 (ev3dev2 API)

The behaviour of the EV3 robot is simulated in the simulator. This is convenient to quickly test programs when you momentarily don’t have access to an EV3.

![ev3dev2simulator](https://raw.githubusercontent.com/wiki/ev3dev-python-tools/thonny-ev3dev/images/ev3dev2simulator.png "ev3dev2simulator")

You can use the 'ev3dev2' python library to program the EV3. The simulator installs a fake 'ev3dev2' library on the PC. When using this library on the PC, every call to this API is forwarded to the simulator which uses it to simulate the behaviour of the EV3 robot. 

For an example see: https://github.com/ev3dev-python-tools/thonny-ev3dev/wiki/Simulator-example<br>
The running program can be seen in the following video: http://www.cs.ru.nl/lab/ev3dev2simulator.html .

The thonny-ev3dev plugin makes it easier to program the EV3 programmable LEGO brick 
using the [Thonny Python IDE for beginners](http://thonny.org/). 
The thonny-ev3dev plugin for the Thonny IDE comes with the ev3dev2simulator.

For more info about the thonny-ev3dev plugin see: https://github.com/ev3dev-python-tools/thonny-ev3dev/wiki <br>
For more info about Thonny: http://thonny.org

## Single instance

The ev3dev2simulator enforces that only one instance of the simulator can be run.

When a simulator is running, and you  then startup a new simulator window:
 * the new simulator sees that another simulator is already running and exits
 * the already simulator's window is raised so that it becomes visible again.

## Key bindings

When you press the key:
* q : Quit the simulator
* m : Maximize simulator window
* f : Show simulator fullscreen (toggle)
* t : Toggle screen on which to show simulator in fullscreen mode. 


## Installation

   Install with pip
   
      pip install ev3dev2simulator
     
   Then you can just run the simulator by running the executable:
   
      ev3dev2simulator

## Command line options 


    
    $ ev3dev2simulator -h
    usage: ev3dev2simulator [-h] [-s WINDOW_SCALING] [-t {small,large}]
                            [-x ROBOT_POSITION_X] [-y ROBOT_POSITION_Y]
                            [-o ROBOT_ORIENTATION] [-c {left,right}] [-2] [-f]
                            [-m]
    .
    optional arguments:
      -h, --help            show this help message and exit
      -s WINDOW_SCALING, --window_scaling WINDOW_SCALING
                            Scaling of the screen, default is 0.65
      -t {small,large}, --simulation_type {small,large}
                            Type of the simulation (small or large). Default is
                            small
      -x ROBOT_POSITION_X, --robot_position_x ROBOT_POSITION_X
                            Starting position x-coordinate of the robot, default
                            is 200
      -y ROBOT_POSITION_Y, --robot_position_y ROBOT_POSITION_Y
                            Starting position y-coordinate of the robot, default
                            is 300
      -o ROBOT_ORIENTATION, --robot_orientation ROBOT_ORIENTATION
                            Starting orientation the robot, default is 0
      -c {left,right}, --connection_order_first {left,right}
                            Side of the first brick to connect to the simulator,
                            default is 'left'
      -2, --show-on-second-monitor
                            Show simulator window on second monitor instead,
                            default is first monitor
      -f, --fullscreen      Show simulator fullscreen
      -m, --maximized       Show simulator maximized


## Features not yet supported

The simulator does not yet support the full ev3dev2 API. When looking at the ev3dev2  API's source files,  the below listed functions, classes, or specific class methods  are not yet supported. 

We list what is NO supported, so the rest is supported. Meaning:
* if only a specific python file is listed, then that whole file is not supported. Python files not listed ARE fully supported.
* if within a python file a specific class/function is listed, then that class/function is not supported but all other class/functions in that file ARE supported.
* if specific for a class a set of methods are listed, those methods are not supported, but the class itself and the other methods in the class ARE supported.

The current not supported listing is:

button.py <br />
 console.py <br />
<br />
 control/init.py<br />
 control/GyroBalance.py <br />
 control/rc\_tank.py<br />
 control//webserver.py <br />
<br />
 display.py <br />
 led.py <br />
<br />
 motor.py
* class ActuonixL1250Motor
* class ActuonixL12100Motor
* class DcMotor
* class ServoMotor
* class MoveJoystick
* class LineFollowErrorLostLine
* class LineFollowErrorTooFast
* class MoveJoystick
* class MoveTank
  * def follow\_line()  port.py <br />
 power.py <br />
<br />
 sensor/init.py
* def list\_sensors
* class Sensor
  * def bin\_data()
* class I2cSensor  sensor/lego.py
* class ColorSensor
  * def reflected\_light\_intensity()
  * def ambient\_light\_intensity()
  * def raw()
  * def calibrate\_white()
  * def rgb()
  * def fab()
  * def hsv()
  * def hls()
  * def red()
  * def green()
  * def blue()
* class UltrasonicSensor
  * def other\_sensor\_present()
* class GyroSensor
* class InfraredSensor
* class SoundSensor
* class LightSensor <br />
  * def get\_command\_processes()
  * Class Sound
    * def beep()
    * def tone()
    * def play\_tone()
    * def play\_note()
    * def play()
    * def play\_file()
    * def get\_volume()
    * def set\_volume()
    * def play\_song()
    * def beep\_args()
    * def get\_channel()
