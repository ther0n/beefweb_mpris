from mimetypes import guess_type
from typing import Optional
from typing import Final
from mpris_server import MetadataObj, ValidMetadata
from mpris_server.adapters import MprisAdapter
from mpris_server.base import Microseconds, PlayState, DbusObj, Rate, Volume, Track, \
    DEFAULT_TRACK_ID
from mpris_server.mpris.compat import get_track_id
from gi.repository import GLib

from beefweb_mpris.beefweb import Beefweb

RATE: Final[Rate] = Rate(1.0)

class BeefwebAdapter(MprisAdapter):
    def __init__(self, wrapper: Beefweb):
        self.beefweb = wrapper
        super().__init__()

    def metadata(self) -> ValidMetadata:
        try:
            active_item = self.beefweb.active_item
            columns = active_item.columns
            self.beefweb.download_art()
            return MetadataObj(
                track_id=get_track_id(active_item.columns.title),
                length=int(self.beefweb.active_item.duration * 1000000),
                art_url=f'file://{GLib.get_user_cache_dir()}/beefweb_mpris/{columns.album}',
                title=columns.title,
                artists=[columns.artists],
                album=columns.album,
                album_artists=[columns.album_artist],
                disc_number=int(columns.disc_no) if columns.disc_no.isdigit() else 1,
                track_number=int(columns.track_no) if columns.track_no.isdigit() else 1
            )
        except AttributeError as e:
            return MetadataObj(
                track_id=DEFAULT_TRACK_ID
            )

    def get_current_position(self) -> Microseconds:
        try:
            seconds = self.beefweb.state.estimated_position()
            microseconds = int(seconds * 1000000)
            return microseconds
        except AttributeError:
            return 0

    def next(self):
        self.beefweb.client.play_next()

    def previous(self):
        self.beefweb.client.play_previous()

    def pause(self):
        self.beefweb.client.pause()

    def resume(self):
        self.beefweb.client.pause_toggle()

    def stop(self):
        self.beefweb.client.stop()

    def play(self):
        self.beefweb.client.play()

    def get_playstate(self) -> PlayState:
        try:
            playback_state = self.beefweb.state.playback_state
            if playback_state == "playing":
                return PlayState.PLAYING
            elif playback_state == "paused":
                return PlayState.PAUSED
            return PlayState.STOPPED
        except AttributeError:
            return PlayState.STOPPED

    def seek(
            self,
            time: Microseconds,
            track_id: Optional[DbusObj] = None
    ):
        seconds = time / 1000000
        self.beefweb.client.set_player_state(position=seconds)

    def open_uri(self, uri: str):
        mimetype, _ = guess_type(uri)
        self.beefweb.client.play()

    def is_repeating(self) -> bool:
        try:
            if self.beefweb.state.playback_mode.number == 2:
                return True
            else:
                return False
        except AttributeError:
            return False

    def is_playlist(self) -> bool:
        return True

    def set_repeating(self, value: bool):
        if self.beefweb.state.playback_mode.number == 2:
            self.beefweb.client.set_player_state(playback_mode=0)
        else:
            self.beefweb.client.set_player_state(playback_mode=2)

    def set_loop_status(self, value: str):
        if value == "None":
            self.beefweb.client.set_player_state(playback_mode=0)
        elif value == "Track":
            self.beefweb.client.set_player_state(playback_mode=2)
        elif value == "Playlist":
            self.beefweb.client.set_player_state(playback_mode=1)

    def get_rate(self) -> Rate:
        return RATE

    # def set_rate(self, value: Rate):
    #     pass

    # def set_minimum_rate(self, value: Rate):
    #     pass

    # def set_maximum_rate(self, value: Rate):
    #     pass

    def get_minimum_rate(self) -> Rate:
        return RATE

    def get_maximum_rate(self) -> Rate:
        return RATE

    def get_shuffle(self) -> bool:
        try:
            if self.beefweb.state.playback_mode.number == 4:
                return True
            else:
                return False
        except AttributeError:
            return False

    def set_shuffle(self, value: bool):
        if self.beefweb.state.playback_mode.number == 4:
            self.beefweb.client.set_player_state(playback_mode=0)
        else:
            self.beefweb.client.set_player_state(playback_mode=4)

    def get_art_url(self, track: DbusObj | Track | None) -> str:
        self.beefweb.download_art()
        return f'file://{GLib.get_user_cache_dir()}/beefweb_mpris/{self.beefweb.active_item.columns.album}'

    def get_volume(self) -> Volume:
        try:
            print("returning volume: ", self.beefweb.state.volume.value)
            return self.beefweb.state.volume.value + 100.0
        except AttributeError:
            return Volume(100)

    def set_volume(self, value: Volume):
        # I don't know what im doing but it works kinda
        new_vol = 0 - (100 ** (1 - value))
        print(new_vol)
        return self.beefweb.client.set_player_state(volume=float(new_vol))

    def is_mute(self) -> bool:
        try:
            return self.beefweb.state.volume.is_muted
        except AttributeError:
            return False

    def set_mute(self, value: bool):
        return self.beefweb.client.set_player_state(mute=False)

    def can_go_next(self) -> bool:
        return True

    def can_go_previous(self) -> bool:
        return True

    def can_play(self) -> bool:
        return True

    def can_pause(self) -> bool:
        return True

    def can_seek(self) -> bool:
        return True

    def can_control(self) -> bool:
        return True

    def get_stream_title(self) -> str:
        return self.metadata().title

    # def get_previous_track(self) -> Track:
    #     pass

    # def get_next_track(self) -> Track:
    #     pass
