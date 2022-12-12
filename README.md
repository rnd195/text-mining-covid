## Installing TOR

A convenient way of installing TOR on your <u>Windows</u> personal computer:

- Install Chocolatey Package Manager https://chocolatey.org/install#individual

- Open `cmd.exe` with admin privileges
- Run `choco install tor -y` 

## TODO

- [x] Provide an option to not route through TOR
  - [x] `Make anonymous requests through TOR? ([y]es / [n]o): `
  - [x] The alternative is to use the [Archive.org API](https://medium.com/analytics-vidhya/the-wayback-machine-scraper-63238f6abb66) or [Google Webcache](https://stackoverflow.com/q/19010131)
  - [ ] Consider implementing the `internetarchive` package
- [x] Stem titles and perexes
  - [x] Create workflow
  - [x] Apply to all 
- [ ] Persist cleaned data
- [ ] Inspect and process individual articles
- [ ] Create a well-structured README

## Notes

We have decided to restrict our analysis to span from early 2020 until the end of June 2021 as roughly 80% of all covid-related articles have been written within this period. The second reason is that the articles written on the topic in later months gradually seem to be related to the pandemic less and less.

## Sources

- https://ohyicong.medium.com/how-to-create-tor-proxy-with-python-cheat-sheet-101-3d2d619a1d39
- https://stackoverflow.com/a/33875657
- https://realpython.com/python-nltk-sentiment-analysis/
- https://machinelearninggeek.com/text-analytics-for-beginners-using-python-nltk/
- https://www.kirenz.com/post/2021-12-11-text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/