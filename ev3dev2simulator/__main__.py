"""
Main file of the ev3dev2simulator. Used when the ev3dev2simulator module is run.
The main goal of the main function is to change the working directory to the simulator source code directory.
This helps with loading all the assets used in visualisation.
"""

import sys
import os


def main():
    """The main routine."""
    orig_path = os.getcwd()
    # pylint: disable=import-outside-toplevel
    try:
        from ev3dev2simulator.simulator import simmain
    except ImportError:
        # below HACK not needed if ev3dev2simulator installed on PYTHONPATH
        # note: run as 'python3 <path-to-package-dir>'
        # HACK: need to change dir to Simulator script's directory because resources are loaded relative from this
        # directory
        script_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_dir)
        # add directory containing the ev3dev2simulator package to the python path
        ev3dev2simulator_dir = os.path.dirname(script_dir)
        sys.path.insert(0, ev3dev2simulator_dir)
        # import main from ev3dev2simulator package
        from ev3dev2simulator.simulator import main as simmain
    # pylint: enable=import-outside-toplevel
    sys.exit(simmain(orig_path))


# run ev3dev2simulator package as script to run simulator
#  usage: python3 -m ev3dev2simulator
if __name__ == "__main__":
    # start main by default
    main()
