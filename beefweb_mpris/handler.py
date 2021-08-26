from typing import Optional

from mpris_server.adapters import MprisAdapter
from mpris_server.events import EventAdapter
from mpris_server.server import Server
from pyfoobeef.models import PlayerState
from beefweb_mpris.beefweb import Beefweb


class BeefwebEventHandler(EventAdapter):
    def __init__(
            self,
            beefweb: Beefweb,
            server: Server,
            adapter: Optional[MprisAdapter] = None
    ):
        self.beefweb = beefweb
        self.server = server
        self.adapter = adapter
        super().__init__(self.server.player, self.server.root)

    def new_player_state(self, state: PlayerState):
        self.on_player_all()


def register_event_handler(
        beefweb: Beefweb,
        server: Server,
        adapter: MprisAdapter
):
    event_handler = BeefwebEventHandler(beefweb, server, adapter)
    beefweb.register_event_handler(event_handler)
