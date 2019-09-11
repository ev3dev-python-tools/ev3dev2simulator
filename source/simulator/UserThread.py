import threading

from source.simulator.Main import main


class UserThread(threading.Thread):
    """
    Class representing the thread in which the user code runs.
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        main()
