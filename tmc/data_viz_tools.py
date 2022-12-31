"""Data visualization tools

This module works with the dataframe outputted by `dynamic_join.py`. It provides several data
visualization options, both static and interactive.

The module contains the following functions:

- create_all_words(df) - Concatenate Counter objects
- basic_wordcloud(all_words_df, width=15, height=10) - Plot a simple wordcloud
- create_hourly_df(df, words_to_delete) - Produce a long dataframe of hours / words / counts
- hourly_words_barplot(df_hourly_words_long, y_range, width=1000, height=600) - Interactive barplot
"""
from functools import reduce
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud


def create_all_words(df, words_to_delete):
    """Join all Counter objects into one and delete specific words

    Args:
        df (pandas.core.frame.DataFrame): Output of `dynamic_join.py`
        words_to_delete (list): List of words to delete

    Returns:
        all_words (collections.Counter): Counter object of most frequent words
    """

    all_words = reduce(lambda a, b: a + b, df.word_counter.dropna())

    # Delete a defined list of words
    if len(words_to_delete) > 0:
        for word in words_to_delete:
            if word in all_words:
                del all_words[word]

    return all_words


def basic_wordcloud(all_words_df, width=15, height=10):
    """Generate a simple wordcloud using the `wordcloud` and `matplotlib` packages

    Args:
        all_words_df (pandas.core.frame.DataFrame): Output of `create_all_words()`
        width (int, optional): Figure width, defaults to 15
        height (int, optional): Figure height, defaults to 10

    Returns:
        A wordcloud plot.
    """
    cloud = WordCloud(width=1280, height=720).generate_from_frequencies(all_words_df)
    plt.figure(figsize=[width, height])
    plt.axis("off")
    plt.imshow(cloud)


def create_hourly_df(df, words_to_delete):
    """Create a per-hour dataframe of top 10 words and their counts

    Args:
        df (pandas.core.frame.DataFrame): Dataframe of articles
        words_to_delete (list): List of words to be deleted (e.g. common words)

    Returns:
        df_hourly_words_long (pandas.core.frame.DataFrame): Long dataframe of hours / words / counts

    """
    # Join Counter objects for each hour from 6 to 20
    list_hourly = [
        [i, reduce(lambda a, b: a + b, df.word_counter[df.time_hour == i].dropna())]
        for i in range(6, 21)
    ]

    df_hourly = pd.DataFrame(list_hourly, columns=["hour", "words"])

    # Delete a defined list of words
    if len(words_to_delete) > 0:
        for i in df_hourly.index:
            for word in words_to_delete:
                if word in df_hourly.words.iloc[i]:
                    del df_hourly.words.iloc[i][word]

    # Split the counter object into words and frequencies only
    list_top_w = []
    list_top_f = []

    for i in df_hourly.index:
        list_top_w.append([j[0] for j in df_hourly.words[i].most_common(10)])
        list_top_f.append([j[1] for j in df_hourly.words[i].most_common(10)])

    df_hourly["top_words"] = list_top_w
    df_hourly["top_freqs"] = list_top_f

    # Create a long dataset with individual hours, words, and counts as columns
    list_hourly_words_long = []

    for i, hour in enumerate(df_hourly.hour):
        for word in enumerate(df_hourly.top_words[i]):
            list_hourly_words_long.append([hour, word[1], df_hourly.top_freqs[i][word[0]]])

    df_hourly_words_long = pd.DataFrame(
        list_hourly_words_long,
        columns=["hour", "word", "frequency"]
    )

    return df_hourly_words_long


def hourly_words_barplot(df_hourly_words_long, y_range: list, width=1000, height=600):
    """Generate an interactive barchart using `plotly`

    Args:
        df_hourly_words_long (pandas.core.frame.DataFrame): Dataframe produced by `create_hourly_df()`
        y_range (list): Range of the y axis (frequency of words)
        width (int, optional): Figure width in pixels, defaults to 1000
        height (int, optional): Figure height in pixelsm, defaults to 600

    Returns:
        Interactive barchart.

    """
    fig = px.bar(
        df_hourly_words_long,
        x="word",
        y="frequency",
        animation_frame="hour",
        width=width,
        height=height,
        range_y=y_range
    )
    fig["layout"].pop("updatemenus")
    fig.show()
