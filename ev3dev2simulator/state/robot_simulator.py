"""
The robot_simulator module contains the RobotSimulator class which handles how the robot behaves.
"""


import math
import threading
from queue import Queue, Empty
from typing import Any
# noinspection PyProtectedMember
from pymunk import Vec2d

from ev3dev2simulator.state.robot_state import RobotState


class RobotSimulator:
    """
    Class responsible for inner-thread communication. All jobs coming from the robot
    are stored in this class to be retrieved by the simulator for updating/rendering
    of the simulated robot.
    """

    def __init__(self, robot: RobotState):
        self.robot = robot

        self.actuator_queues = {}
        self.queue_info = {}

        for actuator in self.robot.get_actuators():
            # actuator is an instance of Arm, Led, Speaker, Wheel  (childs of RobotPart)
            if actuator.ev3type in ['arm', 'motor', 'speaker']:
                actuator_address = (actuator.brick, actuator.address)
                # note: field actuator.address should really be called actuator.port
                #       because real address of an actuator is brick_id and port
                self.queue_info[actuator_address] = actuator
                self.actuator_queues[actuator_address] = Queue()

        self.should_reset = False

        self.motor_lock = threading.Lock()

    def update(self):
        """
        processes the actuators and sensors of the robot and syncs the sprites to the physics.
        """
        if self.should_reset:
            self.reset()

        else:
            self._process_job_per_actuator()
            self._process_leds()
            self.robot.update_sensors()
            self._sync_physics_sprites()

    def put_actuator_job(self, actuator_address: (int, str), job: float):
        """
        Add a new job for actuator to its own queue.
        For each unique actuator address there is a separate queue.
        :param actuator_address: Address of the actuator (brick_id,device_port)
        :param job: to add.
        """
        # actuator_queues is a dict with key an actuator_address, and as value a Queue
        # put_nowait puts a value in the queue without blocking
        self.actuator_queues[actuator_address].put_nowait(job)

    def next_actuator_jobs(self) -> any:
        """
        Get for all actuators of the robot the next job from each actuator's own Queue.
        Some actuators may have an empty Queue, then the actuator does nothing at the moment.

        For example by using this function we can get the next move jobs for the left and right motor from the queues.
        A move job in this case is just a floating point number representing the job's move distance.

        :return:
           list of job per each actuator of robot as :  List of (actuator_address, job) tuples, where job is None if actuator is inactive.
        """

        self.motor_lock.acquire()

        motor_jobs = []
        for actuator_address, jobs in self.actuator_queues.items():
            try:
                job = jobs.get_nowait()
            except Empty:
                job = None
            motor_jobs.append((actuator_address, job))

        self.motor_lock.release()
        return motor_jobs

    def clear_actuator_jobs(self, actuator_address: (int, str)):
        """
        Clears all current jobs of an actuator at actuator_address on the robot
        """
        self.motor_lock.acquire()
        self.actuator_queues[actuator_address] = Queue()
        self.motor_lock.release()

    def set_led_color(self, brick_id, led_id, color):
        """
        Since responds directly to a command, this function directly sets the led to the state of robot
        """
        self.robot.led_colors[(brick_id, led_id)] = color

    def reset_queues_of_brick(self, brick_id: int):
        """
        Reset queues if bricks disconnect.
        :param brick_id: identifier of brick you want to reset the queues of.
        """
        # actuator_address = (brick_id, device_port)
        for actuator_address in self.actuator_queues:
            if actuator_address[0] == brick_id:
                self.clear_actuator_jobs(actuator_address)

    def reset(self):
        """
        Reset the data of this State
        :return:
        """
        for key in self.actuator_queues:
            self.clear_actuator_jobs(key)

        self.robot.reset()
        self.should_reset = False

    def get_value(self, sensor_address: (int, str)) -> Any:
        return self.robot.get_value(sensor_address)

    def determine_port(self, brick_id: int, kwargs: dict, class_name: str):
        """
        Determines the port of a device based on the kwargs given to the device.
        :param brick_id: identifier of the brick, that the device should be connected to.
        :param kwargs: keyword arguments given by the sensor or actuator to the device.
        :param class_name: some devices do not have a driver_name such as leds, for these, we use class_name
        :return: returns 'dev_not_connected' or the port as string.
        """
        devices = {**self.robot.sensors, **self.robot.actuators}
        if class_name is not None and class_name == 'leds':
            return 'leds_addr'
        if class_name is not None and 'driver_name' not in kwargs and class_name == 'tacho-motor':
            kwargs['driver_name'] = 'lego-ev3-m-motor'
        if kwargs.get('driver_name') is not None:
            driver_names_pre = kwargs.get('driver_name')
            driver_names = driver_names_pre if isinstance(driver_names_pre, list) else [driver_names_pre]

            device_port = kwargs.get('address')
            if device_port is not None:
                device_address = (brick_id, device_port)
                device = devices.get(device_address)
                if device:
                    if device.driver_name in driver_names:
                        return device_port
                    else:
                        print('ERROR: device with classname',class_name,'and driver names', driver_names)
                        print('       NOT FOUND on robot', self.robot.name, 'on brick' , brick_id, 'for device address',device_port)
                        print('       Instead the port', device_port,  'on that brick has a device', "'" + device.driver_name + "'",'\n')
                else:
                    print('ERROR: There is no device connected on port',device_port,'on brick', brick_id, 'of robot', self.robot.name)
            else:
                found_devices = list(filter(lambda dev: dev.driver_name in driver_names, devices.values()))
                if len(found_devices) == 1:
                    return found_devices[0].address

        print(f'Could not find device with classname {class_name} and driver name {kwargs.get("driver_name")} on '
              f'address {kwargs.get("address")} of {self.robot.name}, brick {brick_id}')
        return 'dev_not_connected'

    def _process_job_per_actuator(self):
        """
        Request the movement of the robot motors from the robot state and move the robot accordingly.
        This is where the different motor jobs are combined to a single movement of the robot.
        """
        job_per_actuator = self.next_actuator_jobs()
        left_ppf = right_ppf = None
        for (address, job_of_actuator) in job_per_actuator:
            actuator = self.queue_info[address]
            if actuator.ev3type == 'arm':
                if job_of_actuator is not None:
                    self.robot.execute_arm_movement(address, job_of_actuator)
            elif actuator.ev3type == 'motor':
                if actuator.x_offset < 0:
                    left_ppf = job_of_actuator
                else:
                    right_ppf = job_of_actuator
            elif actuator.ev3type == 'speaker':
                self.robot.sounds[address] = job_of_actuator

        if left_ppf is not None or right_ppf is not None:
            self.robot.execute_movement(left_ppf, right_ppf)

    def _process_leds(self):
        for address, led_color in self.robot.led_colors.items():
            self.robot.set_led_color(address, led_color)



    def _sync_physics_sprites(self):
        self.robot.set_last_pos(self.robot.body.position)
        self.robot.last_angle = math.degrees(self.robot.body.angle)
        for part in self.robot.parts:
            rel = Vec2d(*part.shape.center_of_gravity)
            x, y = rel.rotated(self.robot.body.angle) + self.robot.body.position
            part.sprite.center_x = x
            part.sprite.center_y = y
            part.sprite.angle = math.degrees(part.shape.body.angle)
