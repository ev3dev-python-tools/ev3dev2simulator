"""
Module containing the class InstanceChecker.
"""

import os
import time
import tempfile
import sys
import platform
from pyglet import clock


class InstanceChecker:
    """
    Class used to detect whether another instance is already running.
    """
    def __init__(self, visualiser):
        self.visualiser = visualiser
        self.pid_file = None
        self.pid = None

    def check_for_unique_instance(self):
        """ Detect whether an other instance is already running. If so then trigger the
            activation for the other instance and terminate this instance.
        """

        tmpdir = tempfile.gettempdir()
        self.pid_file = os.path.join(tmpdir, "ev3dev2simulator.pid")

        self.pid = str(os.getpid())
        pid_file = open(self.pid_file, 'w')
        pid_file.write(self.pid)
        pid_file.flush()
        pid_file.close()

        time.sleep(2)

        file = open(self.pid_file, 'r')
        line = file.readline()
        file.close()
        read_pid = line.rstrip()
        if read_pid != self.pid:
            # other process already running
            sys.exit()

    def check_for_activation(self):
        """ checks each interval whether the simulator windows must be activated (bring to front)

            note: activation can happen when one tries to start another instance of the simulator,
                  and that instance detects an instance is already running. It then triggers the
                  activation for the other instance and terminates itself.
        """

        def callback(_):
            file = open(self.pid_file, 'r')
            line = file.readline()
            file.close()
            read_pid = line.rstrip()
            if read_pid != self.pid:

                # other simulator tries to start running
                # write pid to pid_file to notify this simulator is already running
                pid_file = open(self.pid_file, 'w')
                pid_file.write(self.pid)
                pid_file.close()

                if platform.system().lower().startswith('win'):
                    self.visualiser.windows_activate()
                else:
                    self.visualiser.activate()

        clock.schedule_interval(callback, 1)
