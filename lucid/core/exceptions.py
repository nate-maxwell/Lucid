"""
# Lucid Pipeline Exceptions

* Description:

    All custom exception definitions.
"""


"""
Custom exceptions have integer value for easy front loading of information.
Exception topics are given an integer range of 100 for easy categorization.

0-99    - WorkUnit/Event related exceptions
100-199 - Project related exceptions
200-299 - File IO related exceptions
300-399 - Debug related exceptions
400-499 - DCC related exceptions
"""


class LucidException(Exception):
    """Base Lucid exception. All other exceptions should derive form
    this class.
    """
    def __init__(self, error_num: int, *args) -> None:
        if len(args) == 0:
            super().__init__(f'[LUCID][{error_num}]')
        elif len(args) == 1:
            super().__init__(f'[LUCID][{error_num}] ' + str(args[0]))
        else:
            super().__init__(f'[LUCID][{error_num}] ', *args)


# ----------WorkUnit / Event---------------------------------------------------

class WorkUnitException(LucidException):
    """Raised on general work unit errors, like an unassigned field."""
    def __init__(self, msg: str) -> None:
        super().__init__(10, msg)


class WorkUnitTokenException(LucidException):
    """Raised on work unit token errors, like an incorrectly or
    unassigned field.
    """
    def __init__(self) -> None:
        err_msg = 'Work unit has incorrect or UNASSIGNED tokens!'
        super().__init__(11, err_msg)


class DomainDetailsException(LucidException):
    """Raised on general work domain details related errors."""
    def __init__(self, msg: str) -> None:
        super().__init__(20, msg)


class DomainDetailsTokenException(LucidException):
    """Raised on domain details token errors, like an incorrectly or
    unassigned field.
    """
    def __init__(self) -> None:
        err_msg = 'Domain details has incorrect or UNASSIGNED tokens!'
        super().__init__(21, err_msg)


class MissingTopicException(LucidException):
    """Raised when the event broker receives a work unit is attempted to be
    passed to a topic that does not exist.
    """
    def __init__(self, topic: str) -> None:
        err_msg = f'Topic: {topic} is missing from event broker!'
        super().__init__(30, err_msg)


class MissingTaskNameException(LucidException):
    """Raised when the event broker receives a work unit whose task name does
    not exist in the corresponding domain topic.
    """
    def __init__(self, topic: str, task_name: str) -> None:
        err_msg = f'Task name: {task_name} not registered in topic: {topic}!'
        super().__init__(40, err_msg)


# ----------Project------------------------------------------------------------

class InvalidProjectException(LucidException):
    """Raised when the environment var for the project is unset."""
    def __init__(self) -> None:
        super().__init__(100, 'Project environment var is UNASSIGNED!')


class MissingConfigsException(LucidException):
    """Raised when the config directory or directory contents are missing for
    a project.
    """
    def __init__(self) -> None:
        super().__init__(110, 'Project config data missing!')


# ----------DCC----------------------------------------------------------------

class ProgramPathNotFoundException(LucidException):
    """Raised when the exe path for a dcc or pipeline program cannot be found."""
    def __init__(self, program: str) -> None:
        super().__init__(400, f'Program: {program} path not found!')
