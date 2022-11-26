"""Initialize TOR for requests.

This module facilitates the usage of TOR for making requests.
Note that `tor.exe` needs to be installed and added in the user's PATH.

The module contains the following functions:

- `get_tor_session()` - Prepares the SOCKS proxy for TOR
- `initiate_tor()` - Starts the tor.exe process in Windows
- `kill_tor_process()` - Terminates the tor.exe process in Windows
"""

import os
import subprocess
import re
import requests
import stem.process


def get_tor_session():
    """Set up the SOCKS5 proxy for TOR

    Returns:
        requests.sessions.Session: A session object with custom proxies
    """
    session = requests.session()
    session.proxies = {
        "http": "socks5://127.0.0.1:9050",
        "https": "socks5://127.0.0.1:9050",
    }
    return session


def initiate_tor():
    """Starts the tor.exe process

    Raises:
        SystemExit: Exits on non-Windows systems or when tor.exe isn't found

    Returns:
        subprocess.Popen: Starts the tor.exe process
    """
    if os.name == "nt":
        # Find the path of tor.exe
        byte_path = subprocess.run(["where", "tor"], stdout=subprocess.PIPE)
        tor_path = byte_path.stdout.decode("utf-8").strip()
        # Check if tor.exe is installed
        if len(tor_path) == 0:
            print(
                "The TOR executable could not be found.",
                "Please, check if tor.exe is installed or added in PATH.")
            raise SystemExit
        # Start TOR process
        port = 9050
        tor_process = stem.process.launch_tor_with_config(
            config={
                "SocksPort": str(port),
            },
            init_msg_handler=lambda line: print(line)
            if re.search("Bootstrapped", line)
            else False,
            tor_cmd=tor_path,
        )
        return tor_process

    print("Sorry, Windows 10/11 is needed to route requests through TOR.")
    raise SystemExit


def kill_tor_process():
    """Terminates the tor.exe process"""
    # Kill the executable ungracefully as tor_process.kill() did not work?
    killmsg = subprocess.run(
        ["taskkill", "/im", "tor.exe", "/F"], stdout=subprocess.PIPE
    )
    return print(str(killmsg.stdout.decode("utf-8")))
