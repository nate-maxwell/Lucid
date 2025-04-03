"""
# Message Transformer

* Description:

    Transformers are the primary message formatters and manipulators.
"""


from lucid.system import message
from lucid.system.consumer import Consumer


class Transformer(Consumer):
    """Transformers take in a message and output a modified version of the
    message.

    Contains transform(msg: message.Message) method to override.
    """

    def __init__(self) -> None:
        self.message: message.Message

    def transform(self, msg: message.T_Message) -> message.Message:
        raise NotImplemented

    def process_message(self, msg: message.T_Message) -> message.Message:
        return self.transform(msg)
