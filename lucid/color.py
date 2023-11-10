"""
# RGB Color

* Description

    A convenience class for handling RGB colors.

* Update History

    `2023-10-12` - Init
"""


class ColorRGB(object):
    """
    Class for handling color in rgb format.

    To use pre-defined color call the class.color function, e.g.
    red = ColorRGB.red()
    print(red.r, red.g, red.b)

    To define a custom color, put the 0-255 rgb code as the arguments.
    my_color = ColorRGB(17, 128, 177)

    Args:
        r (int): Red value
        g (int): Green value
        b (int): Blue value
    """
    def __init__(self, r: int, g: int, b: int):
        try:
            red = int(r)
            green = int(g)
            blue = int(b)

            value_range = range(0, 256)

            for c in [red, green, blue]:
                if c not in value_range:
                    raise ValueError

        except ValueError:
            raise ValueError('Values must be integers between 0 and 255 for rgb code.')

        self._r = red
        self._g = green
        self._b = blue

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @property
    def r_normalized(self):
        return self._r/255.0

    @property
    def g_normalized(self):
        return self._g/255.0

    @property
    def b_normalized(self):
        return self._b/255.0

    @classmethod
    def red(cls):
        return cls(255, 0, 0)

    @classmethod
    def green(cls):
        return cls(0, 255, 0)

    @classmethod
    def blue(cls):
        return cls(0, 0, 255)

    @classmethod
    def cyan(cls):
        return cls(0, 255, 255)

    @classmethod
    def yellow(cls):
        return cls(255, 255, 0)

    @classmethod
    def magenta(cls):
        return cls(255, 0, 255)

    @classmethod
    def orange(cls):
        return cls(255, 128, 0)

    @classmethod
    def purple(cls):
        return cls(128, 0, 128)

    @classmethod
    def white(cls):
        return cls(255, 255, 255)

    @classmethod
    def black(cls):
        return cls(0, 0, 0)

    @classmethod
    def gray(cls):
        return cls(128, 128, 128)

    @classmethod
    def silver(cls):
        return cls(192, 192, 192)
