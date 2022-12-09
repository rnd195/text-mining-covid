import requests
from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd
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
    timeout=30,
)

# %%
# Parse HTML to see whether everything works
soup = BeautifulSoup(req.text, "html.parser")

# Do not persist at this point. Persist cleaned text (stemmed etc.) later
catalog = article_props.generate_article_df(soup)

# %%
# Initialize column
in_article_dict = {"word_counter": [], "author": [], "topics": []}

for j, url in enumerate(catalog.link):
    if catalog.premium[j]:
        in_article_dict["word_counter"].append(pd.NA)
        in_article_dict["author"].append(pd.NA)
        in_article_dict["topics"].append(pd.NA)
    else:
        in_article_dict["word_counter"].append(Counter(["abc", "def"]))
        in_article_dict["author"].append(["AB", "CD"])
        in_article_dict["topics"].append(["topic1", "topic2"])

cat_and_artcls = pd.concat([catalog, pd.DataFrame(in_article_dict)], axis=1)
cat_and_artcls

# %%
ti.kill_tor_process()
