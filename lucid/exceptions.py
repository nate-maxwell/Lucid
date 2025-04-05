"""
# Lucid Pipeline Exceptions

* Description:

    All custom exception definitions.
"""


"""
Custom exceptions have integer value for easy front loading of information.
Exception topics are given an integer range of 100 for easy categorization.

0-99    - Subsystem/Message related exceptions
100-199 - Project related exceptions
200-299 - File IO related exceptions
300-399 - Headless operation related exceptions
400-499 - Camera + Rendering related exceptions
500-599 - Debug related exceptions
600-699 - Maya related exceptions
700-799 - Unreal related exceptions
"""


class LucidException(Exception):
    """Base Lucid exception. All other exceptions should derive form this class."""
    def __init__(self, error_num: int, *args) -> None:
        if len(args) == 0:
            super().__init__(f'[LUCID][{error_num}]')
        elif len(args) == 1:
            super().__init__(f'[LUCID][{error_num}] ' + str(args[0]))
        else:
            super().__init__(f'[LUCID][{error_num}] ', *args)


# ----------Subsystems-----------------------------------------------------------------------------

class ContextError(LucidException):
    """Raised on context-related errors, like trying to construct or set an
    invalid context as active.
    """
    def __init__(self, msg: str) -> None:
        super().__init__(10, msg)
