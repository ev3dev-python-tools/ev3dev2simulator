import arcade

class RobotPartSprite(arcade.Sprite):
    """
    We need a Sprite and a Pymunk physics object. This class blends them
    together.
    """

    def __init__(self,
                 src_list,
                 start_sprite=0,
                 width_mm=0,
                 height_mm=0,
                 scale=1,):
        super().__init__()
        for texture in src_list:
            texture = arcade.load_texture(texture)
            self.append_texture(texture)
        self.set_texture(start_sprite)

        px_mm_scale = scale
        self.scale = px_mm_scale * (width_mm / self.texture.width)  # required for draw
