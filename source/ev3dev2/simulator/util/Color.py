import arcade

BLUE = (58, 166, 221)
GREEN = (122, 182, 72)
YELLOW = (252, 227, 3)
RED = (201, 45, 57)


def to_color_code(color: arcade.Color) -> int:
    switcher = {
        BLUE: 2,
        GREEN: 3,
        YELLOW: 4,
        RED: 5
    }

    return switcher.get(color, 0)
