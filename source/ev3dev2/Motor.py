# -----------------------------------------------------------------------------
# Copyright (c) 2015 Ralph Hempel <rhempel@hempeldesigngroup.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------
import sys
from collections import OrderedDict

from ev3dev2.MockMotor import MockMotor

if sys.version_info < (3, 4):
    raise SystemError('Must be using Python 3.4 or higher')

from logging import getLogger

log = getLogger(__name__)

# The number of milliseconds we wait for the state of a motor to
# update to 'running' in the "on_for_XYZ" methods of the Motor class
WAIT_RUNNING_TIMEOUT = 100


class SpeedValue(object):
    """
    A base class for other unit types. Don't use this directly; instead, see
    :class:`SpeedPercent`, :class:`SpeedRPS`, :class:`SpeedRPM`,
    :class:`SpeedDPS`, and :class:`SpeedDPM`.
    """


    def __eq__(self, other):
        return self.to_native_units() == other.to_native_units()


    def __ne__(self, other):
        return not self.__eq__(other)


    def __lt__(self, other):
        return self.to_native_units() < other.to_native_units()


    def __le__(self, other):
        return self.to_native_units() <= other.to_native_units()


    def __gt__(self, other):
        return self.to_native_units() > other.to_native_units()


    def __ge__(self, other):
        return self.to_native_units() >= other.to_native_units()


    def __rmul__(self, other):
        return self.__mul__(other)


class SpeedPercent(SpeedValue):
    """
    Speed as a percentage of the motor's maximum rated speed.
    """


    def __init__(self, percent):
        assert -100 <= percent <= 100, \
            "{} is an invalid percentage, must be between -100 and 100 (inclusive)".format(percent)

        self.percent = percent


    def __str__(self):
        return str(self.percent) + "%"


    def __mul__(self, other):
        assert isinstance(other, (float, int)), "{} can only be multiplied by an int or float".format(self)
        return SpeedPercent(self.percent * other)


    def to_native_units(self, motor):
        """
        Return this SpeedPercent in native motor units
        """
        return self.percent / 100 * motor.max_speed


class SpeedNativeUnits(SpeedValue):
    """
    Speed in tacho counts per second.
    """


    def __init__(self, native_counts):
        self.native_counts = native_counts


    def __str__(self):
        return "{:.2f}".format(self.native_counts) + " counts/sec"


    def __mul__(self, other):
        assert isinstance(other, (float, int)), "{} can only be multiplied by an int or float".format(self)
        return SpeedNativeUnits(self.native_counts * other)


    def to_native_units(self, motor=None):
        """
        Return this SpeedNativeUnits as a number
        """
        return self.native_counts


class SpeedRPS(SpeedValue):
    """
    Speed in rotations-per-second.
    """


    def __init__(self, rotations_per_second):
        self.rotations_per_second = rotations_per_second


    def __str__(self):
        return str(self.rotations_per_second) + " rot/sec"


    def __mul__(self, other):
        assert isinstance(other, (float, int)), "{} can only be multiplied by an int or float".format(self)
        return SpeedRPS(self.rotations_per_second * other)


    def to_native_units(self, motor):
        """
        Return the native speed measurement required to achieve desired rotations-per-second
        """
        assert abs(self.rotations_per_second) <= motor.max_rps, \
            "invalid rotations-per-second: {} max RPS is {}, {} was requested".format(
                motor, motor.max_rps, self.rotations_per_second)
        return self.rotations_per_second / motor.max_rps * motor.max_speed


class SpeedRPM(SpeedValue):
    """
    Speed in rotations-per-minute.
    """


    def __init__(self, rotations_per_minute):
        self.rotations_per_minute = rotations_per_minute


    def __str__(self):
        return str(self.rotations_per_minute) + " rot/min"


    def __mul__(self, other):
        assert isinstance(other, (float, int)), "{} can only be multiplied by an int or float".format(self)
        return SpeedRPM(self.rotations_per_minute * other)


    def to_native_units(self, motor):
        """
        Return the native speed measurement required to achieve desired rotations-per-minute
        """
        assert abs(self.rotations_per_minute) <= motor.max_rpm, \
            "invalid rotations-per-minute: {} max RPM is {}, {} was requested".format(
                motor, motor.max_rpm, self.rotations_per_minute)
        return self.rotations_per_minute / motor.max_rpm * motor.max_speed


