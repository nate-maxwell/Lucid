"""
# Event Broker

* Description:

    An event broker using a pub/sub system for handling events within the
    pipelines.

    Consumers can subscribe to event publishes in the router.
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


_routes: dict[str, list[Callable]] = defaultdict(list)
# Routes could evolve to a string channel name and a list of follow-up
# channels for the key. The message would run through the list and,
# after each callable, refer back to the _routes dict to see the list
# of further follow-up callables before being sent to the consumer.
# i.e. more complex logic based on future needs.
# ---------------------------------------------------------------------
# For now, it is a simple { string_name: channel_instance } dict.


class EventBroker(types.ModuleType):
    """Primary event coordinator."""
    # As the primary event system broker, the logic in this class wille evolve
    # over time. For now, ti si a very simplistic single channel router.

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._broker_update = BrokerUpdateEvent
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup default routes."""
        # This may be changed to more complex route generation in the future,
        # per other comments.

        # -----Systems-----
        self.register_route(BROKER_CHAN)
        self.register_route(INVALID_CHAN)
        self.register_route(lucid.work.Domain.SYSTEM.value)

        # -----Domains-----
        domains = lucid.work.Domain
        self.register_route(lucid.work.Domain.ANIM.value)
        self.register_route(lucid.work.Domain.COMP.value)
        self.register_route(lucid.work.Domain.LAYOUT.value)
        self.register_route(lucid.work.Domain.MODEL.value)
        self.register_route(lucid.work.Domain.RIG.value)
        self.register_route(lucid.work.Domain.SHADER.value)
        self.register_route(lucid.work.Domain.TEXTURE.value)

        # -----Update-----
        self.route_event(self._broker_update)

    def register_route(self, route_name: str) -> None:
        if route_name not in _routes:
            _routes[route_name] = []
        self.route_event(self._broker_update)

    @staticmethod
    def route_event(wu: lucid.work.WorkUnit) -> None:
        if not wu.validate_tokens():
            err_msg = f'Required field of {wu.task_name} work unit is UNASSIGNED!'
            raise lucid.exceptions.WorkUnitError(err_msg)

        subscribers = _routes[wu.domain.value]
        for i in subscribers:
            i(wu)


# This is here to protect the _routes dict.
custom_modules = EventBroker(sys.modules[__name__].__name__)
sys.modules[__name__] = custom_modules


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Required for static type checkers to accept these names as members of this module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def register_route(route_name: str) -> None:
    """Adds a route by the given name to the broker."""


def route_event(work_unit: lucid.work.WorkUnit) -> None:
    """Sends the WorkUnit to the extrapolated subscribers.

    The logic for routing the unit fo work may expand over time, sending units
    on more complex routes based on information extracted from the unit fields.
    """
