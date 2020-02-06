# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [1.3.0] - 2020-02-06

### Added 
- added functionality that ensures only one simulator is open: the new one terminates terminates itself if another is already open. The already open windows is brought to foreground.
- added icon for simulator window
- support for resizing the window
- support for maximizing the window when pressing 'm' key and fullscreen when pressing 'f'
- commandline options to start simulator maximized or fullscreen
- commandline option to start the simulator on the second screen instead of the primary screen
- added entry script so that simulator can be started from command line
- added auto import ability to the simulated 'ev3dev2' library so that we can easily import everything 
  with the import line: `from ev3dev2 import auto as ev3`. 
- added shortcut keys 'q','m','f','t' for quit, maximize, fullscreen, toggle screem for fullscreen 
- added version option, and version info on title bar of simulator

### Changed 
- moved project from Sam Jansen's github account at https://github.com/Samskip16/ev3dev2-Simulator 
  to new project website https://github.com/ev3dev-python-tools/ev3dev2simulator
- reorganized code so that it can be installed as a package on pypi  
- improved exit   


## [1.2.1] - 2019-12-17

### Added
- Added bottle obstacle for the small simulation type.
- Added sendall() function to BluetoothSocket.

### Fixed
- Fixed BluetoothSocket makefile() error.
- Fixed issue where a ZeroDivisionError would occur when trying to rotate a motor a very short distance.

### Changed 
- Merged the small- and large simulation types into one program.


## [1.2.0] - 2019-11-26

### Added
- Added fall detection for when the robot drives off the map or into a lake.
- Added Mars Rover body, sensors and playing field.
- Added support for led.py.
- Color sensors now flash the color they are sensing.
- Motor classes now correctly contain their current drive state.
- Simulator can now accept two connections. Used to support the Mars Rover.
- Simulator can now mock a bluetooth connection. Used to support the Mars Rover.
- Ultrasonic sensor now does a raycast per eye, instead of one from the center of the unit, to improve simulation accuracy.


## [1.1.1] - 2019-10-16

### Fixed
- Fixed an issue where multiple consecutive calls to a motor would not be overridden immediately when using block=False

### Added
- Added missing unsupported lego.py sensors


## [1.1.0] - 2019-10-15

### Added
- Added all unsupported code of the ev3dev2 library to prevent ModuleNotFound errors.
- Added support for the run_direct() function of the motor.
- Lakes are now filled.
- Requesting data from a sensor can now happen more often (8ms) instead of every frame (30ms).
- Simulator can now be started from the command line.

### Fixed
- Solved an issue where the robot would stutter when calling run_forever() or any function which calls run_forever() internally.

### Changed 
- Updated the ev3dev2 library from version 2.0.0beta1 to 2.0.0beta5.

## [1.0.0] - 2019-10-15

### Added
- First version ready for use


[unreleased]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.3.0...HEAD
[1.3.0]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/olivierlacan/keep-a-changelog/releases/tag/v1.0.0


