from os import chdir, listdir
from os.path import dirname, abspath
import pandas as pd

# Set working directory to filepath
chdir(dirname(abspath(__file__)))

# Get all .csv files in the data directory
CSV_PATH = "data/full_dfs/"
csv_dir = listdir(CSV_PATH)
csv_files = list(filter(lambda f: f.endswith(".csv"), csv_dir))

# Load first and append the rest
df = pd.read_csv(CSV_PATH + csv_files[0], index_col=0)

for file in csv_files[1:]:
    temp_df = pd.read_csv(CSV_PATH + file, index_col=0)
    df = pd.concat([df, temp_df], axis=0)

df = df.reset_index(drop=True)
df.head()
