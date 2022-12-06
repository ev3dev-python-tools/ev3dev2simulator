# ev3dev2simulator: simulator for the EV3 (ev3dev2 API)

The behaviour of the EV3 robot is simulated in the simulator. This is convenient to quickly test programs when you momentarily don’t have access to an EV3.

![ev3dev2simulator](https://raw.githubusercontent.com/wiki/ev3dev-python-tools/ev3dev2simulator/img/small.PNG "ev3dev2simulator")

You can use the 'ev3dev2' python library to program the EV3. The simulator installs a fake 'ev3dev2' library on the PC. When using this library on the PC, every call to this API is forwarded to the simulator which uses it to simulate the behaviour of the EV3 robot. 

For an example see: https://github.com/ev3dev-python-tools/thonny-ev3dev/wiki/Simulator-example<br>
The running program can be seen in the following video: http://www.cs.ru.nl/lab/ev3dev2simulator.html .

The thonny-ev3dev plugin makes it easier to program the EV3 programmable LEGO brick 
using the [Thonny Python IDE for beginners](http://thonny.org/). 
The thonny-ev3dev plugin for the Thonny IDE comes with the ev3dev2simulator.

For more info about the thonny-ev3dev plugin see: https://github.com/ev3dev-python-tools/thonny-ev3dev/wiki <br>
For more info about Thonny: http://thonny.org

## Getting started
   
   The only prerequisites for the simulator are python 3.8.10 and pip. Simulating robot sound works out of the box for Windows and macOS users. Linux user need to install [espeak](http://espeak.sourceforge.net/).
   
   First, for windows users it is strongly adviced to install **python 3.8.10**. For this python version the installation goes smoothly because there are precompiled binary wheels available for all dependencies. Newer versions of python will also work, but then you need a c build environment installed to build the c-code of the simpleaudio package. For macos and linux a c build environment is standard available and install with compiling c-code will not be a problem.  

   Install python3
      
      Download Python 3.8.10 from the Python website (https://www.python.org/downloads/). 
      Note: 3.8.10 is the latest 3.8 version with installers.
      
   Install with pip
   
      pip install ev3dev2simulator
     
   Then you can just run the simulator by running the executable:
   
      ev3dev2simulator

## Using the simulator

The user guide of the simulator can be found on the [wiki](https://github.com/ev3dev-python-tools/ev3dev2simulator/wiki).
