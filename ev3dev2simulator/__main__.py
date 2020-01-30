import sys
import os
import signal
import tempfile

def main(args=None):
    """The main routine."""

    try:
        from ev3dev2simulator.Simulator import simmain
    except ImportError:
        ## below HACK not needed if ev3dev2simulator installed on PYTHONPATH
        ## note: run as 'python3 <path-to-package-dir>'
        import os
        # HACK: need to change dir to Simulator script's directory because resources are loaded relative from this directory
        script_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_dir)
        # add directory containing the ev3devsimulator package to the python path
        ev3devsimulator_dir = os.path.dirname(script_dir)
        sys.path.insert(0,ev3devsimulator_dir)
        # import main from ev3devsimulator package
        from ev3dev2simulator.Simulator import main as simmain

    sys.exit(simmain())


# run ev3dev2simulator package as script to run simulator
#  usage: python3 -m ev3dev2simulator
if __name__ == "__main__":
    # start main by default
    main()
