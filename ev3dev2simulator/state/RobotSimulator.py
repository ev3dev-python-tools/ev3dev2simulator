import threading
from queue import Queue, Empty
from typing import Any, Tuple

from ev3dev2simulator.config.config import get_config
from ev3dev2simulator.state.RobotState import RobotState


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
            if actuator.ev3type in ['arm', 'motor']:
                self.queue_info[(actuator.brick, actuator.address)] = actuator
                self.actuator_queues[(actuator.brick, actuator.address)] = Queue()

        self.sound_queue = Queue()

        self.should_reset = False

        self.values = {}
        self.locks = {}

        self.motor_lock = threading.Lock()

    def update(self):
        if self.should_reset:
            # self.setup()
            self.reset()

        else:
            self._process_actuators()
            self._process_leds()
            self._process_sensors()
            self._check_fall()

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
        self.motor_lock.acquire()
        self.actuator_queues[address] = Queue()
        self.motor_lock.release()

    def put_sound_job(self, job: str):
        """
        Add a new sound job to the queue to be displayed.
        :param job: to add.
        """

        self.sound_queue.put_nowait(job)

    def next_sound_job(self) -> str:
        """
        Get the next sound job from the queue.
        :return: a str representing the sound as text to be displayed.
        """

        try:
            return self.sound_queue.get_nowait()
        except Empty:
            return None

    def set_led_color(self, brick_id, led_id, color):
        self.robot.led_colors[(brick_id, led_id)] = color

    def reset(self):
        """
        Reset the data of this State
        :return:
        """
        for key, actuator_queue in self.actuator_queues.items():
            self.clear_actuator_jobs(key)

        self.robot.values.clear()
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
        return self.values[address]

    def _process_actuators(self):
        """
        Request the movement of the robot motors form the robot state and move
        the robot accordingly. This is where the different motor jobs are combined to a single movement of the robot.
        """
        job_per_actuator = self.next_actuator_jobs()

        # TODO figure a neat way to determine the location of wheels
        for (address, job_of_motor) in job_per_actuator:
            actuator = self.queue_info[address]
            if actuator.ev3type == 'arm':
                self.robot.execute_arm_movement(address, job_of_motor)
            elif actuator.ev3type == 'motor':
                if actuator.x_offset < 0:
                    left_ppf = job_of_motor
                else:
                    right_ppf = job_of_motor

        if left_ppf or right_ppf:
            self.robot.execute_movement(left_ppf, right_ppf)

    def _process_leds(self):
        for address, led_color in self.robot.led_colors.items():
            self.robot.set_led_color(address, led_color)

    def _check_fall(self):
        """
        Check if the robot has fallen of the playing field or is stuck in the
        middle of a lake. If so display a message on the screen.
        """

        wheels = self.robot.get_wheels()
        for wheel in wheels:
            if wheel.is_falling():
                self.msg_counter = self.frames_per_second * 3

    def _process_sensors(self):
        """
        Process the data of the robot sensors by retrieving the data and putting it
        in the robot state.
        """
        for address, sensor in self.robot.sensors.items():
            self.robot.values[address] = sensor.get_latest_value()

