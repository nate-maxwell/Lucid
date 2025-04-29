"""
# Message Router

* Description:

    A message router using a pub/sub system for handling events within the
    pipeline.

    Consumers can subscribe to message publishes in the router.
"""


import types
import sys
from typing import Optional

import lucid.const
from lucid.system.messaging.message import T_Message
from lucid.system.messaging.message import Event
from lucid.system.messaging.channel import Channel
from lucid.system.messaging.channel import StandardChannel
from lucid.system.messaging.channel import T_Channel


ROUTER_CHAN = 'ROUTER'
"""A channel for router observability and maintenance."""


class RouterUpdateEvent(Event):
    """Event that broadcasts when the router updates."""

    def __init__(self) -> None:
        super().__init__(ROUTER_CHAN)


_routes: dict[str, T_Channel] = {}
# Routes could evolve to a string channel name and a list of follow-up
# channels for the key. The message would run through the list and,
# after each channel, refer back to the _routes dict to see the list
# of further follow-up channels before being sent to the consumer.
# i.e. more complex logic based on future needs.
# ---------------------------------------------------------------------
# For now, it is a simple { string_name: channel_instance } dict.


class Router(types.ModuleType):
    """Primary message coordinator."""
    # As the primary message system router the logic in this class wille evolve
    # over time. For now, ti si a very simplistic single channel router.

    ROUTER_CHAN = ROUTER_CHAN
    RouterUpdateEvent = RouterUpdateEvent

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._router_update = RouterUpdateEvent()
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup default routes."""
        # This may be changed to more complex route generation in the future, per other comments.

        # -----Domains-----
        self._register_route(self.ROUTER_CHAN, StandardChannel(self.ROUTER_CHAN))
        self._register_route(lucid.const.MODEL_CHAN, StandardChannel(lucid.const.MODEL_CHAN))
        self._register_route(lucid.const.RIG_CHAN, StandardChannel(lucid.const.RIG_CHAN))
        self._register_route(lucid.const.ANIM_CHAN, StandardChannel(lucid.const.ANIM_CHAN))
        self._register_route(lucid.const.TEXTURE_CHAN, StandardChannel(lucid.const.TEXTURE_CHAN))
        self._register_route(lucid.const.RENDER_CHAN, StandardChannel(lucid.const.RENDER_CHAN))
        self._register_route(lucid.const.SCENE_CHAN, StandardChannel(lucid.const.SCENE_CHAN))
        self._register_route(lucid.const.COMP_CHAN, StandardChannel(lucid.const.COMP_CHAN))
        self._register_route(lucid.const.CAMERA_CHAN, StandardChannel(lucid.const.CAMERA_CHAN))
        self._register_route(lucid.const.MEDIA_CHAN, StandardChannel(lucid.const.MEDIA_CHAN))
        self._register_route(lucid.const.QA_CHAN, StandardChannel(lucid.const.QA_CHAN))

        # -----Systems-----
        self._register_route(lucid.const.INVALID_CHAN, StandardChannel(lucid.const.INVALID_CHAN))
        self._register_route(lucid.const.SUBSYSTEM_CHAN, StandardChannel(lucid.const.SUBSYSTEM_CHAN))

        self.route_message(self._router_update)

    def _register_route(self, route_name: str, channel: Optional[T_Channel]) -> None:
        """Registers the given channel by the given route name. If no channel
         type is provided, a StandardChannel() is created named after the
         route_name.

        Args:
            route_name (str): The name to register the channel as.
            channel (Optional[T_Channel]): The channel to register by the given name.
             If channel is None, a StandardChannel() is created and registered, named
             after the route.
        """
        if channel is None:
            channel = StandardChannel(route_name)
        _routes[route_name] = channel
        self.route_message(self._router_update)

    @staticmethod
    def get_channel(name: str) -> Channel:
        return _routes[name]

    @staticmethod
    def route_message(msg: T_Message) -> None:
        route = _routes[msg.header.route]
        route.process_message(msg)


# This is here to protect the _routes dict.
custom_modules = Router(sys.modules[__name__].__name__)
sys.modules[__name__] = custom_modules


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Required for static type checkers to accept these names as members of this module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def get_channel(name: str) -> Channel:
    """Returns the channel registered by the given name."""


def route_message(msg: T_Message) -> None:
    """Sends the message to the extrapolated destination.

    The logic for routing the message may expand over time, sending messages
    on more complex routes based on information extracted from the message
    header.
    """
