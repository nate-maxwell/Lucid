"""
# Message Channels

* Description:

    Channels are the 'highway' that messages travel through to their
    destination. There are many channel patterns: point-to-point,
    datatype, pub-sub, dead letter, invalid message, bridges,
    message bus, event broker, etc.

    Typically, a static number of channels are decided upon during
    development instead of dynamically at run-time. The number of
    type of channels must be determined by invested parties ahead
    of time. Channels are typically domain driven.
"""


import inspect
from collections import defaultdict
from typing import Callable
from typing import Type
from typing import TypeVar
from typing import Union

from lucid.system.messaging import message
from lucid.system.messaging.consumer import Consumer
from lucid.system.messaging.transformer import Transformer


transformer_func = Callable[[message.T_Message], message.T_Message]
transformer_type = Union[Transformer, transformer_func]


class Channel(Consumer):
    """Channels ar ethe primary highway for a message to travel through,
    passing through any number of transformers (or translators) along the way.
    Messages can be sent from one channel to another, to a router, or to a
    consumer/subscriber.

    Each channel can have a differing method of processing messages:
    round-robin, recipient list, by data type, etc.
    The channel determines the destination t put in the processed message's
    header before sending it back to the router.
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self._transformers: list[Transformer] = []

    def _transform_message(self, msg: message.T_Message) -> message.Message:
        """Runs the given message through all registered transformers."""
        result = msg
        for t in self._transformers:
            result = t.process_message(result)
        return result

    def register_transformer(self, transformer: transformer_type) -> None:
        """Add a transformer to the channel.
        Converts callables to base transformer class. If another is needed,
        this method.
        """
        if isinstance(transformer, Transformer):
            self._transformers.append(transformer)
        elif callable(transformer):
            # Convert func to Transformer class.
            t = Transformer()
            t.transform = transformer
            self._transformers.append(t)
        else:
            raise ValueError('Transformer must be Transformer subclass or callable.')

    def register_subscriber(self, *args, **kwargs) -> None:
        """Register the given message handler to be forwarded any
        processed messages.
        """
        raise NotImplemented


T_Channel = TypeVar('T_Channel', bound=Channel)


class StandardChannel(Channel):
    def __init__(self, name: str, transformers: list[Transformer] = None) -> None:
        super().__init__(name, transformers)
        self.subscribers: dict[Type[message.T_Message]: list[message.handler_]] = defaultdict(list)

    def register_subscriber(self, msg_type: Type[message.T_Message], handler: message.handler_) -> None:
        self.subscribers[msg_type].append(handler)

    def process_message(self, msg: message.T_Message) -> None:
        """Run the given message through all registered transformers, and then
        run the transformed message through all subscribers.
        """
        msg.header.update_status(message.MessageStatus.PENDING)
        transformed_msg = self._transform_message(msg)
        for handler in self.subscribers[msg.header.message_type]:
            handler(transformed_msg)

        transformed_msg.header.update_status(message.MessageStatus.RESOLVED)
