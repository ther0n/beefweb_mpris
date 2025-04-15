import asyncio
import threading
import os
import shutil
from typing import Dict

import yaml
from gi.repository import GLib
from subprocess import Popen
from mpris_server.server import Server

from beefweb_mpris.beefweb import Beefweb
from beefweb_mpris.adapter import BeefwebAdapter
from beefweb_mpris.handler import register_event_handler


def main():
    config_file = GLib.get_user_config_dir() + "/beefweb_mpris/config.yaml"
    if not os.path.isfile(config_file):
        if not os.path.isdir(os.path.dirname(config_file)):
            os.makedirs(os.path.dirname(config_file))
        config = {
            'host': 'localhost',
            'port': 8880,
            'foobar2000-command': 'foobar2000',
            'desktop-entry': 'foobar2000',
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
    adapter = BeefwebAdapter(beefweb, config['desktop-entry'])
    mpris = Server('beefweb', adapter=adapter)

    mpris_thread = threading.Thread(target=mpris.loop, daemon=True)
    mpris_thread.start()

    register_event_handler(beefweb, mpris, adapter)

    foobar2000.wait()
    
    cache_dir = GLib.get_user_cache_dir()
    if not os.path.exists(cache_dir+'/beefweb_mpris'):
        os.makedirs(cache_dir+'/beefweb_mpris')
    shutil.rmtree(cache_dir+'/beefweb_mpris')


if __name__ == '__main__':
    main()
