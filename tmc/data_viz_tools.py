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
import numpy as np
import requests


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
        A wordcloud plot
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
            list_hourly_words_long.append(
                [hour, word[1], df_hourly.top_freqs[i][word[0]]]
            )

    df_hourly_words_long = pd.DataFrame(
        list_hourly_words_long, columns=["hour", "word", "frequency"]
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
        Interactive barchart

    """
    fig = px.bar(
        df_hourly_words_long,
        x="word",
        y="frequency",
        animation_frame="hour",
        width=width,
        height=height,
        range_y=y_range,
        title="Most frequent words per hour"
    )
    fig.update_traces(
        marker_line_color="rgb(10, 45, 100)",
        marker_line_width=1.5,
        opacity=0.65,
    )
    fig["layout"].pop("updatemenus")
    fig.show()

def hourly_density(article_df):
    """Plot a density function of the distribution of articles in daytime.

    Args:
        article_df (pandas.core.frame.DataFrame): Dataframe of all articles in given time.


    Returns:
        Density function

    """
    df = article_df[~article_df["time_hour"].isna()].astype({"time_hour" : "int"})
    df.time_hour.plot(kind='density', ind=np.linspace(0, 23, 400))
    plt.xlabel("Hour")
    plt.ylabel("probability of publishing")
    plt.title("Density of publications")

def time_stats(df):
    """Function performing descriptive statistics about the time when given articles were published.

        Args:
            df (pandas.core.frame.DataFrame): Dataframe of all articles in given time.


        Returns:
            time stats about articles.
    """
    hour, mins = df.time_hour.dropna(), df.time_min.dropna()

    # Convert time to decimals in order to perform descriptive statistics
    daytime = hour.astype("str") + ":" + mins.astype("str")
    daytime_serie = [round(float(t[0]) + float(t[1])/60,2) for t in [t.split(":") for t in daytime]]

    # Compute mean and median and Covert them back to time format
    splitted = [str(stat).split(".") for stat in [round(np.mean(daytime_serie), 2), round(np.median(daytime_serie), 2)]]

    # Data are stored as dictionary
    stats =  dict(zip(["Mean time of publication", "Median Time of publication"],
                    [[":".join([t[0], str(round(float(t[1])*0.6))])] for t in splitted]))
    stats["Least active daily hour"] = [str(df.time_hour.value_counts().index[-1]) + ":" + "00"]
    stats["Most active daily hour"] = [str(df.time_hour.value_counts().index[0]) + ":" + "00"]

    # Convert data to df and then transpose to obtain better readability
    stats_df = pd.DataFrame(stats).T
    stats_df.rename(columns={0: "Time of Publication"}, inplace=True)
    return stats_df

def hourly_bar(df):
    """Function plotting hourly published articles.

           Args:
               df (pandas.core.frame.DataFrame): Dataframe of all articles in given time.


           Returns:
               Bar plot.
    """
    df.time_hour.value_counts().sort_index().plot(kind="bar")
    plt.xlabel("Hour")
    plt.ylabel("Number articles")
    plt.title("Articles published at given time")

def line_plot(df):
    """Function plotting daily published articles.

           Args:
               df (pandas.core.frame.DataFrame): Dataframe of all articles in given time.


           Returns:
               Line plot.
    """
    df.date = pd.to_datetime(df.date)
    df.date.value_counts().sort_index().plot()
    plt.xlabel("Date")
    plt.ylabel("Number articles")
    plt.title("Articles published")

def section_bar(df):
    """Function returning frequency of the articles classified into particular section.

           Args:
               df (pandas.core.frame.DataFrame): Dataframe of all articles in given time.


           Returns:
               DataFrame collecting section stats ready to plot.
    """
    sections = df.link.apply(lambda x: x.split("/")[1]).value_counts()
    sections_df = pd.DataFrame(sections)
    sections_df.rename(columns={"link": "Unique sections"}, inplace=True)
    return sections_df

def plot_section(section_stats):
    """Function plotting frequency of the articles classified into particular section.

           Args:
               section_stats (pandas.core.frame.DataFrame): Dataframe of unique sections frequencies.


           Returns:
               Bar plot.
    """
    section_stats.plot(kind="bar")
    plt.title("Number of articles published under given section")

def cases_df(df):
    """Function importing number of the covid cases in the Czechia for the period associated with
                the time window of the Dataframe of all articles in given time.

           Args:
               df (pandas.core.frame.DataFrame): Dataframe of all articles in given time.


           Returns:
               DataFrame.
    """
    # Define the time window
    start = str(df.date.min())[:len(str(df.date.min())) - 9]
    end = str(df.date.max())[:len(str(df.date.max())) - 9]

    # Import Covid cases data as json and the store them as DataFrame.
    link = f"https://api.covid19api.com/country/czech-republic/status/confirmed?from={start}T00:00:00Z&to={end}T00:00:00Z"
    cases = pd.DataFrame(requests.get(link).json())
    cases.Date = pd.to_datetime(cases.Date)
    cases.Date = cases.Date.dt.strftime('%Y-%m-%d')

    return cases

def article_cases_plot(df, cases):
    """Function plotting number of articles and number of Covid19 cases into one figure.

           Args:
               df (pandas.core.frame.DataFrame): Dataframe of all articles in given time.

               cases (pandas.core.frame.DataFrame): Dataframe of covid cases in given time.


           Returns:
               Line plot.
    """
    # preparing data about articles
    df.date = df.date.dt.strftime('%Y-%m-%d')
    articles_df = df.date.value_counts().sort_index()

    # Plotting with shared y
    fig, ax1 = plt.subplots(figsize=(9, 6))

    # Instantiate a second axes that shares the same x-axis
    ax2 = ax1.twinx()
    ax1.plot(articles_df.index,
             articles_df,
             color="#69b3a2")
    ax1.set_xlabel("day", fontsize=14)
    ax1.set_ylabel("number of articles",
                   color="#69b3a2",
                   fontsize=14)

    # make a plot with different y-axis using second axis object
    ax2.plot(cases.Date, cases.Cases, color="#3399e6")
    ax2.set_ylabel("Covid19 Cases", color="#3399e6", fontsize=14)
    fig.suptitle("Relation ship between covid articles and covid cases", fontsize=20)
    fig.autofmt_xdate()
    plt.show()
