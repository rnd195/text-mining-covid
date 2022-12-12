from os import chdir
from os.path import dirname, abspath
from random import uniform
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
# First, obtain the list of article lists and save them as partial dfs
# The end number changes from time to time due to new articles being added
LIST_START = 93
LIST_END = 455

for i in range(LIST_START, LIST_END):
    print(f"PAGE LIST NUMBER: {i} / {LIST_END - 1}")
    URL = "https://www.idnes.cz/zpravy/zahranicni/koronavirus.K466979/" + str(i)
    soup = arts.soup_object_tor(URL, tor_request)
    article_df = arts.generate_article_df(soup)
    print(f"List number {i} processed. Saving the resulting dataframe.\n")
    article_df.to_csv(f"data/partial_dfs/partial_df_{i}.csv")
    sleep(round(uniform(5, 10), 3))

# %%
# USED FOR GENERATING full_df_355 - full_df_358, REDO FOR THE PERSISTED PARTIAL PAGES
# Persist cleaned pages
# for i in range(LIST_START, LIST_END):
#     print(f"PAGE LIST NUMBER: {i} / {LIST_END - 1}\n")
#     URL = "https://www.idnes.cz/zpravy/zahranicni/koronavirus.K466979/" + str(i)
#     soup = arts.soup_object_tor(URL, tor_request)
#     # Create article dataframe
#     cat_and_artcls = arts.add_content(arts.generate_article_df(soup), tor_request)
#     print(f"\nList number {i} processed. Saving the resulting dataframe.\n")
#     cat_and_artcls.to_csv(f"data/full_df_{i}.csv")
#     # Sleep so that the user has time to read the message
#     sleep(2)

# %%
ti.kill_tor_process()
