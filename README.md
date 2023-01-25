# Final project

**Course:** Data Processing in Python ([JEM207](https://github.com/vitekzkytek/PythonDataIES/))

**Authors:** Martin Řanda & David Černý



This project aims to demonstrate a framework in visualizing trends in the news. It provides a way to *ethically* scrape a list of link from a particular news website through the [Tor network](https://www.torproject.org/), and requesting individual articles using the [Wayback Machine](https://archive.org/web) or Google Webcache. This is done to minimize the amount of traffic on the original website.

In our case, we visualize a month's worth of coronavirus-related articles from idnes.cz, which can be seen in `data_visualization.ipynb`. It includes both interactive plots generated using [plotly](https://plotly.com/python/) as well as static charts produced by [matplotlib](https://matplotlib.org/). Below is an example of a [Wordcloud](https://github.com/amueller/word_cloud) we generated using the coronavirus data:

![wordcloud](assets/wordcloud_example.png)

We also provide documentation and tutorials in the `docs/` directory of the project in HTML format generated using [MkDocs](https://www.mkdocs.org/). The source Markdown files used for generating the docs can be found in `assets/docs_md`. *Currently*, we don't intend on hosting the documentation using Github Pages, meaning that it is only accessible offline as Github doesn't render HTML files. Alternatively, to see the documentation, run `mkdocs serve` in the root of the directory after installing all the necessary `mkdocs`-related packages:

```
pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python
```



## Requirements

1. Open your shell or command prompt in the root folder of the project
2. Assuming Python 3.10+ is installed, run the following command to install all the packages used in this project

```
pip install -r requirements.txt
```



## Installing Tor

A convenient way of installing TOR on your <u>Windows</u> personal computer:

- Install Chocolatey Package Manager https://chocolatey.org/install#individual

- Open `cmd.exe` with admin privileges
- Run `choco install tor -y` 



## Flowchart

![diagram](assets/diagram.jpg)



## Sources

- https://ohyicong.medium.com/how-to-create-tor-proxy-with-python-cheat-sheet-101-3d2d619a1d39
- https://stackoverflow.com/a/33875657
- https://realpython.com/python-nltk-sentiment-analysis/
- https://machinelearninggeek.com/text-analytics-for-beginners-using-python-nltk/
- https://www.kirenz.com/post/2021-12-11-text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/
