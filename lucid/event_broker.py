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
import lucid.details


BROKER_CHAN = 'BROKER'
"""A channel for broker observability and maintenance."""
INVALID_CHAN = 'INVALID'
"""A channel for invalid events."""

BrokerUpdateEvent = lucid.work.WorkUnit(
    status=lucid.work.WorkStatus.REGISTERED,
    project='BROKER',
    user=lucid.const.USERNAME,
    role=lucid.work.Role.SYSTEM,
    domain=lucid.details.Domain.SYSTEM,
    task_name='BROKER_EVENT'
)
"""An event for when the broker itself is affected, rather than event info
being forwarded to subscribers.
"""

END_POINT = Callable[[lucid.work.WorkUnit], None]
"""The end point that event info is forwarded to. These are the actions that
will execute when an event is triggered.
"""

_DOMAIN_TASKS: dict[str, list[END_POINT]] = defaultdict(list)
"""Each domain's topic dict - The { task_name: [subscriber_funcs] }"""
_TOPICS: dict[str, _DOMAIN_TASKS] = {}
"""The broker's record of each topic name to domain task:subscriber records.

This is labeled as 'topics' to create some separation between the pipeline
domains, in the event the broker is used by non-domain centric systems.

This is kept outside of the replaced module class to create a protected
closure around the event subscriber structure.
"""
# Topics could evolve to a string channel name and a list of follow-up
# channels for the key. The message would run through the list and,
# after each callable, refer back to the _topics dict to see the list
# of further follow-up callables before being sent to the consumer.
# i.e. more complex logic based on future needs.
# ---------------------------------------------------------------------
# For now, it is a simple
# {
#   topic_name: {
#       task_name: [subscriber_funcs]
#   }
# }
#   dict structure, with topics being the first key, and task names being
#   the keys within a given topic.


class EventBroker(types.ModuleType):
    """Primary event coordinator."""
    # As the primary event system broker, the logic in this class wille evolve
    # over time. For now, it is a very simplistic single channel topic.

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
        self.register_topic(lucid.details.Domain.SYSTEM.value)

        # -----Domains-----
        self.register_topic(lucid.details.Domain.ANIM.value)
        self.register_topic(lucid.details.Domain.COMP.value)
        self.register_topic(lucid.details.Domain.LAYOUT.value)
        self.register_topic(lucid.details.Domain.MODEL.value)
        self.register_topic(lucid.details.Domain.RIG.value)
        self.register_topic(lucid.details.Domain.SHADER.value)
        self.register_topic(lucid.details.Domain.TEXTURE.value)

        # -----Update-----
        self.trigger_event(self._broker_update)

    def register_topic(self, topic_name: str) -> None:
        if topic_name not in _TOPICS:
            _TOPICS[topic_name] = {}
            self.trigger_event(self._broker_update)

    def register_subscriber(self, topic_name: str, task_name: str, subscriber: END_POINT) -> None:
        self.register_topic(topic_name)
        domain_tasks: _DOMAIN_TASKS = _TOPICS[topic_name]

        # We do not value check here because domain_tasks is a default-dict[list].
        subscribers: list[END_POINT] = domain_tasks[task_name]
        subscribers.append(subscriber)
        self.trigger_event(self._broker_update)

    @staticmethod
    def trigger_event(unit: lucid.work.WorkUnit) -> None:
        if not unit.validate_tokens():
            err_msg = f'Required field of {unit.task_name} work unit is UNASSIGNED!'
            raise lucid.exceptions.WorkUnitError(err_msg)

        domain_tasks: _DOMAIN_TASKS = _TOPICS[unit.domain.value]
        if unit.task_name in domain_tasks:
            subscribers: list[END_POINT] = domain_tasks[unit.task_name]
            for i in subscribers:
                i(unit)
        else:
            raise lucid.exceptions.MissingTaskNameError(
                unit.domain.value,
                unit.task_name
            )


# This is here to protect the _TOPICS dict.
custom_modules = EventBroker(sys.modules[__name__].__name__)
sys.modules[__name__] = custom_modules


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Required for static type checkers to accept these names as members of this module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def register_topic(topic_name: str) -> None:
    """Adds a topic by the given name to the broker."""


def register_subscriber(topic_name: str, task_name: str, subscriber: END_POINT) -> None:
    """Registers an end point, or subscriber, to the task name of the given topic.
    All triggered event's info will be forwarded to each subscriber.
    Subscribers are callables that take and execute on work unit data.
    """


def trigger_event(unit: lucid.work.WorkUnit) -> None:
    """Sends the WorkUnit to the extrapolated subscribers.

    The logic for routing the unit of work may expand over time, sending units
    on more complex topics based on information extracted from the unit fields.
    """
