from os import chdir, listdir
from os.path import dirname, abspath
from collections import Counter
import ast
import pandas as pd


def str_to_list(item):
    """Convert a string representation of a list to a list while handling NAs"""
    return ast.literal_eval(item) if isinstance(item, str) else pd.NA


# Set working directory to filepath
chdir(dirname(abspath(__file__)))

# Get all .csv files in the data directory
CSV_PATH = "data/full_dfs/"
csv_dir = listdir(CSV_PATH)
csv_files = list(filter(lambda f: f.endswith(".csv"), csv_dir))

# Load first and append the rest
df = pd.read_csv(CSV_PATH + csv_files[0], index_col=0)

for file in csv_files[1:]:
    temp_df = pd.read_csv(CSV_PATH + file, index_col=0, na_values=pd.NA)
    df = pd.concat([df, temp_df], axis=0)

# Manually set the type of the date column
df = df.reset_index(drop=True)
df["date"] = pd.to_datetime(df["date"])

# Convert the time column into two integer cols: hours and minutes
time_hour = df["time"].apply(lambda x: int(x[0:2]) if isinstance(x, str) else pd.NA)
time_min = df["time"].apply(lambda x: int(x[3:5]) if isinstance(x, str) else pd.NA)
df.insert(2, "time_hour", time_hour)
df.insert(3, "time_min", time_min)
df.pop("time")

# Convert columns to lists and then process further if necessary
for col in ["title", "perex_short", "perex_full", "word_counter", "authors_hash", "topics"]:
    df[col] = df[col].apply(str_to_list)

df["word_counter"] = df.word_counter.apply(
    lambda x: Counter({key: value for (key, value) in x}) if isinstance(x, list) else pd.NA
)
