import requests
import tmc_utils.tor_initialization as ti
import tmc_utils.article_scraper as arts


# %%
# Test whether TOR works
ti.initiate_tor()
tor_request = ti.get_tor_session()
print("Tor IP:", tor_request.get("http://httpbin.org/ip", timeout=30).text)
print("Actual IP:", requests.get("http://httpbin.org/ip", timeout=30).text)

# %%
# Dummy request and parse HTML
sample_url = "https://www.idnes.cz/zpravy/zahranicni/koronavirus.K466979/182"
soup = arts.soup_object_tor(sample_url, tor_request)


# %%
# Do not persist at this point. Persist cleaned text (stemmed etc.) later
catalog = arts.generate_article_df(soup)

# %%
# Add article content
cat_and_artcls = arts.add_content(catalog, tor_request)

# %%
ti.kill_tor_process()
