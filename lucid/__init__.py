"""
Lucid Unreal Games Pipeline.
"""


__version__ = '1.0.0'


class LucidException(Exception):
    """Base Lucid exception. All other exception should be derived from this class."""
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__()
        elif len(args) == 1:
            super().__init__('[Lucid] ' + str(args[0]))
        else:
            super().__init__('[Lucid]', *args)