class SpeedDPS(SpeedValue):
    """
    Speed in degrees-per-second.
    """


    def __init__(self, degrees_per_second):
        self.degrees_per_second = degrees_per_second


    def __str__(self):
        return str(self.degrees_per_second) + " deg/sec"


    def __mul__(self, other):
        assert isinstance(other, (float, int)), "{} can only be multiplied by an int or float".format(self)
        return SpeedDPS(self.degrees_per_second * other)


    def to_native_units(self, motor):
        """
        Return the native speed measurement required to achieve desired degrees-per-second
        """
        assert abs(self.degrees_per_second) <= motor.max_dps, \
            "invalid degrees-per-second: {} max DPS is {}, {} was requested".format(
                motor, motor.max_dps, self.degrees_per_second)
        return self.degrees_per_second / motor.max_dps * motor.max_speed


class SpeedDPM(SpeedValue):
    """
    Speed in degrees-per-minute.
    """


    def __init__(self, degrees_per_minute):
        self.degrees_per_minute = degrees_per_minute


    def __str__(self):
        return str(self.degrees_per_minute) + " deg/min"


    def __mul__(self, other):
        assert isinstance(other, (float, int)), "{} can only be multiplied by an int or float".format(self)
        return SpeedDPM(self.degrees_per_minute * other)


    def to_native_units(self, motor):
        """
        Return the native speed measurement required to achieve desired degrees-per-minute
        """
        assert abs(self.degrees_per_minute) <= motor.max_dpm, \
            "invalid degrees-per-minute: {} max DPM is {}, {} was requested".format(
                motor, motor.max_dpm, self.degrees_per_minute)
        return self.degrees_per_minute / motor.max_dpm * motor.max_speed


class Motor(MockMotor):

    def __init__(self, address, job_handler, **kwargs):
        super(Motor, self).__init__(address, job_handler)


class LargeMotor(Motor):
    """
    EV3/NXT large servo motor.

    Same as :class:`Motor`, except it will only successfully initialize if it finds a "large" motor.
    """

    SYSTEM_CLASS_NAME = Motor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = []


    def __init__(self, address, job_handler, **kwargs):
        super(LargeMotor, self).__init__(address, job_handler,
                                         driver_name=['lego-ev3-l-motor', 'lego-nxt-motor'], **kwargs)


class MediumMotor(Motor):
    """
    EV3 medium servo motor.

    Same as :class:`Motor`, except it will only successfully initialize if it finds a "medium" motor.
    """

    SYSTEM_CLASS_NAME = Motor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = []


    def __init__(self, address, job_handler, **kwargs):
        super(MediumMotor, self).__init__(address, job_handler,
                                          driver_name=['lego-ev3-m-motor'], **kwargs)


