"""
# Context Subsystem Messages

* Description:

    Any message objects related to the context subsystem.
"""


from dataclasses import dataclass

from lucid import const
from lucid.system.messaging import message


@dataclass
class RoleChangeBody(message.MessageBody):
    role: str


class RoleChanged(message.Event):
    """Event for whenever the context role is changed."""

    def __init__(self, new_role: str) -> None:
        super().__init__(const.SUBSYSTEM_CHAN)
        self.body = RoleChangeBody(new_role)


class ContextChanged(message.Event):
    """Event for whenever a context value is changed."""

    def __init__(self) -> None:
        super().__init__(const.SUBSYSTEM_CHAN)
