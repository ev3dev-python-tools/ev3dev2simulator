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
import _thread
import sys
import time
import math
from collections import OrderedDict

from ev3dev2 import Device
from ev3dev2simulator.connector.motor_connector import MotorConnector

if sys.version_info < (3, 4):
    raise SystemError('Must be using Python 3.4 or higher')

from logging import getLogger
from ev3dev2.stopwatch import StopWatch
from ev3dev2._platform.ev3 import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

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


class Motor(Device):
    """
    The motor class provides a uniform interface for using motors with
    positional and directional feedback such as the EV3 and NXT motors.
    This feedback allows for precise control of the motors. This is the
    most common type of motor, so we just call it `motor`.
    """

    SYSTEM_CLASS_NAME = 'tacho-motor'
    SYSTEM_DEVICE_NAME_CONVENTION = '*'

    __slots__ = [
        '_address',
        '_command',
        '_commands',
        '_count_per_rot',
        '_count_per_m',
        '_driver_name',
        '_duty_cycle',
        '_duty_cycle_sp',
        '_full_travel_count',
        '_polarity',
        '_position',
        '_position_p',
        '_position_i',
        '_position_d',
        '_position_sp',
        '_max_speed',
        '_speed',
        '_speed_sp',
        '_ramp_up_sp',
        '_ramp_down_sp',
        '_speed_p',
        '_speed_i',
        '_speed_d',
        '_state',
        '_stop_action',
        '_stop_actions',
        '_time_sp',
        '_poll',
        'max_rps',
        'max_rpm',
        'max_dps',
        'max_dpm',
        'connector',
        'running_until',
    ]

    #: Run the motor until another command is sent.
    COMMAND_RUN_FOREVER = 'run-forever'

    #: Run to an absolute position specified by `position_sp` and then
    #: stop using the action specified in `stop_action`.
    COMMAND_RUN_TO_ABS_POS = 'run-to-abs-pos'

    #: Run to a position relative to the current `position` value.
    #: The new position will be current `position` + `position_sp`.
    #: When the new position is reached, the motor will stop using
    #: the action specified by `stop_action`.
    COMMAND_RUN_TO_REL_POS = 'run-to-rel-pos'

    #: Run the motor for the amount of time specified in `time_sp`
    #: and then stop the motor using the action specified by `stop_action`.
    COMMAND_RUN_TIMED = 'run-timed'

    #: Run the motor at the duty cycle specified by `duty_cycle_sp`.
    #: Unlike other run commands, changing `duty_cycle_sp` while running *will*
    #: take effect immediately.
    COMMAND_RUN_DIRECT = 'run-direct'

    #: Stop any of the run commands before they are complete using the
    #: action specified by `stop_action`.
    COMMAND_STOP = 'stop'

    #: Reset all of the motor parameter attributes to their default value.
    #: This will also have the effect of stopping the motor.
    COMMAND_RESET = 'reset'

    #: Sets the normal polarity of the rotary encoder.
    ENCODER_POLARITY_NORMAL = 'normal'

    #: Sets the inversed polarity of the rotary encoder.
    ENCODER_POLARITY_INVERSED = 'inversed'

    #: With `normal` polarity, a positive duty cycle will
    #: cause the motor to rotate clockwise.
    POLARITY_NORMAL = 'normal'

    #: With `inversed` polarity, a positive duty cycle will
    #: cause the motor to rotate counter-clockwise.
    POLARITY_INVERSED = 'inversed'

    #: Power is being sent to the motor.
    STATE_RUNNING = 'running'

    #: The motor is ramping up or down and has not yet reached a constant output level.
    STATE_RAMPING = 'ramping'

    #: The motor is not turning, but rather attempting to hold a fixed position.
    STATE_HOLDING = 'holding'

    #: The motor is turning, but cannot reach its `speed_sp`.
    STATE_OVERLOADED = 'overloaded'

    #: The motor is not turning when it should be.
    STATE_STALLED = 'stalled'

    #: Power will be removed from the motor and it will freely coast to a stop.
    STOP_ACTION_COAST = 'coast'

    #: Power will be removed from the motor and a passive electrical load will
    #: be placed on the motor. This is usually done by shorting the motor terminals
    #: together. This load will absorb the energy from the rotation of the motors and
    #: cause the motor to stop more quickly than coasting.
    STOP_ACTION_BRAKE = 'brake'

    #: Does not remove power from the motor. Instead it actively try to hold the motor
    #: at the current position. If an external force tries to turn the motor, the motor
    #: will `push back` to maintain its position.
    STOP_ACTION_HOLD = 'hold'


    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):

        if address is not None:
            kwargs['address'] = address
        super(Motor, self).__init__(self.SYSTEM_CLASS_NAME, name_pattern, name_exact, **kwargs)

        self._address = address
        self._command = None
        self._commands = None
        self._count_per_rot = 360  # 360
        self._count_per_m = 200  # ?
        self._driver_name = 'lego'  # lego-ev3-l-motor
        self._duty_cycle = 1  # 0
        self._duty_cycle_sp = 0  # 0
        self._full_travel_count = 100  # ?
        self._polarity = 'normal'  # 'normal'
        self._position = 0  # 0
        self._position_p = 0
        self._position_i = 0
        self._position_d = 0
        self._position_sp = 0  # 0
        self._max_speed = 1050  # 1050
        self._speed = 10  # 0
        self._speed_sp = 20
        self._ramp_up_sp = 0  # Default
        self._ramp_down_sp = 0  # Default
        self._speed_p = 1
        self._speed_i = 1
        self._speed_d = 1
        self._state = None
        self._stop_action = None
        self._stop_actions = None
        self._time_sp = 0  # 0
        self._poll = None
        self.max_rps = float(self.max_speed / self.count_per_rot)
        self.max_rpm = self.max_rps * 60
        self.max_dps = self.max_rps * 360
        self.max_dpm = self.max_rpm * 360

        self.connector = MotorConnector(self.address, self.max_speed)
        self.running_until = time.time()


    @property
    def address(self):
        """
        Returns the name of the port that this motor is connected to.
        """

        return self._address


    @property
    def command(self):
        """
        Sends a command to the motor controller. See `commands` for a list of
        possible values.
        """
        raise Exception("command is a write-only property!")


    @command.setter
    def command(self, value):
        self._command = value


    @property
    def commands(self):
        """
        Returns a list of commands that are supported by the motor
        controller. Possible values are `run-forever`, `run-to-abs-pos`, `run-to-rel-pos`,
        `run-timed`, `run-direct`, `stop` and `reset`. Not all commands may be supported.
        - `run-forever` will cause the motor to run until another command is sent.
        - `run-to-abs-pos` will run to an absolute position specified by `position_sp`
          and then stop using the action specified in `stop_action`.
        - `run-to-rel-pos` will run to a position relative to the current `position` value.
          The new position will be current `position` + `position_sp`. When the new
          position is reached, the motor will stop using the action specified by `stop_action`.
        - `run-timed` will run the motor for the amount of time specified in `time_sp`
          and then stop the motor using the action specified by `stop_action`.
        - `run-direct` will run the motor at the duty cycle specified by `duty_cycle_sp`.
          Unlike other run commands, changing `duty_cycle_sp` while running *will*
          take effect immediately.
        - `stop` will stop any of the run commands before they are complete using the
          action specified by `stop_action`.
        - `reset` will reset all of the motor parameter attributes to their default value.
          This will also have the effect of stopping the motor.
        """

        return self._commands


    @property
    def count_per_rot(self):
        """
        Returns the number of tacho counts in one rotation of the motor. Tacho counts
        are used by the position and speed attributes, so you can use this value
        to convert rotations or degrees to tacho counts. (rotation motors only)
        """

        return self._count_per_rot


    @property
    def count_per_m(self):
        """
        Returns the number of tacho counts in one meter of travel of the motor. Tacho
        counts are used by the position and speed attributes, so you can use this
        value to convert from distance to tacho counts. (linear motors only)
        """

        return self._count_per_m


    @property
    def driver_name(self):
        """
        Returns the name of the driver that provides this tacho motor device.
        """

        return self._driver_name


    @property
    def duty_cycle(self):
        """
        Returns the current duty cycle of the motor. Units are percent. Values
        are -100 to 100.
        """

        return self._duty_cycle


    @property
    def duty_cycle_sp(self):
        """
        Writing sets the duty cycle setpoint. Reading returns the current value.
        Units are in percent. Valid values are -100 to 100. A negative value causes
        the motor to rotate in reverse.
        """

        return self._duty_cycle_sp


    @duty_cycle_sp.setter
    def duty_cycle_sp(self, value):
        self._duty_cycle_sp = value
        self.connector.set_duty_cycle(value)


    @property
    def full_travel_count(self):
        """
        Returns the number of tacho counts in the full travel of the motor. When
        combined with the `count_per_m` atribute, you can use this value to
        calculate the maximum travel distance of the motor. (linear motors only)
        """

        return self._full_travel_count


    @property
    def polarity(self):
        """
        Sets the polarity of the motor. With `normal` polarity, a positive duty
        cycle will cause the motor to rotate clockwise. With `inversed` polarity,
        a positive duty cycle will cause the motor to rotate counter-clockwise.
        Valid values are `normal` and `inversed`.
        """

        return self._polarity


    @polarity.setter
    def polarity(self, value):
        self._polarity = value


    @property
    def position(self):
        """
        Returns the current position of the motor in pulses of the rotary
        encoder. When the motor rotates clockwise, the position will increase.
        Likewise, rotating counter-clockwise causes the position to decrease.
        Writing will set the position to that value.
        """

        return self._position


    @position.setter
    def position(self, value):
        self._position = value


    @property
    def position_p(self):
        """
        The proportional constant for the position PID.
        """

        return self._position_p


    @position_p.setter
    def position_p(self, value):
        self._position_p = value


    @property
    def position_i(self):
        """
        The integral constant for the position PID.
        """

        return self._position_i


    @position_i.setter
    def position_i(self, value):
        self._position_i = value


    @property
    def position_d(self):
        """
        The derivative constant for the position PID.
        """

        return self._position_d


    @position_d.setter
    def position_d(self, value):
        self._position_d = value


    @property
    def position_sp(self):
        """
        Writing specifies the target position for the `run-to-abs-pos` and `run-to-rel-pos`
        commands. Reading returns the current value. Units are in tacho counts. You
        can use the value returned by `count_per_rot` to convert tacho counts to/from
        rotations or degrees.
        """

        return self._position_sp


    @position_sp.setter
    def position_sp(self, value):
        self._position_sp = value
        self.connector.set_distance(value)


    @property
    def max_speed(self):
        """
        Returns the maximum value that is accepted by the `speed_sp` attribute. This
        may be slightly different than the maximum speed that a particular motor can
        reach - it's the maximum theoretical speed.
        """

        return self._max_speed


    @property
    def speed(self):
        """
        Returns the current motor speed in tacho counts per second. Note, this is
        not necessarily degrees (although it is for LEGO motors). Use the `count_per_rot`
        attribute to convert this value to RPM or deg/sec.
        """

        return self._speed


    @property
    def speed_sp(self):
        """
        Writing sets the target speed in tacho counts per second used for all `run-*`
        commands except `run-direct`. Reading returns the current value. A negative
        value causes the motor to rotate in reverse with the exception of `run-to-*-pos`
        commands where the sign is ignored. Use the `count_per_rot` attribute to convert
        RPM or deg/sec to tacho counts per second. Use the `count_per_m` attribute to
        convert m/s to tacho counts per second.
        """

        return self._speed_sp


    @speed_sp.setter
    def speed_sp(self, value):
        self._speed_sp = value
        self.connector.set_speed(value)


    @property
    def ramp_up_sp(self):
        """
        Writing sets the ramp up setpoint. Reading returns the current value. Units
        are in milliseconds and must be positive. When set to a non-zero value, the
        motor speed will increase from 0 to 100% of `max_speed` over the span of this
        setpoint. The actual ramp time is the ratio of the difference between the
        `speed_sp` and the current `speed` and max_speed multiplied by `ramp_up_sp`.
        """

        return self._ramp_up_sp


    @ramp_up_sp.setter
    def ramp_up_sp(self, value):
        self._ramp_up_sp = value


    @property
    def ramp_down_sp(self):
        """
        Writing sets the ramp down setpoint. Reading returns the current value. Units
        are in milliseconds and must be positive. When set to a non-zero value, the
        motor speed will decrease from 0 to 100% of `max_speed` over the span of this
        setpoint. The actual ramp time is the ratio of the difference between the
        `speed_sp` and the current `speed` and max_speed multiplied by `ramp_down_sp`.
        """

        return self._ramp_down_sp


    @ramp_down_sp.setter
    def ramp_down_sp(self, value):
        self._ramp_down_sp = value


    @property
    def speed_p(self):
        """
        The proportional constant for the speed regulation PID.
        """

        return self._speed_p


    @speed_p.setter
    def speed_p(self, value):
        self._speed_p = value


    @property
    def speed_i(self):
        """
        The integral constant for the speed regulation PID.
        """

        return self._speed_i


    @speed_i.setter
    def speed_i(self, value):
        self._speed_i = value


    @property
    def speed_d(self):
        """
        The derivative constant for the speed regulation PID.
        """

        return self._speed_d


    @speed_d.setter
    def speed_d(self, value):
        self._speed_d = value


    @property
    def state(self):
        """
        Reading returns a list of state flags. Possible flags are
        `running`, `ramping`, `holding`, `overloaded` and `stalled`.
        """

        if time.time() < self.running_until:
            return Motor.STATE_RUNNING
        else:
            return Motor.STATE_HOLDING


    @property
    def stop_action(self):
        """
        Reading returns the current stop action. Writing sets the stop action.
        The value determines the motors behavior when `command` is set to `stop`.
        Also, it determines the motors behavior when a run command completes. See
        `stop_actions` for a list of possible values.
        """

        return self._stop_action


    @stop_action.setter
    def stop_action(self, value):
        self._stop_action = value
        self.connector.set_stop_action(value)


    @property
    def stop_actions(self):
        """
        Returns a list of stop actions supported by the motor controller.
        Possible values are `coast`, `brake` and `hold`. `coast` means that power will
        be removed from the motor and it will freely coast to a stop. `brake` means
        that power will be removed from the motor and a passive electrical load will
        be placed on the motor. This is usually done by shorting the motor terminals
        together. This load will absorb the energy from the rotation of the motors and
        cause the motor to stop more quickly than coasting. `hold` does not remove
        power from the motor. Instead it actively tries to hold the motor at the current
        position. If an external force tries to turn the motor, the motor will 'push
        back' to maintain its position.
        """

        return self._stop_actions


    @property
    def time_sp(self):
        """
        Writing specifies the amount of time the motor will run when using the
        `run-timed` command. Reading returns the current value. Units are in
        milliseconds.
        """

        return self._time_sp


    @time_sp.setter
    def time_sp(self, value):
        self._time_sp = value
        self.connector.set_time(value)


    def run_forever(self):
        """
        Run the motor until another command is sent.
        """

        self.command = self.COMMAND_RUN_FOREVER

        run_time = self.connector.run_forever()
        self.running_until = time.time() + run_time


    def run_to_abs_pos(self):
        """
        Run to an absolute position specified by `position_sp` and then
        stop using the action specified in `stop_action`.
        """

        self._command = self.COMMAND_RUN_TO_ABS_POS

        run_time = self.connector.run_to_rel_pos()
        self.running_until = time.time() + run_time


    def run_to_rel_pos(self):
        """
        Run to a position relative to the current `position` value.
        The new position will be current `position` + `position_sp`.
        When the new position is reached, the motor will stop using
        the action specified by `stop_action`.
        """

        self.command = self.COMMAND_RUN_TO_REL_POS

        run_time = self.connector.run_to_rel_pos()
        self.running_until = time.time() + run_time


    def run_timed(self):
        """
        Run the motor for the amount of time specified in `time_sp`
        and then stop the motor using the action specified by `stop_action`.
        """

        self.command = self.COMMAND_RUN_TIMED

        run_time = self.connector.run_timed()
        self.running_until = time.time() + run_time


    def run_direct(self):
        """
        Run the motor at the duty cycle specified by `duty_cycle_sp`.
        Unlike other run commands, changing `duty_cycle_sp` while running *will*
        take effect immediately.
        """

        self.command = self.COMMAND_RUN_DIRECT

        run_time = self.connector.run_direct()
        self.running_until = time.time() + run_time


    def stop(self):
        """
        Stop any of the run commands before they are complete using the
        action specified by `stop_action`.
        """

        self.command = self.COMMAND_STOP

        run_time = self.connector.stop()
        self.running_until = time.time() + run_time


    def reset(self):
        """
        Reset all of the motor parameter attributes to their default value.
        This will also have the effect of stopping the motor.
        """

        self.command = self.COMMAND_RESET

        run_time = self.connector.stop()
        self.running_until = time.time() + run_time


    @property
    def is_running(self):
        """
        Power is being sent to the motor.
        """

        return time.time() < self.running_until


    @property
    def is_ramping(self):
        """
        The motor is ramping up or down and has not yet reached a constant output level.
        """
        return False


    @property
    def is_holding(self):
        """
        The motor is not turning, but rather attempting to hold a fixed position.
        """

        return time.time() > self.running_until


    @property
    def is_overloaded(self):
        """
        The motor is turning, but cannot reach its `speed_sp`.
        """
        return False


    @property
    def is_stalled(self):
        """
        The motor is not turning when it should be.
        """
        return False


    def wait(self, cond, timeout=None):
        """
        Blocks until ``cond(self.state)`` is ``True``.  The condition is
        checked when there is an I/O event related to the ``state`` attribute.
        Exits early when ``timeout`` (in milliseconds) is reached.
        Returns ``True`` if the condition is met, and ``False`` if the timeout
        is reached.
        """

        start = time.time()

        if timeout:
            sleep_time = min(timeout, 0.1)
        else:
            sleep_time = 0.1

        while True:
            now = time.time()

            if cond(now):
                return True

            time.sleep(sleep_time)

            if timeout is not None and time.time() >= start + timeout / 1000:
                # Final check when user timeout is reached
                return cond(now)


    def wait_until_not_moving(self, timeout=None):
        """
        Blocks until ``running`` is not in ``self.state`` or ``stalled`` is in
        ``self.state``.  The condition is checked when there is an I/O event
        related to the ``state`` attribute.  Exits early when ``timeout``
        (in milliseconds) is reached.
        Returns ``True`` if the condition is met, and ``False`` if the timeout
        is reached.
        Example::
            m.wait_until_not_moving()
        """

        l = lambda now: True if self.running_until is None else self.running_until < now
        return self.wait(l, timeout)


    def wait_until(self, s, timeout=None):
        """
        Blocks until ``s`` is in ``self.state``.  The condition is checked when
        there is an I/O event related to the ``state`` attribute.  Exits early
        when ``timeout`` (in milliseconds) is reached.
        Returns ``True`` if the condition is met, and ``False`` if the timeout
        is reached.
        Example::
            m.wait_until('stalled')
        """

        l = lambda now: False if self.running_until is None else now < self.running_until
        return self.wait(l, timeout)


    def wait_while(self, s, timeout=None):
        """
        Blocks until ``s`` is not in ``self.state``.  The condition is checked
        when there is an I/O event related to the ``state`` attribute.  Exits
        early when ``timeout`` (in milliseconds) is reached.
        Returns ``True`` if the condition is met, and ``False`` if the timeout
        is reached.
        Example::
            m.wait_while('running')
        """

        l = lambda now: True if self.running_until is None else self.running_until < now
        return self.wait(l, timeout)


    def _speed_native_units(self, speed, label=None):

        # If speed is not a SpeedValue object we treat it as a percentage
        if not isinstance(speed, SpeedValue):
            assert -100 <= speed <= 100, \
                "{}{} is an invalid speed percentage, must be between -100 and 100 (inclusive)".format(
                    "" if label is None else (label + ": "), speed)
            speed = SpeedPercent(speed)

        return speed.to_native_units(self)


    def _set_rel_position_degrees_and_speed_sp(self, degrees, speed):
        degrees = degrees if speed >= 0 else -degrees
        speed = abs(speed)

        position_delta = int(round((degrees * self.count_per_rot) / 360))
        speed_sp = int(round(speed))

        self.position_sp = position_delta
        self.speed_sp = speed_sp


    def _set_brake(self, brake):
        if brake:
            self.stop_action = self.STOP_ACTION_HOLD
        else:
            self.stop_action = self.STOP_ACTION_COAST


    def on_for_rotations(self, speed, rotations, brake=True, block=True):
        """
        Rotate the motor at ``speed`` for ``rotations``
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        speed_sp = self._speed_native_units(speed)
        self._set_rel_position_degrees_and_speed_sp(rotations * 360, speed_sp)
        self._set_brake(brake)
        self.run_to_rel_pos()

        if block:
            self.wait_until('running', timeout=WAIT_RUNNING_TIMEOUT)
            self.wait_until_not_moving()


    def on_for_degrees(self, speed, degrees, brake=True, block=True):
        """
        Rotate the motor at ``speed`` for ``degrees``
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        speed_sp = self._speed_native_units(speed)
        self._set_rel_position_degrees_and_speed_sp(degrees, speed_sp)
        self._set_brake(brake)
        self.run_to_rel_pos()

        if block:
            self.wait_until('running', timeout=WAIT_RUNNING_TIMEOUT)
            self.wait_until_not_moving()


    def on_to_position(self, speed, position, brake=True, block=True):
        """
        Rotate the motor at ``speed`` to ``position``
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """
        speed = self._speed_native_units(speed)
        self.speed_sp = int(round(speed))
        self.position_sp = position
        self._set_brake(brake)
        self.run_to_abs_pos()

        if block:
            self.wait_until('running', timeout=WAIT_RUNNING_TIMEOUT)
            self.wait_until_not_moving()


    def on_for_seconds(self, speed, seconds, brake=True, block=True):
        """
        Rotate the motor at ``speed`` for ``seconds``
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        """

        if seconds < 0:
            raise ValueError("seconds is negative ({})".format(seconds))

        speed = self._speed_native_units(speed)
        self.speed_sp = int(round(speed))
        self.time_sp = int(seconds * 1000)
        self._set_brake(brake)
        self.run_timed()

        if block:
            self.wait_until('running', timeout=WAIT_RUNNING_TIMEOUT)
            self.wait_until_not_moving()


    def on(self, speed, brake=True, block=False):
        """
        Rotate the motor at ``speed`` for forever
        ``speed`` can be a percentage or a :class:`ev3dev2.motor.SpeedValue`
        object, enabling use of other units.
        Note that `block` is False by default, this is different from the
        other `on_for_XYZ` methods.
        """
        speed = self._speed_native_units(speed)
        self.speed_sp = int(round(speed))
        self._set_brake(brake)
        self.run_forever()

        if block:
            self.wait_until('running', timeout=WAIT_RUNNING_TIMEOUT)
            self.wait_until_not_moving()


    def off(self, brake=True):
        self._set_brake(brake)
        self.stop()


    @property
    def rotations(self):
        return float(self.position / self.count_per_rot)


    @property
    def degrees(self):
        return self.rotations * 360