class MotorSet(object):

    def __init__(self, motor_specs, job_handler, desc=None):
        """
        motor_specs is a dictionary such as
        {
            OUTPUT_A : LargeMotor,
            OUTPUT_C : LargeMotor,
        }
        """
        self.motors = OrderedDict()
        for motor_port in sorted(motor_specs.keys()):
            motor_class = motor_specs[motor_port]
            self.motors[motor_port] = motor_class(motor_port, job_handler)
            self.motors[motor_port].reset()

        self.desc = desc


    def __str__(self):

        if self.desc:
            return self.desc
        else:
            return self.__class__.__name__


    def set_args(self, **kwargs):
        motors = kwargs.get('motors', self.motors.values())

        for motor in motors:
            for key in kwargs:
                if key != 'motors':
                    try:
                        setattr(motor, key, kwargs[key])
                    except AttributeError as e:
                        # log.error("%s %s cannot set %s to %s" % (self, motor, key, kwargs[key]))
                        raise e


    def set_polarity(self, polarity, motors=None):
        valid_choices = (LargeMotor.POLARITY_NORMAL, LargeMotor.POLARITY_INVERSED)

        assert polarity in valid_choices, \
            "%s is an invalid polarity choice, must be %s" % (polarity, ', '.join(valid_choices))
        motors = motors if motors is not None else self.motors.values()

        for motor in motors:
            motor.polarity = polarity


    def _run_command(self, **kwargs):
        motors = kwargs.get('motors', self.motors.values())

        for motor in motors:
            for key in kwargs:
                if key not in ('motors', 'commands'):
                    # log.debug("%s: %s set %s to %s" % (self, motor, key, kwargs[key]))
                    setattr(motor, key, kwargs[key])

        for motor in motors:
            motor.command = kwargs['command']
            # log.debug("%s: %s command %s" % (self, motor, kwargs['command']))


    def run_forever(self, **kwargs):
        kwargs['command'] = LargeMotor.COMMAND_RUN_FOREVER
        self._run_command(**kwargs)


    def run_to_abs_pos(self, **kwargs):
        kwargs['command'] = LargeMotor.COMMAND_RUN_TO_ABS_POS
        self._run_command(**kwargs)


    def run_to_rel_pos(self, **kwargs):
        kwargs['command'] = LargeMotor.COMMAND_RUN_TO_REL_POS
        self._run_command(**kwargs)


    def run_timed(self, **kwargs):
        kwargs['command'] = LargeMotor.COMMAND_RUN_TIMED
        self._run_command(**kwargs)


    def run_direct(self, **kwargs):
        kwargs['command'] = LargeMotor.COMMAND_RUN_DIRECT
        self._run_command(**kwargs)


    def reset(self, motors=None):
        motors = motors if motors is not None else self.motors.values()

        for motor in motors:
            motor.reset()


    def off(self, motors=None, brake=True):
        """
        Stop motors immediately. Configure motors to brake if ``brake`` is set.
        """
        motors = motors if motors is not None else self.motors.values()

        for motor in motors:
            motor._set_brake(brake)

        for motor in motors:
            motor.stop()


    def stop(self, motors=None, brake=True):
        """
        ``stop`` is an alias of ``off``.  This is deprecated but helps keep
        the API for MotorSet somewhat similar to Motor which has both ``stop``
        and ``off``.
        """
        self.off(motors, brake)


    def _is_state(self, motors, state):
        motors = motors if motors is not None else self.motors.values()

        for motor in motors:
            if state not in motor.state:
                return False

        return True


    @property
    def is_running(self, motors=None):
        return self._is_state(motors, LargeMotor.STATE_RUNNING)


    @property
    def is_ramping(self, motors=None):
        return self._is_state(motors, LargeMotor.STATE_RAMPING)


    @property
    def is_holding(self, motors=None):
        return self._is_state(motors, LargeMotor.STATE_HOLDING)


    @property
    def is_overloaded(self, motors=None):
        return self._is_state(motors, LargeMotor.STATE_OVERLOADED)


    @property
    def is_stalled(self, motors=None):
        return self._is_state(motors, LargeMotor.STATE_STALLED)


    def wait(self, cond, timeout=None, motors=None):
        motors = motors if motors is not None else self.motors.values()

        for motor in motors:
            motor.wait(cond, timeout)


    def wait_until_not_moving(self, timeout=None, motors=None):
        motors = motors if motors is not None else self.motors.values()

        for motor in motors:
            motor.wait_until_not_moving(timeout)


    def wait_until(self, s, timeout=None, motors=None):
        motors = motors if motors is not None else self.motors.values()

        for motor in motors:
            motor.wait_until(s, timeout)


    def wait_while(self, s, timeout=None, motors=None):
        motors = motors if motors is not None else self.motors.values()

        for motor in motors:
            motor.wait_while(s, timeout)


    def _block(self):
        self.wait_until('running', timeout=WAIT_RUNNING_TIMEOUT)
        self.wait_until_not_moving()


