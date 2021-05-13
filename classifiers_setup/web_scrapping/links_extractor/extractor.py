#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from urllib.parse import urlparse
import csv
import configuration
import tldextract

"""
Methods used to get all links from a certain page.
"""
def getLinks(url):

    headers = {'user-agent': configuration.USER_AGENT}
    req = requests.get(url, headers = headers, timeout = 5)

    pattern = r"(?:href\=\")(http?:\/\/[^\"]+)(?:\")"
    links = re.findall(pattern, str(req.content))

    return links

def write_to_csv(links, url):
    root = 'extractedFiles'
    parse = tldextract.extract(url)
    if parse.domain in configuration.domains:
        name = parse.domain
    #name = urlparse(url).netloc
    #name = name.replace(".", "")

    with open(root + '/' + name + '.csv', 'w') as csvfile:
        #csvwriter = csv.writer(csvfile)
        for link in links:
            csvfile.write(link)
            csvfile.write('\n')

if __name__ == "__main__":

    print("Link extractor program is running...")

    for pick_url in configuration.urls:
        print("Opening [{}]".format(pick_url))
        print("Scraping for links on [{}]".format(pick_url))

        retreivedLinks = getLinks(pick_url)
        print("Found {} links for this website".format(len(retreivedLinks)))

        if len(retreivedLinks) is not 0:
            write_to_csv(retreivedLinks, pick_url)
