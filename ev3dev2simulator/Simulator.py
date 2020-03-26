import argparse
import sys
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.state import WorldState
from ev3dev2simulator.visualisation.Visualiser import Visualiser, start
from ev3dev2simulator.connection.ServerSockets import ServerSockets
from ev3dev2simulator.state.WorldSimulator import WorldSimulator
from ev3dev2simulator.state.WorldState import WorldState


def create_arg_parser():
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
    return parser


def main():
    """
    Spawns the user thread and creates and starts the simulation.
    """
    arg_parser = create_arg_parser()
    args = vars(arg_parser.parse_args())

    if args['version']:
        from ev3dev2 import version as apiversion
        from ev3dev2simulator import version as simversion
        print("version ev3dev2           : " + apiversion.__version__)
        print("version ev3dev2simulator  : " + simversion.__version__)
        sys.exit(0)

    use_second_screen_to_show_simulator = args['show_on_second_monitor']
    show_fullscreen = args['fullscreen']
    show_maximized = args['maximized']

    simulation_config = get_config().get_simulation_config(args['simulation_file'])
    world_state = WorldState(simulation_config)

    world_simulator = WorldSimulator(world_state)

    Visualiser(world_simulator.update, world_state, show_fullscreen, show_maximized,
               use_second_screen_to_show_simulator)

    server_thread = ServerSockets(world_simulator.robotSimulators)
    server_thread.setDaemon(True)
    server_thread.start()

    start()


main()
