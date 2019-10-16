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

import ctypes
import logging
from PIL import Image, ImageDraw
from . import get_current_platform, library_load_warning_message

log = logging.getLogger(__name__)

try:
    # This is a linux-specific module.
    # It is required by the Display class, but failure to import it may be
    # safely ignored if one just needs to run API tests on Windows.
    import fcntl
except ImportError:
    log.warning(library_load_warning_message("fcntl", "Display"))


class FbMem(object):
    """The framebuffer memory object.

    Made of:
        - the framebuffer file descriptor
        - the fix screen info struct
        - the var screen info struct
        - the mapped memory
    """

    # ------------------------------------------------------------------
    # The code is adapted from
    # https://github.com/LinkCareServices/cairotft/blob/master/cairotft/linuxfb.py
    #
    # The original code came with the following license:
    # ------------------------------------------------------------------
    # Copyright (c) 2012 Kurichan
    #
    # This program is free software. It comes without any warranty, to
    # the extent permitted by applicable law. You can redistribute it
    # and/or modify it under the terms of the Do What The Fuck You Want
    # To Public License, Version 2, as published by Sam Hocevar. See
    # http://sam.zoy.org/wtfpl/COPYING for more details.
    # ------------------------------------------------------------------

    __slots__ = ('fid', 'fix_info', 'var_info', 'mmap')

    FBIOGET_VSCREENINFO = 0x4600
    FBIOGET_FSCREENINFO = 0x4602

    FB_VISUAL_MONO01 = 0
    FB_VISUAL_MONO10 = 1

    class FixScreenInfo(ctypes.Structure):
        """The fb_fix_screeninfo from fb.h."""

        _fields_ = [
            ('id_name', ctypes.c_char * 16),
            ('smem_start', ctypes.c_ulong),
            ('smem_len', ctypes.c_uint32),
            ('type', ctypes.c_uint32),
            ('type_aux', ctypes.c_uint32),
            ('visual', ctypes.c_uint32),
            ('xpanstep', ctypes.c_uint16),
            ('ypanstep', ctypes.c_uint16),
            ('ywrapstep', ctypes.c_uint16),
            ('line_length', ctypes.c_uint32),
            ('mmio_start', ctypes.c_ulong),
            ('mmio_len', ctypes.c_uint32),
            ('accel', ctypes.c_uint32),
            ('reserved', ctypes.c_uint16 * 3),
        ]

    class VarScreenInfo(ctypes.Structure):
        class FbBitField(ctypes.Structure):
            """The fb_bitfield struct from fb.h."""

            _fields_ = [
                ('offset', ctypes.c_uint32),
                ('length', ctypes.c_uint32),
                ('msb_right', ctypes.c_uint32),
            ]


            def __str__(self):
                pass

        """The fb_var_screeninfo struct from fb.h."""

        _fields_ = [
            ('xres', ctypes.c_uint32),
            ('yres', ctypes.c_uint32),
            ('xres_virtual', ctypes.c_uint32),
            ('yres_virtual', ctypes.c_uint32),
            ('xoffset', ctypes.c_uint32),
            ('yoffset', ctypes.c_uint32),

            ('bits_per_pixel', ctypes.c_uint32),
            ('grayscale', ctypes.c_uint32),

            ('red', FbBitField),
            ('green', FbBitField),
            ('blue', FbBitField),
            ('transp', FbBitField),
        ]


        def __str__(self):
            pass

    def __init__(self, fbdev=None):
        """Create the FbMem framebuffer memory object."""

        pass


    @staticmethod
    def _open_fbdev(fbdev=None):
        """Return the framebuffer file descriptor.

        Try to use the FRAMEBUFFER
        environment variable if fbdev is not given. Use '/dev/fb0' by
        default.
        """

        pass


    @staticmethod
    def _get_fix_info(fbfid):
        """Return the fix screen info from the framebuffer file descriptor."""

        pass


    @staticmethod
    def _get_var_info(fbfid):
        """Return the var screen info from the framebuffer file descriptor."""

        pass


    @staticmethod
    def _map_fb_memory(fbfid, fix_info):
        """Map the framebuffer memory."""

        pass


