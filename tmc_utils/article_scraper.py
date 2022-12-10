"""Generate a dataframe with article properties.

Produces a dataframe with article details such as title, date, or link. Any
meaningful text is pre-processed using the `clean_text` module. Note that it
is tailored to a specific HTML structure of idnes.cz.

The module contains the following functions:

- `soup_object_tor(link, tor_request_obj)` - Parses a TOR request
- `soup_object_request_all(link, tor_request_obj=None)` - Requests Archive.org before TOR or Google Webcache
- `generate_article_df(soup_object)` - Generates a dataframe of article properties
- `add_content(article_df, tor_requests_obj, sleeping=(10, 15))` - Adds content
   and other attributes to the df from the function `generate_article_df`
"""

from time import sleep
from random import uniform
from collections import Counter
from itertools import chain
import datetime
import requests
import pandas as pd
from tmc_utils.clean_text import sentence_cleaner_cz
from bs4 import BeautifulSoup


def soup_object_tor(link, tor_request_obj):
    """"Send a request through TOR and parse it using BeautifulSoup"""

    req = tor_request_obj.get(
        link,
        timeout=30,
    )
    return BeautifulSoup(req.text, "html.parser")


def soup_object_request_all(link, tor_request_obj=None):
    """Request Archive.org before using TOR or Google Webcache and return a BeautifulSoup object"""

    archive_link = "http://archive.org/wayback/available?url=" + link
    archive_json = requests.get(archive_link, timeout=30).json()
    archived = len(archive_json["archived_snapshots"]) != 0

    # Continue if the website is available on archive.org
    if archived and archive_json["archived_snapshots"]["closest"]["available"]:
        req = requests.get(archive_json["archived_snapshots"]["closest"]["url"], timeout=30)
        print("Found a snapshot on Archive.org.")
        return BeautifulSoup(req.text, "html.parser")

    # Otherwise try TOR
    if not archived and tor_request_obj is not None:
        print(
            f"URL: {link}",
            "could not be found on Archive.org, trying TOR."
        )
        return soup_object_tor(link, tor_request_obj)

    # And finally try Google Webcache - not yet tested whether this works as intended
    print(
        f"URL: {link}",
        "could not be found on Archive.org and TOR is not avaiable.",
        "Trying Google Webcache."
    )
    req = requests.get(
        "https://webcache.googleusercontent.com/search?q=cache:" + link,
        timeout=30
    )
    if not req:
        print("The website hasn't been cached or something else went wrong. Outputting None.")
        return None
    return BeautifulSoup(req.text, "html.parser")



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
        "perex_short": [],
        "premium": [],
        "video": [],
        "gallery": []
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
        # Video articles don't have perex in the preview (e.g. around p. 203)
        if perex is None:
            article_dict["perex_short"].append(pd.NA)
            article_dict["premium"].append(False)
        # It also gives us the ability to find whether it is a premium article
        elif perex.find("a", {"class": "premlab"}) is None:
            perex_list = sentence_cleaner_cz(perex.text)
            article_dict["perex_short"].append(perex_list)
            article_dict["premium"].append(False)
        else:
            # The word "Premium" is skipped
            perex_list = sentence_cleaner_cz(perex.text[len("Premium") + 1:])
            article_dict["perex_short"].append(perex_list)
            article_dict["premium"].append(True)
        # Some articles are purely video-based
        video = item.find("a", {"score-type": "Video"})
        if video is not None:
            article_dict["video"].append(True)
        else:
            article_dict["video"].append(False)
        # Some articles are just photo galleries
        if link[-5:] == "/foto":
            article_dict["gallery"].append(True)
        else:
            article_dict["gallery"].append(False)

    return pd.DataFrame(article_dict)


def add_content(article_df, tor_requests_obj, sleeping=(5, 10)):
    """Add content to the article dataframe generated by `generate_article_df`

    Args:
        article_df (pandas.core.frame.DataFrame): Dataframe with article properties
        tor_requests_obj (requests.sessions.Session): TOR requests object
        sleeping (tuple, optional): Sleep time inbetween requests, defaults to (10, 15)

    Returns:
        pandas.core.frame.DataFrame: Dataframe with article properties and other content

    """
    in_article_dict = {
        "perex_full": [],
        "word_counter": [],
        "authors_hash": [],
        "topics": []
    }

    for j, url in enumerate(article_df.link):
        # Provide simple progress bar
        print(
            f"Processing page {j} / {len(article_df.link)}.",
            f"Estimated time left: {sleeping[1] * (len(article_df.link) - j)}s"
        )

        # Skip for premium, gallery, and video articles
        if article_df.premium[j] or article_df.gallery[j] or article_df.video[j]:
            in_article_dict["perex_full"].append(pd.NA)
            in_article_dict["word_counter"].append(pd.NA)
            in_article_dict["authors_hash"].append(pd.NA)
            in_article_dict["topics"].append(pd.NA)
            continue

        # Request and parse
        soup_page = soup_object_request_all(url, tor_requests_obj)

        if soup_page is None:
            print("Tried Archive.org, TOR, and Google Webcache, found nothing. Skipping.")
            continue

        # Give the page some breathing room
        sleep(round(uniform(sleeping[0], sleeping[1]), 3))

        # Full perex
        try:
            perex_full = sentence_cleaner_cz(
                soup_page.find("div", {"class": "opener"}).text
            )
        # Some subpages have a different name for the opening paragraph
        except AttributeError:
            perex_full = sentence_cleaner_cz(
                soup_page.find("div", {"class": "excert"}).text
            )
        in_article_dict["perex_full"].append(perex_full)

        # Content of the article as a Counter object
        content_list = []
        div_art_text = soup_page.find("div", {"id": "art-text"})
        # Some subpages use a different attribute for content
        if div_art_text is None:
            div_art_text = soup_page.find("div", {"class": "content"})

        for item in div_art_text.findAll("p", attrs={"class": None}):
            content_list.append(sentence_cleaner_cz(item.text))

        # Unnest nested lists -> convert iterable to list -> apply Counter
        in_article_dict["word_counter"].append(
            Counter(list(chain.from_iterable(content_list)))
        )

        # Hashed author names
        authors_div = soup_page.find("div", {"class": "authors"}).find(
            "span", {"itemprop": "name"}
        )
        # For our intents and purposes, we won't store names of the authors
        # Instead, we store hashes - unique ID for each author
        in_article_dict["authors_hash"].append(
            [hash(x) for x in authors_div.text.split(", ")]
        )

        # Topics or tags of each article (lowercase)
        tags = []
        try:
            topics_div = soup_page.find("div", {"id": "art-tags"}).findAll("a")
            for tag in topics_div:
                tags.append(tag.text.strip().lower())
            in_article_dict["topics"].append(tags)
        # In some cases, there are no tags
        except AttributeError:
            in_article_dict["topics"].append(pd.NA)

    return pd.concat(
        [article_df, pd.DataFrame(in_article_dict)],
        axis=1
    )
