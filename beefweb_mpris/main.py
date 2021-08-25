import asyncio
import threading
import os
import yaml
from gi.repository import GLib
from subprocess import Popen
from mpris_server.server import Server

from beefweb_mpris.beefweb import Beefweb
from beefweb_mpris.adapter import BeefwebAdapter, BeefwebEventHandler


async def start(event_handler, beefweb):
    await beefweb.register_event_handler(event_handler)


def start_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


def main():
    config_file = GLib.get_user_config_dir() + "/beefweb_mpris/config.yaml"
    if not os.path.isfile(config_file):
        if not os.path.isdir(os.path.dirname(config_file)):
            os.makedirs(os.path.dirname(config_file))
        config = {
            'host': 'localhost',
            'port': 8880,
            'foobar2000-command': 'foobar2000',
            'timeout': 30.0,
            'username': 'user',
            'password': 'password'
        }
        with open(config_file, 'w') as cf:
            yaml.dump(config, cf)

    with open(config_file, 'r') as cf:
        try:
            config = yaml.safe_load(cf)
        except yaml.YAMLError as e:
            print(e)

    foobar2000 = Popen([config['foobar2000-command']])

    beefweb = Beefweb(config['host'], config['port'], config['username'], config['password'])
    adapter = BeefwebAdapter(beefweb)
    mpris = Server('beefweb', adapter=adapter)
    event_handler = BeefwebEventHandler(root=mpris.root, player=mpris.player)

    event_loop = asyncio.new_event_loop()
    event_thread = threading.Thread(target=start_event_loop, args=(event_loop,), daemon=True)
    event_thread.start()
    event_task = asyncio.run_coroutine_threadsafe(start(event_handler, beefweb), event_loop)

    mpris_thread = threading.Thread(target=mpris.loop, daemon=True)
    mpris_thread.start()

    foobar2000.wait()


if __name__ == '__main__':
    main()
