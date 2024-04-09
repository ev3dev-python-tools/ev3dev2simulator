"""
Module containing the ``RobotPartSprite`` class.
"""

import arcade as _arcade


class RobotPartSprite(_arcade.Sprite):
    """
    Class used to display all robot parts. Keeps the required textures and its scale.
    Only uses width, since height is scaled automatically based on the height found in the textures.
    """

    def __init__(self,
                 src_list,
                 start_sprite=0,
                 width_mm=0,
                 scale=1,):
        super().__init__()
        for texture in src_list:
            texture = _arcade.load_texture(texture)
            self.append_texture(texture)
        self.set_texture(start_sprite)

        px_mm_scale = scale
        self.scale = px_mm_scale * (width_mm / self.texture.width)  # required for draw
