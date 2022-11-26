from bs4 import BeautifulSoup
import tmc_utils.tor_initialization as ti
import requests


# %%
# Test whether TOR works
ti.initiate_tor()
tor_request = ti.get_tor_session()
print("Tor IP:", tor_request.get("http://httpbin.org/ip").text)
print("Actual IP:", requests.get("http://httpbin.org/ip").text)

# %%
# Dummy request
req = tor_request.get(
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

ti.kill_tor_process()
