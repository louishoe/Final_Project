import pandas as pd
import requests
import threading
import time
import concurrent.futures
import urllib.request


URLS = 'https://coinmarketcap.com/'


results = []


def html_table(url):
    data = pd.read_html(requests.get(url).content)[0]
    results.append(data)
    return data

results = html_table(URLS)
results