import argparse
import sys

from ev3dev2simulator.Visualiser import Visualiser
from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.connection.ServerSockets import ServerSockets
from ev3dev2simulator.state.WorldSimulator import WorldSimulator
from ev3dev2simulator.state.WorldState import WorldState
from ev3dev2simulator.util.Util import apply_scaling

from ev3dev2simulator.connection.ServerSocketDouble import ServerSocketDouble
from ev3dev2simulator.connection.BrickServerSocket import ServerSocketSingle


def create_arg_parser():
    def validate_scale(value):
        """
        Check if the given value is a valid scale value. Throw an Error if this is not the case.
        :param value: to validate.
        :return: a boolean value representing if the validation was successful.
        """

        try:
            f = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError('Scaling value must be a floating point number')

        if f < 0.0 or f > 1.0:
            raise argparse.ArgumentTypeError("%s is an invalid scaling value. Should be between 0 and 1" % f)

        return f

    def validate_xy(value):
        """
        Check if the given value is a valid xy value. Throw an Error if this is not the case.
        :param value: to validate.
        :return: a boolean value representing if the validation was successful.
        """

        try:
            f = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError('Coordinate value must be a integer')

        if f < 0 or f > 1000:
            raise argparse.ArgumentTypeError("%s is an invalid coordinate. Should be between 0 and 1000" % f)

        return f

    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version",
                        action='store_true',
                        help="Show version info")
    parser.add_argument("-s", "--window_scaling",
                        default=0.65,
                        help="Scaling of the screen, default is 0.65",
                        required=False,
                        type=validate_scale)
    parser.add_argument("-t", "--simulation_file",
                        default='config_small',
                        help="Path to the configuration file. Defaults to config_small",
                        required=False,
                        type=str)
    # parser.add_argument("-x", "--robot_position_x",
    #                     default=200,
    #                     help="Starting position x-coordinate of the robot, default is 200",
    #                     required=False,
    #                     type=validate_xy)
    # parser.add_argument("-y", "--robot_position_y",
    #                     default=300,
    #                     help="Starting position y-coordinate of the robot, default is 300",
    #                     required=False,
    #                     type=validate_xy)
    # parser.add_argument("-o", "--robot_orientation",
    #                     default=0,
    #                     help="Starting orientation the robot, default is 0",
    #                     required=False,
    #                     type=int)
    # parser.add_argument("-c", "--connection_order_first",
    #                     choices=['left', 'right'],
    #                     default='left',
    #                     help="Side of the first brick to connect to the simulator, default is 'left'",
    #                     required=False,
    #                     type=str)

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

    config = get_config()

    s = args['window_scaling']
    config.write_scale(s)

    # config.write_sim_type(t)

    use_second_screen_to_show_simulator = args['show_on_second_monitor']
    show_fullscreen = args['fullscreen']
    show_maximized = args['maximized']

    simulation_config = config.get_simulation_config(args['simulation_file'])
    world_state = WorldState(simulation_config)

    world_simulator = WorldSimulator(world_state)

    # visualiser = Visualiser(world_simulator.update, world_state, show_fullscreen, show_maximized,
    #                         use_second_screen_to_show_simulator)

    # server_thread = ServerSockets(world_simulator)
    # server_thread.setDaemon(True)
    # server_thread.start()

    # visualiser.start()


main()