class MoveTank(MotorSet):
    """
    Controls a pair of motors simultaneously, via individual speed setpoints for each motor.

    Example:

    .. code:: python

        tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
        # drive in a turn for 10 rotations of the outer motor
        tank_drive.on_for_rotations(50, 75, 10)
    """


    def __init__(self, left_motor_port, right_motor_port, job_handler, desc=None, motor_class=LargeMotor):
        motor_specs = {
            left_motor_port: motor_class,
            right_motor_port: motor_class,
        }

        MotorSet.__init__(self, motor_specs, job_handler, desc)
        self.left_motor = self.motors[left_motor_port]
        self.right_motor = self.motors[right_motor_port]
        self.max_speed = self.left_motor.max_speed

        # color sensor used by follow_line()
        self.cs = None


    def _unpack_speeds_to_native_units(self, left_speed, right_speed):
        left_speed = self.left_motor._speed_native_units(left_speed, "left_speed")
        right_speed = self.right_motor._speed_native_units(right_speed, "right_speed")

        return (
            left_speed,
            right_speed
        )


    def on_for_degrees(self, left_speed, right_speed, degrees, brake=True, block=True):
        """
        Rotate the motors at 'left_speed & right_speed' for 'degrees'. Speeds
        can be percentages or any SpeedValue implementation.

        If the left speed is not equal to the right speed (i.e., the robot will
        turn), the motor on the outside of the turn will rotate for the full
        ``degrees`` while the motor on the inside will have its requested
        distance calculated according to the expected turn.
        """
        (left_speed_native_units, right_speed_native_units) = self._unpack_speeds_to_native_units(left_speed,
                                                                                                  right_speed)

        # proof of the following distance calculation: consider the circle formed by each wheel's path
        # v_l = d_l/t, v_r = d_r/t
        # therefore, t = d_l/v_l = d_r/v_r

        if degrees == 0 or (left_speed_native_units == 0 and right_speed_native_units == 0):
            left_degrees = degrees
            right_degrees = degrees

        # larger speed by magnitude is the "outer" wheel, and rotates the full "degrees"
        elif abs(left_speed_native_units) > abs(right_speed_native_units):
            left_degrees = degrees
            right_degrees = abs(right_speed_native_units / left_speed_native_units) * degrees

        else:
            left_degrees = abs(left_speed_native_units / right_speed_native_units) * degrees
            right_degrees = degrees

        # Set all parameters
        self.left_motor._set_rel_position_degrees_and_speed_sp(left_degrees, left_speed_native_units)
        self.left_motor._set_brake(brake)
        self.right_motor._set_rel_position_degrees_and_speed_sp(right_degrees, right_speed_native_units)
        self.right_motor._set_brake(brake)

        log.debug("{}: on_for_degrees {}".format(self, degrees))

        # These debugs involve disk I/O to pull position and position_sp so only uncomment
        # if you need to troubleshoot in more detail.
        # log.debug("{}: left_speed {}, left_speed_native_units {}, left_degrees {}, left-position {}->{}".format(
        #     self, left_speed, left_speed_native_units, left_degrees,
        #     self.left_motor.position, self.left_motor.position_sp))
        # log.debug("{}: right_speed {}, right_speed_native_units {}, right_degrees {}, right-position {}->{}".format(
        #     self, right_speed, right_speed_native_units, right_degrees,
        #     self.right_motor.position, self.right_motor.position_sp))

        # Start the motors
        self.left_motor.run_to_rel_pos()
        self.right_motor.run_to_rel_pos()

        if block:
            self._block()


    def on_for_rotations(self, left_speed, right_speed, rotations, brake=True, block=True):
        """
        Rotate the motors at 'left_speed & right_speed' for 'rotations'. Speeds
        can be percentages or any SpeedValue implementation.

        If the left speed is not equal to the right speed (i.e., the robot will
        turn), the motor on the outside of the turn will rotate for the full
        ``rotations`` while the motor on the inside will have its requested
        distance calculated according to the expected turn.
        """
        MoveTank.on_for_degrees(self, left_speed, right_speed, rotations * 360, brake, block)


    def on_for_seconds(self, left_speed, right_speed, seconds, brake=True, block=True):
        """
        Rotate the motors at 'left_speed & right_speed' for 'seconds'. Speeds
        can be percentages or any SpeedValue implementation.
        """

        if seconds < 0:
            raise ValueError("seconds is negative ({})".format(seconds))

        (left_speed_native_units, right_speed_native_units) = self._unpack_speeds_to_native_units(left_speed,
                                                                                                  right_speed)

        # Set all parameters
        self.left_motor.speed_sp = int(round(left_speed_native_units))
        self.left_motor.time_sp = int(seconds * 1000)
        self.left_motor._set_brake(brake)
        self.right_motor.speed_sp = int(round(right_speed_native_units))
        self.right_motor.time_sp = int(seconds * 1000)
        self.right_motor._set_brake(brake)

        log.debug("%s: on_for_seconds %ss at left-speed %s, right-speed %s" %
                  (self, seconds, left_speed, right_speed))

        # Start the motors
        self.left_motor.run_timed()
        self.right_motor.run_timed()

        if block:
            self._block()


    def on(self, left_speed, right_speed):
        """
        Start rotating the motors according to ``left_speed`` and ``right_speed`` forever.
        Speeds can be percentages or any SpeedValue implementation.
        """
        (left_speed_native_units, right_speed_native_units) = self._unpack_speeds_to_native_units(left_speed,
                                                                                                  right_speed)

        # Set all parameters
        self.left_motor.speed_sp = int(round(left_speed_native_units))
        self.right_motor.speed_sp = int(round(right_speed_native_units))

        # This debug involves disk I/O to pull speed_sp so only uncomment
        # if you need to troubleshoot in more detail.
        # log.debug("%s: on at left-speed %s, right-speed %s" %
        #     (self, self.left_motor.speed_sp, self.right_motor.speed_sp))

        # Start the motors
        self.left_motor.run_forever()
        self.right_motor.run_forever()