def list_motors(name_pattern=Motor.SYSTEM_DEVICE_NAME_CONVENTION, **kwargs):
    """
    This is a generator function that enumerates all tacho motors that match
    the provided arguments.

    Parameters:
        name_pattern: pattern that device name should match.
            For example, 'motor*'. Default value: '*'.
        keyword arguments: used for matching the corresponding device
            attributes. For example, driver_name='lego-ev3-l-motor', or
            address=['outB', 'outC']. When argument value
            is a list, then a match against any entry of the list is
            enough.
    """

    pass


class LargeMotor(Motor):
    """
    EV3/NXT large servo motor.
    Same as :class:`Motor`, except it will only successfully initialize if it finds a "large" motor.
    """

    SYSTEM_CLASS_NAME = Motor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = []


    def __init__(self, address, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(LargeMotor, self).__init__(address, name_pattern, name_exact,
                                         driver_name=['lego-ev3-l-motor', 'lego-nxt-motor'], **kwargs)


class MediumMotor(Motor):
    """
    EV3 medium servo motor.
    Same as :class:`Motor`, except it will only successfully initialize if it finds a "medium" motor.
    """

    SYSTEM_CLASS_NAME = Motor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = '*'
    __slots__ = []


    def __init__(self, address, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(MediumMotor, self).__init__(address, name_pattern, name_exact,
                                          driver_name=['lego-ev3-m-motor'], **kwargs)


class MotorSet(object):

    def __init__(self, motor_specs, desc=None):
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
            self.motors[motor_port] = motor_class(motor_port)
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


# line follower classes
class LineFollowErrorLostLine(Exception):
    """
    Raised when a line following robot has lost the line
    """
    pass


class LineFollowErrorTooFast(Exception):
    """
    Raised when a line following robot has been asked to follow
    a line at an unrealistic speed
    """
    pass


# line follower functions
def follow_for_forever(tank):
    """
    ``tank``: the MoveTank object that is following a line
    """
    return True


def follow_for_ms(tank, ms):
    """
    ``tank``: the MoveTank object that is following a line
    ``ms`` : the number of milliseconds to follow the line
    """
    if not hasattr(tank, 'stopwatch') or tank.stopwatch is None:
        tank.stopwatch = StopWatch()
        tank.stopwatch.start()

    if tank.stopwatch.value_ms >= ms:
        tank.stopwatch = None
        return False
    else:
        return True


class MoveTank(MotorSet):
    """
    Controls a pair of motors simultaneously, via individual speed setpoints for each motor.
    Example:
    .. code:: python
        tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
        # drive in a turn for 10 rotations of the outer motor
        tank_drive.on_for_rotations(50, 75, 10)
    """


    def __init__(self, left_motor_port, right_motor_port, desc=None, motor_class=LargeMotor):
        motor_specs = {
            left_motor_port: motor_class,
            right_motor_port: motor_class,
        }

        MotorSet.__init__(self, motor_specs, desc)
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


    def follow_line(self,
                    kp, ki, kd,
                    speed,
                    target_light_intensity=None,
                    follow_left_edge=True,
                    white=60,
                    off_line_count_max=20,
                    sleep_time=0.01,
                    follow_for=follow_for_forever,
                    **kwargs
                    ):
        """
        PID line follower
        ``kp``, ``ki``, and ``kd`` are the PID constants.
        ``speed`` is the desired speed of the midpoint of the robot
        ``target_light_intensity`` is the reflected light intensity when the color sensor
            is on the edge of the line.  If this is None we assume that the color sensor
            is on the edge of the line and will take a reading to set this variable.
        ``follow_left_edge`` determines if we follow the left or right edge of the line
        ``white`` is the reflected_light_intensity that is used to determine if we have
            lost the line
        ``off_line_count_max`` is how many consecutive times through the loop the
            reflected_light_intensity must be greater than ``white`` before we
            declare the line lost and raise an exception
        ``sleep_time`` is how many seconds we sleep on each pass through
            the loop.  This is to give the robot a chance to react
            to the new motor settings. This should be something small such
            as 0.01 (10ms).
        ``follow_for`` is called to determine if we should keep following the
            line or stop.  This function will be passed ``self`` (the current
            ``MoveTank`` object). Current supported options are:
            - ``follow_for_forever``
            - ``follow_for_ms``
        ``**kwargs`` will be passed to the ``follow_for`` function
        Example:
        .. code:: python
            from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent, follow_for_ms
            from ev3dev2.sensor.lego import ColorSensor
            tank = MoveTank(OUTPUT_A, OUTPUT_B)
            tank.cs = ColorSensor()
            try:
                # Follow the line for 4500ms
                tank.follow_line(
                    kp=11.3, ki=0.05, kd=3.2,
                    speed=SpeedPercent(30),
                    follow_for=follow_for_ms,
                    ms=4500
                )
            except Exception:
                tank.stop()
                raise
        """
        assert self.cs, "ColorSensor must be defined"

        if target_light_intensity is None:
            target_light_intensity = self.cs.reflected_light_intensity

        integral = 0.0
        last_error = 0.0
        derivative = 0.0
        off_line_count = 0
        speed_native_units = speed.to_native_units(self.left_motor)
        MAX_SPEED = SpeedNativeUnits(self.max_speed)

        while follow_for(self, **kwargs):
            reflected_light_intensity = self.cs.reflected_light_intensity
            error = target_light_intensity - reflected_light_intensity
            integral = integral + error
            derivative = error - last_error
            last_error = error
            turn_native_units = (kp * error) + (ki * integral) + (kd * derivative)

            if not follow_left_edge:
                turn_native_units *= -1

            left_speed = SpeedNativeUnits(speed_native_units - turn_native_units)
            right_speed = SpeedNativeUnits(speed_native_units + turn_native_units)

            if left_speed > MAX_SPEED:
                log.info("%s: left_speed %s is greater than MAX_SPEED %s"  % (self, left_speed, MAX_SPEED))
                self.stop()
                raise LineFollowErrorTooFast("The robot is moving too fast to follow the line")

            if right_speed > MAX_SPEED:
                log.info("%s: right_speed %s is greater than MAX_SPEED %s"  % (self, right_speed, MAX_SPEED))
                self.stop()
                raise LineFollowErrorTooFast("The robot is moving too fast to follow the line")

            # Have we lost the line?
            if reflected_light_intensity >= white:
                off_line_count += 1

                if off_line_count >= off_line_count_max:
                    self.stop()
                    raise LineFollowErrorLostLine("we lost the line")
            else:
                off_line_count = 0

            if sleep_time:
                time.sleep(sleep_time)

            self.on(left_speed, right_speed)

        self.stop()


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

class MoveDifferential(MoveTank):
    """
    MoveDifferential is a child of MoveTank that adds the following capabilities:
    - drive in a straight line for a specified distance
    - rotate in place in a circle (clockwise or counter clockwise) for a
      specified number of degrees
    - drive in an arc (clockwise or counter clockwise) of a specified radius
      for a specified distance
    Odometry can be use to enable driving to specific coordinates and
    rotating to a specific angle.
    New arguments:
    wheel_class - Typically a child class of :class:`ev3dev2.wheel.Wheel`. This is used to
    get the circumference of the wheels of the robot. The circumference is
    needed for several calculations in this class.
    wheel_distance_mm - The distance between the mid point of the two
    wheels of the robot. You may need to do some tests drives to find
    the correct value for your robot.  It is not as simple as measuring
    the distance between the midpoints of the two wheels. The weight of
    the robot, center of gravity, etc come into play.
    You can use utils/move_differential.py to call on_arc_left() to do
    some tests drives of circles with a radius of 200mm. Adjust your
    wheel_distance_mm until your robot can drive in a perfect circle
    and stop exactly where it started. It does not have to be a circle
    with a radius of 200mm, you can tests with any size circle but you do
    not want it to be too small or it will be difficult to tests small
    adjustments to wheel_distance_mm.
    Example:
    .. code:: python
        from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveDifferential, SpeedRPM
        from ev3dev2.wheel import EV3Tire
        STUD_MM = 8
        # tests with a robot that:
        # - uses the standard wheels known as EV3Tire
        # - wheels are 16 studs apart
        mdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3Tire, 16 * STUD_MM)
        # Rotate 90 degrees clockwise
        mdiff.turn_right(SpeedRPM(40), 90)
        # Drive forward 500 mm
        mdiff.on_for_distance(SpeedRPM(40), 500)
        # Drive in arc to the right along an imaginary circle of radius 150 mm.
        # Drive for 700 mm around this imaginary circle.
        mdiff.on_arc_right(SpeedRPM(80), 150, 700)
        # Enable odometry
        mdiff.odometry_start()
        # Use odometry to drive to specific coordinates
        mdiff.on_to_coordinates(SpeedRPM(40), 300, 300)
        # Use odometry to go back to where we started
        mdiff.on_to_coordinates(SpeedRPM(40), 0, 0)
        # Use odometry to rotate in place to 90 degrees
        mdiff.turn_to_angle(SpeedRPM(40), 90)
        # Disable odometry
        mdiff.odometry_stop()
    """

    def __init__(self, left_motor_port, right_motor_port,
            wheel_class, wheel_distance_mm,
            desc=None, motor_class=LargeMotor):

        MoveTank.__init__(self, left_motor_port, right_motor_port, desc, motor_class)
        self.wheel = wheel_class()
        self.wheel_distance_mm = wheel_distance_mm

        # The circumference of the circle made if this robot were to rotate in place
        self.circumference_mm = self.wheel_distance_mm * math.pi

        self.min_circle_radius_mm = self.wheel_distance_mm / 2

        # odometry variables
        self.x_pos_mm = 0.0  # robot X position in mm
        self.y_pos_mm = 0.0  # robot Y position in mm
        self.odometry_thread_run = False
        self.odometry_thread_id = None
        self.theta = 0.0

    def on_for_distance(self, speed, distance_mm, brake=True, block=True):
        """
        Drive distance_mm
        """
        rotations = distance_mm / self.wheel.circumference_mm
        log.debug("%s: on_for_rotations distance_mm %s, rotations %s, speed %s" % (self, distance_mm, rotations, speed))

        MoveTank.on_for_rotations(self, speed, speed, rotations, brake, block)

    def _on_arc(self, speed, radius_mm, distance_mm, brake, block, arc_right):
        """
        Drive in a circle with 'radius' for 'distance'
        """

        if radius_mm < self.min_circle_radius_mm:
            raise ValueError("{}: radius_mm {} is less than min_circle_radius_mm {}" .format(
                    self, radius_mm, self.min_circle_radius_mm))

        # The circle formed at the halfway point between the two wheels is the
        # circle that must have a radius of radius_mm
        circle_outer_mm = 2 * math.pi * (radius_mm + (self.wheel_distance_mm / 2))
        circle_middle_mm = 2 * math.pi * radius_mm
        circle_inner_mm = 2 * math.pi * (radius_mm - (self.wheel_distance_mm / 2))

        if arc_right:
            # The left wheel is making the larger circle and will move at 'speed'
            # The right wheel is making a smaller circle so its speed will be a fraction of the left motor's speed
            left_speed = speed
            right_speed = float(circle_inner_mm/circle_outer_mm) * left_speed

        else:
            # The right wheel is making the larger circle and will move at 'speed'
            # The left wheel is making a smaller circle so its speed will be a fraction of the right motor's speed
            right_speed = speed
            left_speed = float(circle_inner_mm/circle_outer_mm) * right_speed

        log.debug("%s: arc %s, radius %s, distance %s, left-speed %s, right-speed %s, circle_outer_mm %s, circle_middle_mm %s, circle_inner_mm %s" %
            (self, "right" if arc_right else "left",
             radius_mm, distance_mm, left_speed, right_speed,
             circle_outer_mm, circle_middle_mm, circle_inner_mm
            )
        )

        # We know we want the middle circle to be of length distance_mm so
        # calculate the percentage of circle_middle_mm we must travel for the
        # middle of the robot to travel distance_mm.
        circle_middle_percentage = float(distance_mm / circle_middle_mm)

        # Now multiple that percentage by circle_outer_mm to calculate how
        # many mm the outer wheel should travel.
        circle_outer_final_mm = circle_middle_percentage * circle_outer_mm

        outer_wheel_rotations = float(circle_outer_final_mm / self.wheel.circumference_mm)
        outer_wheel_degrees = outer_wheel_rotations * 360

        log.debug("%s: arc %s, circle_middle_percentage %s, circle_outer_final_mm %s, outer_wheel_rotations %s, outer_wheel_degrees %s" %
            (self, "right" if arc_right else "left",
             circle_middle_percentage, circle_outer_final_mm,
             outer_wheel_rotations, outer_wheel_degrees
            )
        )

        MoveTank.on_for_degrees(self, left_speed, right_speed, outer_wheel_degrees, brake, block)

    def on_arc_right(self, speed, radius_mm, distance_mm, brake=True, block=True):
        """
        Drive clockwise in a circle with 'radius_mm' for 'distance_mm'
        """
        self._on_arc(speed, radius_mm, distance_mm, brake, block, True)

    def on_arc_left(self, speed, radius_mm, distance_mm, brake=True, block=True):
        """
        Drive counter-clockwise in a circle with 'radius_mm' for 'distance_mm'
        """
        self._on_arc(speed, radius_mm, distance_mm, brake, block, False)

    def _turn(self, speed, degrees, brake=True, block=True):
        """
        Rotate in place 'degrees'. Both wheels must turn at the same speed for us
        to rotate in place.
        """

        # The distance each wheel needs to travel
        distance_mm = (abs(degrees) / 360) * self.circumference_mm

        # The number of rotations to move distance_mm
        rotations = distance_mm/self.wheel.circumference_mm

        log.debug("%s: turn() degrees %s, distance_mm %s, rotations %s, degrees %s" %
            (self, degrees, distance_mm, rotations, degrees))

        # If degrees is positive rotate clockwise
        if degrees > 0:
            MoveTank.on_for_rotations(self, speed, speed * -1, rotations, brake, block)

        # If degrees is negative rotate counter-clockwise
        else:
            rotations = distance_mm / self.wheel.circumference_mm
            MoveTank.on_for_rotations(self, speed * -1, speed, rotations, brake, block)

    def turn_right(self, speed, degrees, brake=True, block=True):
        """
        Rotate clockwise 'degrees' in place
        """
        self._turn(speed, abs(degrees), brake, block)

    def turn_left(self, speed, degrees, brake=True, block=True):
        """
        Rotate counter-clockwise 'degrees' in place
        """
        self._turn(speed, abs(degrees) * -1, brake, block)

    def odometry_coordinates_log(self):
        log.debug("%s: odometry angle %s at (%d, %d)" %
            (self, math.degrees(self.theta), self.x_pos_mm, self.y_pos_mm))

    def odometry_start(self, theta_degrees_start=90.0,
            x_pos_start=0.0, y_pos_start=0.0,
            sleep_time=0.005):  # 5ms
        """
        Ported from:
        http://seattlerobotics.org/encoder/200610/Article3/IMU%20Odometry,%20by%20David%20Anderson.htm
        A thread is started that will run until the user calls odometry_stop()
        which will set odometry_thread_run to False
        """

        def _odometry_monitor():
            left_previous = 0
            right_previous = 0
            self.theta = math.radians(theta_degrees_start)  # robot heading
            self.x_pos_mm = x_pos_start  # robot X position in mm
            self.y_pos_mm = y_pos_start  # robot Y position in mm
            TWO_PI = 2 * math.pi

            while self.odometry_thread_run:

                # sample the left and right encoder counts as close together
                # in time as possible
                left_current = self.left_motor.position
                right_current = self.right_motor.position

                # determine how many ticks since our last sampling
                left_ticks = left_current - left_previous
                right_ticks = right_current - right_previous

                # Have we moved?
                if not left_ticks and not right_ticks:
                    if sleep_time:
                        time.sleep(sleep_time)
                    continue

                # log.debug("%s: left_ticks %s (from %s to %s)" %
                #     (self, left_ticks, left_previous, left_current))
                # log.debug("%s: right_ticks %s (from %s to %s)" %
                #     (self, right_ticks, right_previous, right_current))

                # update _previous for next time
                left_previous = left_current
                right_previous = right_current

                # rotations = distance_mm/self.wheel.circumference_mm
                left_rotations = float(left_ticks / self.left_motor.count_per_rot)
                right_rotations = float(right_ticks / self.right_motor.count_per_rot)

                # convert longs to floats and ticks to mm
                left_mm = float(left_rotations * self.wheel.circumference_mm)
                right_mm = float(right_rotations * self.wheel.circumference_mm)

                # calculate distance we have traveled since last sampling
                mm = (left_mm + right_mm) / 2.0

                # accumulate total rotation around our center
                self.theta += (right_mm - left_mm) / self.wheel_distance_mm

                # and clip the rotation to plus or minus 360 degrees
                self.theta -= float(int(self.theta/TWO_PI) * TWO_PI)

                # now calculate and accumulate our position in mm
                self.x_pos_mm += mm * math.cos(self.theta)
                self.y_pos_mm += mm * math.sin(self.theta)

                if sleep_time:
                    time.sleep(sleep_time)

            self.odometry_thread_id = None

        self.odometry_thread_run = True
        self.odometry_thread_id = _thread.start_new_thread(_odometry_monitor, ())

    def odometry_stop(self):
        """
        Signal the odometry thread to exit and wait for it to exit
        """

        if self.odometry_thread_id:
            self.odometry_thread_run = False

            while self.odometry_thread_id:
                pass

    def turn_to_angle(self, speed, angle_target_degrees, brake=True, block=True):
        """
        Rotate in place to `angle_target_degrees` at `speed`
        """
        assert self.odometry_thread_id, "odometry_start() must be called to track robot coordinates"

        # Make both target and current angles positive numbers between 0 and 360
        if angle_target_degrees < 0:
            angle_target_degrees += 360

        angle_current_degrees = math.degrees(self.theta)

        if angle_current_degrees < 0:
            angle_current_degrees += 360

        # Is it shorter to rotate to the right or left
        # to reach angle_target_degrees?
        if angle_current_degrees > angle_target_degrees:
            turn_right = True
            angle_delta = angle_current_degrees - angle_target_degrees
        else:
            turn_right = False
            angle_delta = angle_target_degrees - angle_current_degrees

        if angle_delta > 180:
            angle_delta = 360 - angle_delta
            turn_right = not turn_right

        log.debug("%s: turn_to_angle %s, current angle %s, delta %s, turn_right %s" %
            (self, angle_target_degrees, angle_current_degrees, angle_delta, turn_right))
        self.odometry_coordinates_log()

        if turn_right:
            self.turn_right(speed, angle_delta, brake, block)
        else:
            self.turn_left(speed, angle_delta, brake, block)

        self.odometry_coordinates_log()

    def on_to_coordinates(self, speed, x_target_mm, y_target_mm, brake=True, block=True):
        """
        Drive to (`x_target_mm`, `y_target_mm`) coordinates at `speed`
        """
        assert self.odometry_thread_id, "odometry_start() must be called to track robot coordinates"

        # stop moving
        self.off(brake='hold')

        # rotate in place so we are pointed straight at our target
        x_delta = x_target_mm - self.x_pos_mm
        y_delta = y_target_mm - self.y_pos_mm
        angle_target_radians = math.atan2(y_delta, x_delta)
        angle_target_degrees = math.degrees(angle_target_radians)
        self.turn_to_angle(speed, angle_target_degrees, brake=True, block=True)

        # drive in a straight line to the target coordinates
        distance_mm = math.sqrt(pow(self.x_pos_mm - x_target_mm, 2) + pow(self.y_pos_mm - y_target_mm, 2))
        self.on_for_distance(speed, distance_mm, brake, block)
