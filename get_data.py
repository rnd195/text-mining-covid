from os import chdir
from os.path import dirname, abspath
from time import sleep
import requests
import tmc_utils.tor_initialization as ti
import tmc_utils.article_scraper as arts


# Set working directory to filepath
chdir(dirname(abspath(__file__)))

# %%
# Initialize TOR
ti.initiate_tor()
tor_request = ti.get_tor_session()
print("Tor IP:", tor_request.get("http://httpbin.org/ip", timeout=30).text)
print("Actual IP:", requests.get("http://httpbin.org/ip", timeout=30).text)

# %%
# Persist cleaned pages
# The end number is difficult to get programatically
LIST_START = 358
LIST_END = 359

for i in range(LIST_START, LIST_END):
    print(f"PAGE LIST NUMBER: {i} / {LIST_END - 1}\n")
    URL = "https://www.idnes.cz/zpravy/zahranicni/koronavirus.K466979/" + str(i)
    soup = arts.soup_object_tor(URL, tor_request)
    # Create article dataframe
    cat_and_artcls = arts.add_content(arts.generate_article_df(soup), tor_request)
    print(f"\nList number {i} processed. Saving the resulting dataframe.\n")
    cat_and_artcls.to_csv(f"data/df_{i}.csv")
    # Sleep so that the user has time to read the message
    sleep(2)

# %%
ti.kill_tor_process()
