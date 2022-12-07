"""Generate a dataframe with article properties.

Produces a dataframe with article details such as title, date, or link. Any
meaningful text is pre-processed using the `clean_text` module. Note that it
is tailored to a specific HTML structure of idnes.cz.

The module contains the following function:

- `generate_article_df(soup_object)` - Generates a dataframe of article properties
"""

import pandas as pd
import datetime
from tmc_utils.clean_text import sentence_cleaner_cz


def generate_article_df(soup_object):
    """Generate a dataframe of article properties

    Args:
        soup_object (bs4.BeautifulSoup): Parsed HTML document using BeautifulSoup

    Returns:
        pandas.core.frame.DataFrame: Dataframe with article properties
    """
    soup_content = soup_object.find("div", {"id": "list-art-count"})
    # Initialize empty dictionary
    article_dict = {
        "link": [],
        "date": [],
        "time": [],
        "title": [],
        "perex": [],
        "premium": [],
        "video": [],
    }

    # Find and append links, dates, time, titles, perex, and premium access
    for item in soup_content.findAll("div", {"class": "art"}):
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

        title = item.find("a", {"class": "art-link"}).find("h3").text
        title_list = sentence_cleaner_cz(title)
        article_dict["title"].append(title_list)

        # 'perex' is the lead paragraph of each article (shortened here)
        perex = item.find("p", {"class": "perex"})
        # Video articles don't have perex in the preview
        if perex is None:
            article_dict["perex"].append(pd.NA)
            article_dict["premium"].append(False)
        # It also gives us the ability to find whether it is a premium article
        elif perex.find("a", {"class": "premlab"}) is None:
            perex_list = sentence_cleaner_cz(perex.text)
            article_dict["perex"].append(perex_list)
            article_dict["premium"].append(False)
        else:
            # The word "Premium" is skipped
            perex_list = sentence_cleaner_cz(perex.text[len("Premium") + 1:])
            article_dict["perex"].append(perex_list)
            article_dict["premium"].append(True)
        # Some articles are purely video-based
        video = item.find("a", {"score-type": "Video"})
        if video is not None:
            article_dict["video"].append(True)
        else:
            article_dict["video"].append(False)

    return pd.DataFrame(article_dict)
