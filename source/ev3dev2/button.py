# -----------------------------------------------------------------------------
# Copyright (c) 2015 Ralph Hempel <rhempel@hempeldesigngroup.com>
# Copyright (c) 2015 Anton Vanhoucke <antonvh@gmail.com>
# Copyright (c) 2015 Denis Demidov <dennis.demidov@gmail.com>
# Copyright (c) 2015 Eric Pascual <eric@pobot.org>
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

if sys.version_info < (3, 4):
    raise SystemError('Must be using Python 3.4 or higher')

from logging import getLogger

log = getLogger(__name__)


class MissingButton(Exception):
    pass


class ButtonCommon(object):

    def __str__(self):
        return self.__class__.__name__


    @staticmethod
    def on_change(changed_buttons):
        """
        This handler is called by `process()` whenever state of any button has
        changed since last `process()` call. `changed_buttons` is a list of
        tuples of changed button names and their states.
        """

        pass


    @property
    def buttons_pressed(self):
        raise NotImplementedError()


    def any(self):
        """
        Checks if any button is pressed.
        """

        pass


    def check_buttons(self, buttons=[]):
        """
        Check if currently pressed buttons exactly match the given list.
        """

        pass


    def _wait(self, wait_for_button_press, wait_for_button_release, timeout_ms):
        raise NotImplementedError()


    def wait_for_pressed(self, buttons, timeout_ms=None):
        """
        Wait for the button to be pressed down.
        """

        pass


    def wait_for_released(self, buttons, timeout_ms=None):
        """
        Wait for the button to be released.
        """

        pass


    def wait_for_bump(self, buttons, timeout_ms=None):
        """
        Wait for the button to be pressed down and then released.
        Both actions must happen within timeout_ms.
        """

        pass


    def process(self, new_state=None):
        """
        Check for currenly pressed buttons. If the new state differs from the
        old state, call the appropriate button event handlers (on_up, on_down, etc).
        """

        pass


class EV3ButtonCommon(object):
    # These handlers are called by `ButtonCommon.process()` whenever the
    # state of 'up', 'down', etc buttons have changed since last
    # `ButtonCommon.process()` call
    on_up = None
    on_down = None
    on_left = None
    on_right = None
    on_enter = None
    on_backspace = None


    @property
    def up(self):
        """
        Check if 'up' button is pressed.
        """

        pass


    @property
    def down(self):
        """
        Check if 'down' button is pressed.
        """

        pass


    @property
    def left(self):
        """
        Check if 'left' button is pressed.
        """

        pass


    @property
    def right(self):
        """
        Check if 'right' button is pressed.
        """

        pass


    @property
    def enter(self):
        """
        Check if 'enter' button is pressed.
        """

        pass


    @property
    def backspace(self):
        """
        Check if 'backspace' button is pressed.
        """

        pass
