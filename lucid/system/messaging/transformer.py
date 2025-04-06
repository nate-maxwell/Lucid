"""
# Message Transformer

* Description:

    Transformers are the primary message formatters and manipulators.
"""


from lucid.system.messaging import message
from lucid.system.messaging.consumer import Consumer


class Transformer(Consumer):
    """Transformers take in a message and output a modified version of the
    message.

    Contains transform(msg: message.Message) method to override.
    """

    def __init__(self) -> None:
        self.message: message.Message

    def transform(self, msg: message.T_Message) -> message.Message:
        raise NotImplemented

    async def process_message(self, msg: message.T_Message) -> message.Message:
        """Runs the given message through self.transform().
        Do not override this func, override self.transform().
        """
        return self.transform(msg)
