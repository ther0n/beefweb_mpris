import asyncio
import threading
import os
import requests
import pyfoobeef

from gi.repository import GLib
from pyfoobeef.models import PlayerState, ActiveItem, Columns


class Beefweb:
    def __init__(self, server: str, port: int, username: str, password: str):
        self.server = server
        self.port = port
        self.event_listener = pyfoobeef.EventListener(
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
        return self.event_listener.player_state

    @property
    def active_item(self) -> ActiveItem:
        return self.state.active_item

    @property
    def columns(self) -> Columns:
        return self.active_item.columns

    def download_art(self):
        try:
            r = requests.get(f'http://{self.server}:{self.port}/api'
                f'/artwork/{self.active_item.playlist_id}/{self.active_item.index}')
            cover_path = f'{GLib.get_user_cache_dir()}/beefweb_mpris/{self.active_item.columns.album}'
            if not os.path.isfile(cover_path):
                if not os.path.isdir(os.path.dirname(cover_path)):
                    os.makedirs(os.path.dirname(cover_path))
            with open(cover_path, 'wb') as f:
                f.write(r.content)
        finally:
            return

    def listener(self, loop, event_listener):
        self.event_listener.add_callback("player_state", event_listener.new_player_state)
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.listener_loop())

    async def listener_loop(self):
        await self.event_listener.connect(1)
        while True:
            await asyncio.sleep(10)

    def register_event_handler(self, event_handler):
        loop = asyncio.new_event_loop()
        threading.Thread(target=self.listener, args=(loop, event_handler), daemon=True).start()
