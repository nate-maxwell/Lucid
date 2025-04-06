"""
# Consumer Base Object

* Description:

    Channels, routers, and some transformers and endpoint implementations
    will 'consume' a message, removing it from teh system, performing some
    operation on the message data, and either executing an action based on
    the message data or forwarding a new message to another destination.
"""


from abc import ABC

from lucid.system.messaging import message


class Consumer(ABC):
    """Anything that consumes (takes in and does something with) a message.
    Contains standard process_message method to be overridden by derived
    consumers.
    """
    async def process_message(self, msg: message.T_Message) -> None:
        raise NotImplemented
