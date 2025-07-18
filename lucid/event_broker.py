"""
# Event Broker

* Description:

    An event broker using a pub/sub system for handling events within the
    pipelines.

    Consumers can subscribe to event publishes in the broker.
"""


import types
import sys
from collections import defaultdict
from typing import Callable

import lucid.const
import lucid.exceptions
import lucid.work


BROKER_CHAN = 'BROKER'
"""A channel for broker observability and maintenance."""
INVALID_CHAN = 'INVALID'
"""A channel for invalid events."""


BrokerUpdateEvent = lucid.work.WorkUnit(
    status=lucid.work.WorkStatus.REGISTERED,
    project='BROKER',
    user=lucid.const.USERNAME,
    role=lucid.work.Role.SYSTEM,
    domain=lucid.work.Domain.SYSTEM,
    task_name='BROKER_EVENT'
)


_topics: dict[str, list[Callable]] = defaultdict(list)
# Topics could evolve to a string channel name and a list of follow-up
# channels for the key. The message would run through the list and,
# after each callable, refer back to the _topics dict to see the list
# of further follow-up callables before being sent to the consumer.
# i.e. more complex logic based on future needs.
# ---------------------------------------------------------------------
# For now, it is a simple { string_name: channel_instance } dict.


class EventBroker(types.ModuleType):
    """Primary event coordinator."""
    # As the primary event system broker, the logic in this class wille evolve
    # over time. For now, ti si a very simplistic single channel topic.

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._broker_update = BrokerUpdateEvent
        self._setup_topics()

    def _setup_topics(self) -> None:
        """Setup default topics."""
        # This may be changed to more complex topic generation in the future,
        # per other comments.

        # -----Systems-----
        self.register_topic(BROKER_CHAN)
        self.register_topic(INVALID_CHAN)
        self.register_topic(lucid.work.Domain.SYSTEM.value)

        # -----Domains-----
        domains = lucid.work.Domain
        self.register_topic(lucid.work.Domain.ANIM.value)
        self.register_topic(lucid.work.Domain.COMP.value)
        self.register_topic(lucid.work.Domain.LAYOUT.value)
        self.register_topic(lucid.work.Domain.MODEL.value)
        self.register_topic(lucid.work.Domain.RIG.value)
        self.register_topic(lucid.work.Domain.SHADER.value)
        self.register_topic(lucid.work.Domain.TEXTURE.value)

        # -----Update-----
        self.trigger_event(self._broker_update)

    def register_topic(self, topic_name: str) -> None:
        if topic_name not in _topics:
            _topics[topic_name] = []
        self.trigger_event(self._broker_update)

    @staticmethod
    def trigger_event(unit: lucid.work.WorkUnit) -> None:
        if not unit.validate_tokens():
            err_msg = f'Required field of {unit.task_name} work unit is UNASSIGNED!'
            raise lucid.exceptions.WorkUnitError(err_msg)

        subscribers = _topics[unit.domain.value]
        for i in subscribers:
            i(unit)


# This is here to protect the _topics dict.
custom_modules = EventBroker(sys.modules[__name__].__name__)
sys.modules[__name__] = custom_modules


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Required for static type checkers to accept these names as members of this module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def register_topic(topic_name: str) -> None:
    """Adds a topic by the given name to the broker."""


def trigger_event(unit: lucid.work.WorkUnit) -> None:
    """Sends the WorkUnit to the extrapolated subscribers.

    The logic for routing the unit of work may expand over time, sending units
    on more complex topics based on information extracted from the unit fields.
    """
