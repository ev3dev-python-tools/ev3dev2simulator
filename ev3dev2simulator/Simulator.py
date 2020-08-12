import argparse
import sys
import os

if __name__ == '__main__':
    orig_path = os.getcwd()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

from ev3dev2simulator.config.config import load_config, get_world_config
from ev3dev2simulator.state import WorldState
from ev3dev2simulator.visualisation.Visualiser import Visualiser, start
from ev3dev2simulator.connection.ServerSockets import ServerSockets
from ev3dev2simulator.state.WorldSimulator import WorldSimulator
from ev3dev2simulator.state.WorldState import WorldState


def parse_args(args):
    """
    Parses the arguments given to the program. Mainly arguments for the visualisation.
    :param args: list of parameters given to program
    :return: list of parsed values based on parameters
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version",
                        action='store_true',
                        help="Show version info")
    parser.add_argument("-t", "--simulation_file",
                        default='config_small',
                        help="Path to the configuration file. Defaults to config_small",
                        required=False,
                        type=str)
    parser.add_argument("-2", "--show-on-second-monitor",
                        action='store_true',
                        help="Show simulator window on second monitor instead, default is first monitor")
    parser.add_argument("-f", "--fullscreen",
                        action='store_true',
                        help="Show simulator fullscreen")
    parser.add_argument("-m", "--maximized",
                        action='store_true',
                        help="Show simulator maximized")
    return parser.parse_args(args)


def main(orig_path):
    """
    Spawns the user thread and creates and starts the simulation.
    """
    args = vars(parse_args(sys.argv[1:]))

    if args['version']:
        from ev3dev2 import version as api_version
        from ev3dev2simulator import version as sim_version
        print("version ev3dev2           : " + api_version.__version__)
        print("version ev3dev2simulator  : " + sim_version.__version__)
        sys.exit(0)

    use_second_screen_to_show_simulator = args['show_on_second_monitor']
    show_fullscreen = args['fullscreen']
    show_maximized = args['maximized']

    load_config(args['simulation_file'], orig_path)

    world_state = WorldState(get_world_config())

    world_simulator = WorldSimulator(world_state)

    Visualiser(world_simulator.update, world_state, show_fullscreen, show_maximized,
               use_second_screen_to_show_simulator)

    server_thread = ServerSockets(world_simulator)
    server_thread.setDaemon(True)
    server_thread.start()

    start()


if __name__ == '__main__':
    main(orig_path)