class MoveSteering(MoveTank):
    """
    Controls a pair of motors simultaneously, via a single "steering" value and a speed.

    steering [-100, 100]:
        * -100 means turn left on the spot (right motor at 100% forward, left motor at 100% backward),
        *  0   means drive in a straight line, and
        *  100 means turn right on the spot (left motor at 100% forward, right motor at 100% backward).

    "steering" can be any number between -100 and 100.

    Example:

    .. code:: python

        steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
        # drive in a turn for 10 rotations of the outer motor
        steering_drive.on_for_rotations(-20, SpeedPercent(75), 10)
    """


    def on_for_rotations(self, steering, speed, rotations, brake=True, block=True):
        """
        Rotate the motors according to the provided ``steering``.

        The distance each motor will travel follows the rules of :meth:`MoveTank.on_for_rotations`.
        """
        (left_speed, right_speed) = self.get_speed_steering(steering, speed)
        MoveTank.on_for_rotations(self, SpeedNativeUnits(left_speed), SpeedNativeUnits(right_speed), rotations, brake,
                                  block)


    def on_for_degrees(self, steering, speed, degrees, brake=True, block=True):
        """
        Rotate the motors according to the provided ``steering``.

        The distance each motor will travel follows the rules of :meth:`MoveTank.on_for_degrees`.
        """
        (left_speed, right_speed) = self.get_speed_steering(steering, speed)
        MoveTank.on_for_degrees(self, SpeedNativeUnits(left_speed), SpeedNativeUnits(right_speed), degrees, brake,
                                block)


    def on_for_seconds(self, steering, speed, seconds, brake=True, block=True):
        """
        Rotate the motors according to the provided ``steering`` for ``seconds``.
        """
        (left_speed, right_speed) = self.get_speed_steering(steering, speed)
        MoveTank.on_for_seconds(self, SpeedNativeUnits(left_speed), SpeedNativeUnits(right_speed), seconds, brake,
                                block)


    def on(self, steering, speed):
        """
        Start rotating the motors according to the provided ``steering`` and
        ``speed`` forever.
        """
        (left_speed, right_speed) = self.get_speed_steering(steering, speed)
        MoveTank.on(self, SpeedNativeUnits(left_speed), SpeedNativeUnits(right_speed))


    def get_speed_steering(self, steering, speed):
        """
        Calculate the speed_sp for each motor in a pair to achieve the specified
        steering. Note that calling this function alone will not make the
        motors move, it only calculates the speed. A run_* function must be called
        afterwards to make the motors move.

        steering [-100, 100]:
            * -100 means turn left on the spot (right motor at 100% forward, left motor at 100% backward),
            *  0   means drive in a straight line, and
            *  100 means turn right on the spot (left motor at 100% forward, right motor at 100% backward).

        speed:
            The speed that should be applied to the outmost motor (the one
            rotating faster). The speed of the other motor will be computed
            automatically.
        """

        assert steering >= -100 and steering <= 100, \
            "{} is an invalid steering, must be between -100 and 100 (inclusive)".format(steering)

        # We don't have a good way to make this generic for the pair... so we
        # assume that the left motor's speed stats are the same as the right
        # motor's.
        speed = self.left_motor._speed_native_units(speed)
        left_speed = speed
        right_speed = speed
        speed_factor = (50 - abs(float(steering))) / 50

        if steering >= 0:
            right_speed *= speed_factor
        else:
            left_speed *= speed_factor

        return (left_speed, right_speed)
