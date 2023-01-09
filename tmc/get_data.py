"""Get article data

This script is used to obtain data article data from idnes.cz. First, a TOR
proxy is established, if possible. Then the user specifies the list start and
list end of the article list in question. The user is then informed about the
minimum amount of time the process will take (given that no rate limiting
takes place). Consent needs to be given in order to continue the script.
Finally, the script first collects the article lists and then processes public
articles as specified in `article_scraper.py`.
"""
# %%
from os import chdir
from os.path import dirname, abspath
from random import uniform
from time import sleep
import requests
import pandas as pd
import tmc_utils.tor_initialization as ti
import tmc_utils.article_scraper as arts


# Set working directory to filepath
chdir(dirname(abspath(__file__)))

# %%
# Initialize TOR
if ti.tor_available():
    ti.initiate_tor()
    tor_request = ti.get_tor_session()
    print("Tor IP:", tor_request.get("http://httpbin.org/ip", timeout=30).text)
    print("Actual IP:", requests.get("http://httpbin.org/ip", timeout=30).text)
else:
    tor_request = None
    

# %%
while True:
    try:
        LIST_START = int(input("Input list start (e.g. 289): "))
        LIST_END = int(input("Input list end (e.g. 290): "))
    except ValueError:
        print("Supply an integer as the start/end of the list.")
        continue
    # The list starts at 2 and ends at 455 as of Jan 2023
    if LIST_START >= LIST_END or LIST_START <= 1 or LIST_START > 455:
        print("LIST_START has to be strictly larger than 1 and lower than LIST_END.")
        continue

    print("List start:", LIST_START, "\nList end:", LIST_END)
    break

# Inform the user about the time it will take and ask for consent
LIST_LENGTH = LIST_END - LIST_START

print(
    # 10 seconds for each list, 36 articles in a list, each taking around 15 seconds
    f"""
    {LIST_LENGTH} lists and around {LIST_LENGTH * 36} articles will be processed.
    This might take at least {(LIST_LENGTH * 10 + LIST_LENGTH * 36 * 15) // 60} minutes,
    provided that the user doesn't get rate limited.
    We recommend processing no more than 2 lists at a time.
    By continuing, you express your familiarity with the terms of service of the accessed website.
    """
)

while True:
    try:
        CONSENT = str(input("Would you like to continue? ([y]es / [n]o): ")).upper()
    except ValueError:
        print("Incorrect input, please try again.")
        continue
    if CONSENT not in ("Y", "N"):
        print("Incorrect input, please try again.")
        continue
    break

if CONSENT == "N":
    print("Exiting.")
    ti.kill_tor_process()
    raise SystemExit

# %%
# First, obtain the list of article lists and save them as partial dfs
for i in range(LIST_START, LIST_END):
    print(f"PAGE LIST NUMBER: {i} / {LIST_END - 1}")
    URL = "https://www.idnes.cz/zpravy/zahranicni/koronavirus.K466979/" + str(i)
    soup = arts.soup_object_tor(URL, tor_request)
    article_df = arts.generate_article_df(soup)
    print(f"List number {i} processed. Saving the resulting dataframe.\n")
    article_df.to_csv(f"data/partial_dfs/partial_df_{i}.csv")
    sleep(round(uniform(5, 10), 3))

# %%
# Persist cleaned pages without accessing idnes.cz directly due to the high number of requests
for i in range(LIST_START, LIST_END):
    print(f"PAGE LIST NUMBER: {i} / {LIST_END - 1}\n")
    temp_df = pd.read_csv(
        "data/partial_dfs/partial_df_" + str(i) + ".csv",
        index_col=0,
        na_values=pd.NA
    )
    # Create article dataframe
    cat_and_artcls = arts.add_content(temp_df, tor_request)
    print(f"\nList number {i} processed. Saving the resulting dataframe.\n")
    cat_and_artcls.to_csv(f"data/full_dfs/full_df_{i}.csv")
    # Sleep so that the user has time to read the message
    sleep(2)

# %%
if ti.tor_available():
    ti.kill_tor_process()
