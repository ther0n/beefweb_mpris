# beefweb-mpris

Adds MPRIS support to foobar2000 running in WINE on Linux by using the beefweb REST API.

## Installation

Note: These are only tested on Fedora 40, but can be adapted to other distros

1. Install WINE (`sudo dnf install wine`)
2. Download the Foobar2000 installer and install in wine: `wine foobar2000-x64_v2.1.5.exe`
3. Install the beefweb plugin in foobar2000
4. Install (potential) dependencies
    - `sudo dnf -y groupinstall "Development Tools"`
    - `sudo dnf install pipx cairo-devel pkg-config python3-pip python3-devel cmake gobject-introspection-devel cairo-gobject-devel`
    - Some of these may not be needed, but all were needed for development
5.  Install `beefweb_mpris`: `pipx install git+https://github.com/ther0n/beefweb_mpris.git`
    - `pipx` can also be installed with `pip install --user pipx`, installation using `pipx` is highly recommended unless you know what you're doing :)
7. Create a script to launch foobar2000 somewhere in your $PATH, make sure it's executable with `chmod +x`
   - For example `~/.local/bin/foobar2000`:
   ```bash
    #!/bin/bash
    
    env WINEPREFIX="/home/theron/.wine" wine "/home/theron/.wine/drive_c/Program Files/foobar2000/foobar2000.exe"
    ```
8. Edit `$CONFIG/beefweb_mpris/config.yaml` to match your settings for beefweb in foobar2000

   -`foobar2000-command` should be set to the foobar2000 launch script you just created (or the [one included with the AUR package](https://aur.archlinux.org/cgit/aur.git/tree/foobar2000.sh?h=foobar2000))
9. Edit or create a `.desktop` file to launch beefweb_mpris
   - For example my `~/.local/share/applications/wine/Programs/foobar2000.desktop` file:
   ```
    [Desktop Entry]
    Name=foobar2000
    Exec=beefweb_mpris
    Type=Application
    StartupNotify=true
    Comment=Play, organize and tag your music.
    Path=/home/theron/.wine/dosdevices/c:/Program Files/foobar2000
    Icon=9F8A_foobar2000.0
    StartupWMClass=foobar2000.exe
   ```

## Old Installation (Arch Linux)

Note: These are old instructions and were only tested on Arch linux but may still be useful for someone

1. Install foobar2000: `yay -S foobar2000`
2. Install beefweb in foobar2000
3. Install `beefweb_mpris`: `pip install --user git+https://github.com/ther0n/beefweb_mpris.git`
4. Run `beefweb_mpris` on the command line
5. Edit `$CONFIG/beefweb_mpris/config.yaml` to match your settings for beefweb in foobar2000

   -`foobar2000-command` should be set to a [command/script to run foobar2000](https://aur.archlinux.org/cgit/aur.git/tree/foobar2000.sh?h=foobar2000)

6. Create/edit a `.desktop` file to launch beefweb_mpris
