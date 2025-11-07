"""
# Event Broker

* Description:

    An event broker using a pub/sub system for handling events within the
    core.

    Consumers can subscribe to event publishes in the broker.
"""


import sys
import types
from collections import defaultdict
from typing import Callable

import lucid.core.exceptions
import lucid.core.work
from lucid.core import const
from lucid.core.details import DomainDetails


BROKER_CHAN = 'BROKER'
"""A channel for broker observability and maintenance."""
INVALID_CHAN = 'INVALID'
"""A channel for invalid events."""

BrokerUpdateEvent = lucid.core.work.WorkUnit(
    dcc=const.Dcc.SYSTEM,
    project='BROKER',
    user=const.USERNAME,
    role=lucid.core.const.Role.SYSTEM,
    domain_details=DomainDetails(),
    task_name='BROKER_EVENT'
)
"""An event for when the broker itself is affected, rather than event info
being forwarded to subscribers.
"""
BrokerUpdateEvent.domain_details.domain_name = const.Role.SYSTEM

END_POINT = Callable[[lucid.core.work.WorkUnit], None]
"""The end point that event info is forwarded to. These are the actions that
will execute when an event is triggered.
"""

_domain_task_type = dict[str, list[END_POINT]]
_DOMAIN_TASKS: _domain_task_type = defaultdict(list)
"""Each domain's topic dict - The { task_name: [subscriber_funcs] }"""
_TOPICS: dict[str, _domain_task_type] = {
    const.Role.SYSTEM.value: {
        'BROKER_EVENT': []
    }
}
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
# -----------------------------------------------------------------------------
# For now, it is a simple
# {
#   topic_name: {
#       task_name: [subscriber_funcs]
#   }
# }
# dict structure, with topics being the first key, and task names being
# the keys within a given topic. Task names hold lists of callable
# subscriber objects that the event is forwarded to.


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
        self.register_topic(const.Role.SYSTEM.value)

        # -----Domains-----
        self.register_topic(const.Role.ANIM.value)
        self.register_topic(const.Role.COMP.value)
        self.register_topic(const.Role.LAYOUT.value)
        self.register_topic(const.Role.MODEL.value)
        self.register_topic(const.Role.RIG.value)
        self.register_topic(const.Role.SHADER.value)
        self.register_topic(const.Role.TEXTURE.value)

        # -----Update-----
        self.emit(self._broker_update)

    def register_topic(self, topic_name: str) -> None:
        if topic_name not in _TOPICS:
            _TOPICS[topic_name] = {}
            self.emit(self._broker_update)

    def register_subscriber(self, topic_name: str, task_name: str, subscriber: END_POINT) -> None:
        self.register_topic(topic_name)
        domain_tasks: _DOMAIN_TASKS = _TOPICS[topic_name]

        # We do not value check here as domain_tasks is a default-dict[list].
        subscribers: list[END_POINT] = domain_tasks[task_name]
        subscribers.append(subscriber)
        self.emit(self._broker_update)

    @staticmethod
    def emit(unit: lucid.core.work.WorkUnit) -> None:
        if not unit.validate_tokens():
            err_msg = f'Required field of {unit.task_name} work unit is UNASSIGNED!'
            raise lucid.core.exceptions.WorkUnitException(err_msg)

        topic = unit.role.value
        if topic not in _TOPICS:
            raise lucid.core.exceptions.MissingTopicException(topic)

        domain_tasks = _TOPICS[unit.role.value]
        # We do not value check here as domain_tasks is a default-dict[list].
        subscribers: list[END_POINT] = domain_tasks[unit.task_name]
        for i in subscribers:
            i(unit)


# This is here to protect the _TOPICS dict.
custom_modules = EventBroker(sys.modules[__name__].__name__)
sys.modules[__name__] = custom_modules

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Required for static type checkers to accept these names as members of
# this module.
# -----------------------------------------------------------------------------


def register_topic(topic_name: str) -> None:
    """Adds a topic by the given name to the broker."""


def register_subscriber(topic_name: str, task_name: str, subscriber: END_POINT) -> None:
    """Registers an end point, or subscriber, to the task name of the given topic.
    All triggered event's info will be forwarded to each subscriber.
    Subscribers are callables that take and execute on work unit data.
    """


def emit(unit: lucid.core.work.WorkUnit) -> None:
    """Sends the WorkUnit to the extrapolated subscribers.

    The logic for routing the unit of work may expand over time, sending units
    on more complex topics based on information extracted from the unit fields.
    """
