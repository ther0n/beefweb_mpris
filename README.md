# beefweb-mpris

Adds MPRIS support to foobar2000 running in WINE on Linux by using the beefweb REST API.

## Installation

Note: This is currently only tested on Arch linux but should work on other distros

1. Install foobar2000: `yay -S foobar2000`
2. Install beefweb in foobar2000
3. Install `beefweb_mpris`: `pip install --user git+https://github.com/ther0n/beefweb_mpris.git`
4. Run `beefweb_mpris` on the command line
5. Edit `$CONFIG/beefweb_mpris/config.yaml` to match your settings for beefweb in foobar2000
  - `foobar2000-command` should be set to a [command/script to run foobar2000](https://aur.archlinux.org/cgit/aur.git/tree/foobar2000.sh?h=foobar2000)
6. Create/edit a `.desktop` file to launch beefweb_mpris
