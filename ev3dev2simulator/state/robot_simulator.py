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
            if actuator.ev3type in ['arm', 'motor', 'speaker']:
                self.queue_info[(actuator.brick, actuator.address)] = actuator
                self.actuator_queues[(actuator.brick, actuator.address)] = Queue()

        self.should_reset = False
        self.locks = {}

        self.motor_lock = threading.Lock()

        for sensor in self.robot.get_sensors():
            self.load_sensor(sensor)

    def update(self):
        """
        processes the actuators and sensors of the robot and syncs the sprites to the physics.
        """
        if self.should_reset:
            self.reset()

        else:
            self._process_actuators()
            self._process_leds()
            self._process_sensors()
            self._sync_physics_sprites()

        self.release_locks()

    def put_actuator_job(self, address: (int, str), job: float):
        """
        Add a new move job to the queue for the center motor.
        :param address: Address of the actuator
        :param job: to add.
        """
        self.actuator_queues[address].put_nowait(job)

    def next_actuator_jobs(self) -> any:
        """
        Get the next move jobs for the left and right motor from the queues.
        :return: a floating point numbers representing the job move distances.
        """

        self.motor_lock.acquire()

        motor_jobs = []
        for actuator, jobs in self.actuator_queues.items():
            try:
                job = jobs.get_nowait()
            except Empty:
                job = None
            motor_jobs.append((actuator, job))

        self.motor_lock.release()
        return motor_jobs

    def clear_actuator_jobs(self, address: (int, str)):
        """
        Clears all current jobs of the robot
        """
        self.motor_lock.acquire()
        self.actuator_queues[address] = Queue()
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
        for key in self.actuator_queues:
            if key[0] == brick_id:
                self.clear_actuator_jobs(key)

    def reset(self):
        """
        Reset the data of this State
        :return:
        """
        for key in self.actuator_queues:
            self.clear_actuator_jobs(key)

        self.robot.reset()
        self.should_reset = False

    def load_sensor(self, sensor):
        """
        Load the given sensor adding its default value to this state.
        Also create a lock for the given sensor.
        :param sensor: to load.
        """
        address = (sensor.brick, sensor.address)
        self.robot.values[address] = sensor.get_default_value()
        self.locks[address] = threading.Lock()

    def release_locks(self):
        """
        Release all the locked sensor locks. This re-allows for reading
        the sensor values.
        """
        for lock in self.locks.values():
            if lock.locked():
                lock.release()

    def get_value(self, address: (int, str)) -> Any:
        """
        Get the value of a sensor by its address. Blocks if the lock of
        the requested sensor is not available.
        :param address: of the sensor to get the value from.
        :return: the value of the sensor.
        """
        self.locks[address].acquire()
        return self.robot.values[address]

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

            if kwargs.get('address') is not None:
                device = devices.get((brick_id, kwargs.get('address')))
                if device:
                    if devices.get((brick_id, kwargs.get('address'))).driver_name in driver_names:
                        return kwargs.get('address')
                else:
                    print('device not found on brick', brick_id, ' with address', kwargs.get('address'))
            else:
                found_devices = list(filter(lambda dev: dev.driver_name in driver_names, devices.values()))
                if len(found_devices) == 1:
                    return found_devices[0].address

        print(f'Could not find device with classname {class_name} and driver name {kwargs.get("driver_name")} on '
              f'address {kwargs.get("address")} of {self.robot.name}, brick {brick_id}')
        return 'dev_not_connected'

    def _process_actuators(self):
        """
        Request the movement of the robot motors form the robot state and move
        the robot accordingly. This is where the different motor jobs are combined to a single movement of the robot.
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

    def _process_sensors(self):
        """
        Process the data of the robot sensors by retrieving the data and putting it
        in the robot state.
        """
        for address, sensor in self.robot.sensors.items():
            self.robot.values[address] = sensor.get_latest_value()

    def _sync_physics_sprites(self):
        self.robot.set_last_pos(self.robot.body.position)
        self.robot.last_angle = math.degrees(self.robot.body.angle)
        for part in self.robot.parts:
            rel = Vec2d(part.shape.center_of_gravity)
            x, y = rel.rotated(self.robot.body.angle) + self.robot.body.position
            part.sprite.center_x = x
            part.sprite.center_y = y
            part.sprite.angle = math.degrees(part.shape.body.angle)
