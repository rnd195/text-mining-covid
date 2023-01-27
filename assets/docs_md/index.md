# Project documentation

This is the documentation for the final project for the Data Processing in Python course at IES FSV CUNI in WS 2022/23 authored by Martin Řanda & David Černý.

The **How-To Guide** section contains tutorials on how to obtain new data and install Tor.

In the **Reference** section, we provide docstring for all the functions in this repository.



## Project layout

    text-mining-covid/
    ├─ assets/ # Images and documentation
    │  ├─ docs_md/ # Documentation in Markdown
    │  │  ├─ ...
    │  └─ ...
    ├─ docs/ # Code documentation in HTML
    │  └─...
    ├─ tmc/ # Folder for Python scripts and data
    │  │  ├─ tmc_utils/ # Utility scripts and helper functions
    │  │  │  ├─ __init__.py 			# Helper file
    │  │  │  ├─ article_scraper.py 		# Script for scraping articles
    │  │  │  ├─ clean_text.py 			# Text processing script
    │  │  │  └─ tor_initialization.py 	# Route requests through Tor
    │  ├─ __init__.py 		# Helper file
    │  ├─ data_viz_tools.py # Data visualization snippets
    │  ├─ dynamic_join.py 	# CSV file joiner
    │  └─ get_data.py 		# Script for obtaining data
    ├─ .gitignore
    ├─ README.md
    ├─ data_visualization.ipynb # Sample analysis
    ├─ mkdocs.yml
    └─ requirements.txt
