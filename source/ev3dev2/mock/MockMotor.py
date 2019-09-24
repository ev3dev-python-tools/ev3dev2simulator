import time

import ev3dev2.Motor
from ev3dev2.mock.MockDevice import MockDevice
# The number of milliseconds we wait for the state of a motor to
# update to 'running' in the "on_for_XYZ" methods of the Motor class
from ev3dev2.util.MotorConnector import *

WAIT_RUNNING_TIMEOUT = 100


class MockMotor(MockDevice):
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


    def __init__(self, address, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(MockMotor, self).__init__()

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

        self.connector = MotorConnector(self.address)
        self.running_until = None


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

        return self._state


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


    def stop(self):
        """
        Stop any of the run commands before they are complete using the
        action specified by `stop_action`.
        """

        self.command = self.COMMAND_STOP
        self.connector.stop()


    def reset(self):
        """
        Reset all of the motor parameter attributes to their default value.
        This will also have the effect of stopping the motor.
        """

        self.command = self.COMMAND_RESET
        self.connector.stop()


    @property
    def is_running(self):
        """
        Power is being sent to the motor.
        """

        # check if robot_state queue is not empty
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

        # check if robot_state queue is empty
        return self.STATE_HOLDING in self.state


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
        if not isinstance(speed, ev3dev2.Motor.SpeedValue):
            assert -100 <= speed <= 100, \
                "{}{} is an invalid speed percentage, must be between -100 and 100 (inclusive)".format(
                    "" if label is None else (label + ": "), speed)
            speed = ev3dev2.Motor.SpeedPercent(speed)

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