class Display(FbMem):
    """
    A convenience wrapper for the FbMem class.
    Provides drawing functions from the python imaging library (PIL).
    """

    GRID_COLUMNS = 22
    GRID_COLUMN_PIXELS = 8
    GRID_ROWS = 12
    GRID_ROW_PIXELS = 10


    def __init__(self, desc='Display'):
        FbMem.__init__(self)

        pass


    def __str__(self):
        pass


    @property
    def xres(self):
        """
        Horizontal screen resolution
        """

        pass


    @property
    def yres(self):
        """
        Vertical screen resolution
        """

        pass


    @property
    def shape(self):
        """
        Dimensions of the screen.
        """

        pass


    @property
    def draw(self):
        """
        Returns a handle to PIL.ImageDraw.Draw class associated with the screen.

        Example::

            screen.draw.rectangle((10,10,60,20), fill='black')
        """

        pass


    @property
    def image(self):
        """
        Returns a handle to PIL.Image class that is backing the screen. This can
        be accessed for blitting images to the screen.

        Example::

            screen.image.paste(picture, (0, 0))
        """

        pass


    def clear(self):
        """
        Clears the screen
        """

        pass


    def _color565(self, r, g, b):
        """Convert red, green, blue components to a 16-bit 565 RGB value. Components
        should be values 0 to 255.
        """

        pass


    def _img_to_rgb565_bytes(self):

        pass


    def update(self):
        """
        Applies pending changes to the screen.
        Nothing will be drawn on the screen until this function is called.
        """

        pass


    def image_filename(self, filename, clear_screen=True, x1=0, y1=0, x2=None, y2=None):

        pass


    def line(self, clear_screen=True, x1=10, y1=10, x2=50, y2=50, line_color='black', width=1):
        """
        Draw a line from (x1, y1) to (x2, y2)
        """

        pass


    def circle(self, clear_screen=True, x=50, y=50, radius=40, fill_color='black', outline_color='black'):
        """
        Draw a circle of 'radius' centered at (x, y)
        """

        pass


    def rectangle(self, clear_screen=True, x1=10, y1=10, x2=80, y2=40, fill_color='black', outline_color='black'):
        """
        Draw a rectangle where the top left corner is at (x1, y1) and the
        bottom right corner is at (x2, y2)
        """

        pass


    def point(self, clear_screen=True, x=10, y=10, point_color='black'):
        """
        Draw a single pixel at (x, y)
        """

        pass


    def text_pixels(self, text, clear_screen=True, x=0, y=0, text_color='black', font=None):
        """
        Display `text` starting at pixel (x, y).

        The EV3 display is 178x128 pixels

        - (0, 0) would be the top left corner of the display
        - (89, 64) would be right in the middle of the display

        'text_color' : PIL says it supports "common HTML color names". There
        are 140 HTML color names listed here that are supported by all modern
        browsers. This is probably a good list to start with.
        https://www.w3schools.com/colors/colors_names.asp

        'font' : can be any font displayed here
            http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/display.html#bitmap-fonts

        - If font is a string, it is the name of a font to be loaded.
        - If font is a Font object, returned from :meth:`ev3dev2.fonts.load`, then it is
          used directly.  This is desirable for faster display times.

        """

        pass


    def text_grid(self, text, clear_screen=True, x=0, y=0, text_color='black', font=None):
        """
        Display 'text' starting at grid (x, y)

        The EV3 display can be broken down in a grid that is 22 columns wide
        and 12 rows tall. Each column is 8 pixels wide and each row is 10
        pixels tall.

        'text_color' : PIL says it supports "common HTML color names". There
        are 140 HTML color names listed here that are supported by all modern
        browsers. This is probably a good list to start with.
        https://www.w3schools.com/colors/colors_names.asp

        'font' : can be any font displayed here
            http://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/ev3dev-stretch/display.html#bitmap-fonts

        - If font is a string, it is the name of a font to be loaded.
        - If font is a Font object, returned from :meth:`ev3dev2.fonts.load`, then it is
          used directly.  This is desirable for faster display times.

        """

        pass


    def reset_screen(self):

        pass
