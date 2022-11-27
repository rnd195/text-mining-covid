from bs4 import BeautifulSoup
import tmc_utils.tor_initialization as ti
import requests
import pandas as pd
import datetime


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

# Initialize empty dictionary
article_dict = {
    "link": [],
    "date": [],
    "time": [],
    "title": [],
    "perex": [],
    "premium": []
}

# Find and append links, dates, time, titles, perex, and premium access
for item in content.findAll("div", {"class": "art"}):
    link = item.find("a", {"class": "art-link"}, href=True)["href"]
    article_dict["link"].append(link)

    date_and_time = pd.to_datetime(
        item.find("span", {"class": "time"})["datetime"]
    )
    article_dict["date"].append(date_and_time.date())
    # Articles with no specific time have 00:00:00 as the time of publication
    if date_and_time.time() == datetime.time(0, 0):
        article_dict["time"].append(pd.NA)
    else:
        article_dict["time"].append(date_and_time.time())

    title = item.find("a", {"class": "art-link"}).find("h3").text.strip()
    article_dict["title"].append(title)

    # 'perex' is the lead paragraph of each article displayed in the preview
    perex = item.find("p", {"class": "perex"})
    # It also gives us the ability to find whether it is a premium article
    if perex.find("a", {"class": "premlab"}) is None:
        article_dict["perex"].append(perex.text.strip())
        article_dict["premium"].append(False)
    else:
        # The word "Premium" is skipped
        article_dict["perex"].append(perex.text[len("Premium") + 1:].strip())
        article_dict["premium"].append(True)

# Do not persist at this point. Persist cleaned text (stemmed etc.) later
article_df = pd.DataFrame(article_dict)

# %%
ti.kill_tor_process()
