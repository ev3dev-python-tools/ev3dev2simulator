from  ev3dev2.version import __version__ as apiversion
from  ev3dev2simulator.version import __version__ as simversion

print("version            ev3dev2 : " + apiversion)
print("version   ev3dev2simulator : " + simversion)

# note: single line :  python3 -c"import ev3dev2simulator.version; print(ev3dev2simulator.version.__version__)"
