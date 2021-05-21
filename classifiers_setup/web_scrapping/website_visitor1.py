#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: enkeledabardhi
"""

import webbrowser
import time
#from pykeyboard import PyKeyboard
import requests
import re
import configuration
import random
#from bs4 import BeautifulSoup

class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    NONE = '\033[0m'


def debug_print(message, color=Colors.NONE):
    #A method which prints if DEBUG is set
    if configuration.DEBUG:
        print(color + message + Colors.NONE)

def make_request(url):
    # method used for loading web pages

    global data_meter
    global good_requests
    global bad_requests

    debug_print(" Request for page ".format(url))
    headers = {'user-agent': configuration.USER_AGENT}
    try:
        req = requests.get(url, headers = headers, timeout = 5)
        # if we want to open the web page on the browser
        #webbrowser.open(url, new=0)
        #close the page
        #PyKeyboard.press_keys(['Command','W'])

    except:
        # Prevent 100% CPU loop in a net down situation
        time.sleep(30)
        return False

    page_size = len(req.content)
    data_meter += page_size
    status = req.status_code

    if (status != 200):
        bad_requests += 1
        debug_print(" Response status: {}".format(req.status_code), Colors.RED)
        if (status == 429):
            debug_print(
                " Making too frequent requests, sleep longer")
            configuration.MIN_WAIT += 10
            configuration.MAX_WAIT += 10
    else:
        good_requests += 1

    debug_print("  Good requests: {}".format(good_requests), Colors.YELLOW)
    debug_print("  Bad requests: {}".format(bad_requests), Colors.YELLOW)

    return req

def get_links(page):

    # method used to get all links from a web page

    pattern = r"(?:href\=\")(http?:\/\/[^\"]+)(?:\")"
    links = re.findall(pattern, str(page.content))

    return links


def overall_visiting(url):

    debug_print("Recursively browsing [{}]".format(url))
    # method in order to first visit the homepage, and then visit links picked randomly with decrement depth
    web_page = make_request(url)
    if not web_page:
        debug_print("  Stopping: page error".format(url), Colors.YELLOW)
        return
    debug_print("  Scraping page {} for links".format(url), Colors.RED)
    links = get_links(web_page)
    debug_print(" Found {} links".format(len(links)), Colors.RED)

    # sleep and then recursively browse
    sleep_time = random.randrange(configuration.MIN_WAIT, configuration.MAX_WAIT)
    debug_print("  Pausing for {} seconds...".format(sleep_time))
    time.sleep(sleep_time)

    for one_link in links:
            debug_print("Browsing [{}] link from [{}] web page".format(one_link, url), Colors.PURPLE)
            make_request(one_link)

if __name__ == "__main__":

# global variables initialization
    data_meter = 0
    good_requests = 0
    bad_requests = 0

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Webpage visitor started working...")
    print(" The visitor is actually requesting between 2 and {} links deep into {} home page URLs".format(configuration.MAX_DEPTH, len(configuration.urls)))
    print("Range of wait between requests goes from {} to {}".format(configuration.MIN_WAIT, configuration.MAX_WAIT))
    print("Press Ctrl+C to exit the visitor.")

    while True:
        debug_print("Randomly selecting one of {} home page URLs".format(len(configuration.urls)), Colors.PURPLE)
        random_url = random.choice(configuration.urls)
        #found_links = get_links(random_url)
        #depth = random.choice(range(configuration.MIN_DEPTH, configuration.MAX_DEPTH))

        overall_visiting(random_url)
