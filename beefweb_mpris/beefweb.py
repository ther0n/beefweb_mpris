import pyfoobeef

from pyfoobeef.models import PlayerState, ActiveItem, Columns


class Beefweb:
    def __init__(self, server: str, port: int, username: str, password: str):
        self.server = server
        self.port = port
        self.listener = pyfoobeef.EventListener(
            base_url=server,
            port=port,
            active_item_column_map={
                "%title%": "title",
                "%length%": "length",
                "%artist%": "artists",
                "%album artist%": "album_artist",
                "%album%": "album",
                "%discnumber%": "disc_no",
                "%track number%": "track_no"
            },
            username=username,
            password=password
        )
        self.client = pyfoobeef.Client(
            base_url=server,
            port=port,
            username=username,
            password=password
        )

    @property
    def state(self) -> PlayerState:
        return self.listener.player_state

    @property
    def active_item(self) -> ActiveItem:
        return self.state.active_item

    @property
    def columns(self) -> Columns:
        return self.active_item.columns

    async def register_event_handler(self, event_handler):
        self.listener.add_callback("player_state", event_handler.on_event)
        await self.listener.connect(reconnect_time=1)

