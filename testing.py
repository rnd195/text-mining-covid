import requests
from bs4 import BeautifulSoup
import os
import subprocess
import io
import os
import stem.process
import re


def get_tor_session():
    session = requests.session()
    # Prepare SOCKS proxy for Tor
    session.proxies = {
        "http": "socks5://127.0.0.1:9050",
        "https": "socks5://127.0.0.1:9050",
    }
    return session


# %%
# Dummy request
req = requests.get(
    "https://www.idnes.cz/zpravy/zahranicni/koronavirus.K466979/200"
)

# %%
# Parse HTML to see whether everything works
soup = BeautifulSoup(req.text, "html.parser")
content = soup.find("div", {"id": "list-art-count"})

final_list = []

# Find dates, strip-off whitespaces and other unwanted content
for dt in content.findAll("span"):
    if dt.has_attr("datetime"):
        date_time = dt["datetime"]
        # Only the first 10 chars needed for date
        date = date_time[:10]
        final_list.append(date)

print(final_list)

# %%
port = 9050
byte_path = subprocess.run(["where", "tor"], stdout=subprocess.PIPE)
tor_path = byte_path.stdout.decode("utf-8").strip()
tor_process = stem.process.launch_tor_with_config(
    config={
        "SocksPort": str(port),
    },
    init_msg_handler=lambda line: print(line)
    if re.search("Bootstrapped", line)
    else False,
    tor_cmd=tor_path,
)

# %%
# Test out whether Tor works
session = get_tor_session()
print("Tor IP:", session.get("http://httpbin.org/ip").text)
print("Actual IP:", requests.get("http://httpbin.org/ip").text)

# Kill the executable ungracefully as tor_process.kill() did not work well
killmsg = subprocess.run(
    ["taskkill", "/im", "tor.exe", "/F"], stdout=subprocess.PIPE
)
print(str(killmsg.stdout.decode("utf-8")))
