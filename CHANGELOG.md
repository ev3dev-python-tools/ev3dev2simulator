# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

##  [2.0.5] - 2020-12-10

### Added
- Added configuration of the depth of lake objects. The ultrasonic sensor pointed to the bottom measures the depth to the underlying object. Previously, everything was assumed to be very shallow and specific obstacles had the maximum depth. Now, the depth of the lakes can be configured (default 800mm).  The board, the playing field of the robots, is not configurable and gets the default value of 20mm depth. When no lake  nor a playfield is sensed the sensor gets the maximal value of 2550.  Finally, the border of the lake is assumed at board depth, and therefore gets the same depth as the board.

## [2.0.4] - 2020-11-25

### Added
- Bluetooth example 

### Changed 
- default config files

## [2.0.3] - 2020-11-11

### Fixed
- Fix for threading issue #39

## [2.0.2] - 2020-10-29

### Fixed
- Fixed issue with turning leds off.

## [2.0.1] - 2020-10-13

### Fixed
- Fixed bug which happened when selecting or moving invalid objects 

## [2.0.0] - 2020-10-06

### Added 
- Added physics to simulate collision between all objects, including robots
- Added support for simulating multiple robots
- Added support for playings sounds from the simulator
- Added configuration of the robot(s) and the simulated environment before simulation by means of a configuration file
- Added support for drag-and-dropping robots and obstacles during simulation
- Added support for scaling the playing field
- Added checks on ports used by the robot on startup
- Added two types of rocks (light and heavy)
- Added sidebar with robot information

### Changed
- Changed architecture to support millimeters instead of pixels
- Changed the architecture to allow multiple robots in a single simulation environment.
- Changed behaviour of distance sensor (it now picks the shortest distance of the two beams)
- Removed the dependency of the behaviour of the robot on the usage of sprites. It now uses physics. 

### Fixed
- Fixed bug with drawing circles that prevented updating Arcade


## [1.3.2] - 2020-02-28

### Added 
  - added simulated bluetooth.py to ev3dev2simulator package. 
  - Warning: to use the simulated bluetooth in the simulator make sure you have PyBluez uninstalled!!
  
### Fixed
  - fullscreen switch when dragged: drag window to screen where you want it fullscreen, and then press F
  - key T toggles fullscreen view between the two screens (if not at fullscreen, nothing happens)


## 1.3.1 - 2020-02-07

 ### Added
 - added building of wheels and uploading them to the pypi server

 ### Removed
 - don't build and upload sdist package anymore, because a wheel is also a source package
   and is better because it contains the requirements in metadata of the package,
   which one can fetch from the pypi server before downloading a package. 
   
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


[unreleased]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v2.0.5...HEAD
[2.0.5]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v2.0.4...v2.0.5
[2.0.4]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v2.0.3...v2.0.4
[2.0.3]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v2.0.2...v2.0.3
[2.0.2]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.3.2...v2.0.0
[1.3.2]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.3.0...v1.3.2
[1.3.0]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/ev3dev-python-tools/ev3dev2simulator//compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ev3dev-python-tools/ev3dev2simulator/releases/tag/1.0


