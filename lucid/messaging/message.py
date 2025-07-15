"""
# Message Types

* Description:

    Messages are the packets of information sent through the system.

    Messages typically consist of two parts:
        - Header: Informs the system of the message's intent, destination,
                  origin, etc.
        - Body:   The data the receiving party is interested in.

    Messages may be transformed before reaching their destination, but can be
    cataloged at each step of the process for later playback.

    There are three types of messages:
        - Events:    Past tense data informing the receiver that something has
                     changed in the sender.
        - Commands:  Verb tense data invoking functionality in the receiver, who
                     typically tell the consumer to respond with a document.
        - Documents: A set of data to inform the receiver.
"""


import enum
import inspect
import time
import uuid
import json
from collections import deque
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar


@enum.unique
class MessageStatus(enum.Enum):
    # These may expand as messages are integrated into the larger pipeline.
    # There may need to be status for channel received vs consumer received.
    RESOLVED = 'RESOLVED'
    RECEIVED = 'RECEIVED'
    REJECTED = 'REJECTED'   # Channel or system will not take
    INVALID = 'INVALID'     # Channel or system was not expecting message or message type
    PENDING = 'PENDING'
    CREATED = 'CREATED'
    ERROR = 'ERROR'         # Something went wrong in processing the message

    # Failed messages are often sent to a dead letter channel, which we may or may not want.
    FAILED = 'FAILED'       # Message could not be delivered


class MessageComponent(object):
    """A message component is any part of a message object.
    These are typically the message header and message body.

    Each part has some custom magic methods and get(key, default) method.
    """

    def __str__(self) -> str:
        attr_str = '\n'.join(f'\t{k}: {v}' for k, v in self.__dict__.items())
        return f'Message Header:(\n{attr_str}\n)'

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def get(self, key: str, default: Any = None) -> Any:
        """Like dict.get(key, default)"""
        try:
            return self.__dict__[key]
        except KeyError:
            return default


@dataclass
class MessageHeader(MessageComponent):
    """Metadata associated with a message.
    Used for route processing through the message system.
    """
    route: str
    message_type: str
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    status: MessageStatus = MessageStatus(MessageStatus.CREATED)

    # Command messages may kick off additional commands.
    correlation_id: Optional[str] = None  # The id of the message this one responds to.
    return_channel: Optional[str] = None  # The channel the correlated message will listen on.

    def update_status(self, new_status: MessageStatus) -> None:
        """Update the message's current status."""
        self.status = new_status


class MessageBody(MessageComponent):
    """A message body holds the values the subscriber is actually after, and is
    unique to each message definition.
    """


class Message(object):
    """A message is the item that is run through channels and transformers
    in the message bus. They come in a variety of forms and represent
    different 'tenses' or timestamps relative to code invocation.
    """

    def __init__(self, route: str) -> None:
        self.header = MessageHeader(route, self.__class__.__name__.lower())
        self.body: MessageBody = MessageBody()

    def __str__(self) -> str:
        data = {
            'Header:': {k: str(v) for k, v in self.header.__dict__.items()},
            'Body:': {k: str(v) for k, v in self.body.__dict__.items()}
        }

        return json.dumps(data, indent=4)

    @property
    def instance_site(self) -> str:
        """Returns the name of the file where the object was instantiated."""
        stack = inspect.stack()
        call_frame = stack[1]
        call_file = call_frame.filename
        return Path(call_file).stem


class Event(Message):
    """Past tense data informing the receiver that something has
    changed in the sender.
    """

    def __init__(self, route: str) -> None:
        super().__init__(route)


class Command(Message):
    """Verb tense data invoking functionality in the receiver, who typically
    tell the consumer to respond with a document message.
    """

    def __init__(self, route: str) -> None:
        super().__init__(route)


class Document(Message):
    """A set of data to inform the subscriber."""

    def __init__(self, route: str) -> None:
        super().__init__(route)


T_Message = TypeVar('T_Message', bound=Message)

handler_ = Callable[[Message], Optional[Document]]
"""Anything that handles a message. May return a document message."""

transformer_ = Callable[[Message], Message]
"""Anything that updates, filters, or changes a message and returns
the updated message.
"""


class MessagePropertyFilter(object):
    """Filters messages based on specified header properties."""

    def __init__(self, filter_conditions: Optional[dict[str, Any]] = None) -> None:
        """Initialize the filter with conditions.

        Args:
            filter_conditions (Optional[dict[str, Any]]): A dictionary of header
                properties to match.
        """
        self.filter_conditions = filter_conditions or {}

    def clear_conditions(self) -> None:
        """Clears all current filter conditions."""
        self.filter_conditions = {}

    def add_condition(self, con: dict[str, Any]) -> None:
        """Adds the key value requirement to the registered filter conditions."""
        self.filter_conditions.update(con)

    def _apply(self, msg: T_Message) -> bool:
        """Check if a message matches all current filter conditions.

        Args:
            msg (T_Message): The message to evaluate.
        Returns:
            bool: True if the message matches, False otherwise.
        """
        return all(
            msg.header.get(k) == v for k, v in self.filter_conditions.items()
        )

    def filter_messages(self, messages: list[T_Message]) -> list[T_Message]:
        """Filters a list of messages and returns only those that match the conditions.

        Args:
            messages (list[T_Message]): List of messages to filter.
        Returns:
            list[T_Message]: Filtered messages that match conditions.
        """
        return [msg for msg in messages if self._apply(msg)]


class MessageQueue(object):
    """A queue object for handling groups of messages in FIFO order.
    Contains a format_queue() method that should be overridden by consumer to
    reorganize the queue based on consumer requirements.
    """

    def __init__(self) -> None:
        # Private deque attr instead of inheriting from deque so that
        # implementors of consumers do not call deque methods directly.
        # Easier to define preferred deque interfaces this way.
        self._items: deque = deque([])
        self.message_property_filter = MessagePropertyFilter()

    def __bool__(self) -> bool:
        return bool(self._items)

    def append(self, msg: Message) -> None:
        """Adds the given message to the end of the queue."""
        self._items.append(msg)

    def get_next(self) -> Optional[Message]:
        """Gets the next message in the queue if one exists else None.
        Messages gotten in FIFO ( First-in-first-out ) order.
        """
        if self._items:
            return self._items.popleft()
        return None
