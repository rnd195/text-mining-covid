import requests
from bs4 import BeautifulSoup
import tmc_utils.tor_initialization as ti
import tmc_utils.article_props as article_props


# %%
# Test whether TOR works
ti.initiate_tor()
tor_request = ti.get_tor_session()
print("Tor IP:", tor_request.get("http://httpbin.org/ip", timeout=30).text)
print("Actual IP:", requests.get("http://httpbin.org/ip", timeout=30).text)

# %%
# Dummy request
req = tor_request.get(
    "https://www.idnes.cz/zpravy/zahranicni/koronavirus.K466979/182",
    timeout=30
)

# %%
# Parse HTML to see whether everything works
soup = BeautifulSoup(req.text, "html.parser")

# Do not persist at this point. Persist cleaned text (stemmed etc.) later
article_df = article_props.generate_article_df(soup)


# %%
ti.kill_tor_process()
