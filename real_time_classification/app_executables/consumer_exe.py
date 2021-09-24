#!/usr/bin/env python

import logging
import os
import time
import sys
from pprint import pprint
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote
from numpy import random
from itertools import cycle

from argparse import ArgumentParser
from pyndn import Interest, Face, Name
import pandas as pd
import numpy as np

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(levelname)s [%(name)s] %(message)s"
)

Interest.setDefaultCanBePrefix(False)

if __name__ == '__main__':

    log = logging.getLogger("app:main")

    arg_parser = ArgumentParser()

    arg_parser.add_argument("-p", "--prefixes", type=str, nargs="*",help="Prefix for all requests")  # -p /www.bu.edu/
    arg_parser.add_argument("-rf", "--requestsFile", type=str, help="File containing the requests") # -rd domain_list_unique_def.csv
    arg_parser.add_argument("-l", "--length", type=int, help="Max name length")  # -l 200
    arg_parser.add_argument("-a", "--alpha", type=float, help="Alpha parameter for Zipf distribution")
    arg_parser.add_argument("-sr", "--sendingRate", type=float, help="Consumer's sending rate interval") # from 1.0 to 25.0
    arg_parser.add_argument("--info", action="store_true", help="Only print dataset info")  # --info
    arg_parser.add_argument("--dry", action="store_true", help="Only print requests")  # --dry

    args = arg_parser.parse_args()

    # read csv and drop repetitions
    requests = pd.read_csv(args.requestsFile, keep_default_na=False)["Full request URI"]


    if args.prefixes is not None:
        pref = args.prefixes
        l_pref = len(args.prefixes)
        requests = ["/%s/%s" % (pref.strip("/"), r.lstrip("/"))
                    for pref, r in zip(cycle(args.prefixes), requests)]

    if args.info:
        print("Content domain: %d" % len(requests))
        pprint(requests[:5])
        print("...")
        pprint(requests[-6:-1])
        exit(0)

    frequency = None
    if args.alpha:
        n = len(requests)
        x = np.arange(1, n + 1)
        a = args.alpha
        frequency = x ** (-a)
        frequency /= frequency.sum()

    face = Face()

    def send_request(name):
        if args.length is not None:
            name = name.getPrefix(args.length)
        if args.dry:
            log.info("Dry: %s" % unquote(name.toUri()))
            return
        interest = Interest() \
            .setMustBeFresh(False) \
            .setCanBePrefix(True) \
            .setInterestLifetimeMilliseconds(5000.0) \
            .setName(name)

        req_time = time.time()

        face.expressInterest(
            interest,
            lambda intr, data: log.info(
                "%.5f [%.5f] Data: %s -> %s" % (
                    time.time(), time.time() - req_time,
                    unquote(intr.getName().toUri()), data.content.toRawStr())))
            #lambda i: log.warning("Timeout: %s" %
            #                     unquote(i.getName().toUri()))
            #lambda i, n: log.warning("NACK: %s" % unquote(i.getName().toUri())))

    def iter_requests():
        #log.info("Requests domain {}".format(requests))
        already_req_names = []
        while True:
            valid_name = False
            while not valid_name:
                content_name = Name(str(random.choice(requests, replace=False, p=frequency))) #,
                if content_name not in already_req_names:
                    already_req_names.append(content_name)
                    valid_name = True
                #log.info(time.time())
            send_request(content_name)
            face.processEvents()
            time.sleep(args.sendingRate)


    # Run client and check for exceptions
    try:
        iter_requests()
    except (KeyboardInterrupt, SystemExit):
        face.shutdown()
        sys.exit("Ok, exited")

    print("Completed!")
