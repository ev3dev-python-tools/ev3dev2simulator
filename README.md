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
   
### Prerequisites needed only for Linux

   
For Macos and Windows you don't need any prerequisites,
but for linux you do.

The pyttsx3  python speech library  uses system libraries in its implementation. For Macos/Windows the used system 'speak' libraries are always available, but for linux you must sure these are installed with:

     sudo apt update && sudo apt install espeak ffmpeg libespeak1

For linux there are is no binary distribution available for simpleaudio.
          The Python 3 and ALSA development packages are required for pip to build the extension.
          For Debian variants (including Raspbian), this will usually get the job done:

     sudo apt-get install -y python3-dev libasound2-dev


### Installation

Install with pip:
   
      pip install ev3dev2simulator
     
For Windows and Macos all binary dependencies are provided by wheels on pypi, however for Linux the binary extenssion for simpleaudio is compiled when installing.
     
Then you can just run the simulator by running the executable:
   
      ev3dev2simulator

The simulator works on all python versions 3.8 till python 3.12.

   

## Using the simulator

The user guide of the simulator can be found on the [wiki](https://github.com/ev3dev-python-tools/ev3dev2simulator/wiki).
