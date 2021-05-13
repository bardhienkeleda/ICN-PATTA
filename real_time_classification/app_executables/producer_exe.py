#!/usr/bin/env python2

import logging
import os
import string
import sys

from pprint import pprint
from urllib import unquote
from numpy import random
from itertools import cycle
from random import choice

from argparse import ArgumentParser
from pyndn import Interest, Face, Name, MetaInfo, NetworkNack, Data
import pandas as pd

from pyndn.security import KeyChain
from pyndn.threadsafe_face import ThreadsafeFace

try:
	import asyncio
except ImportError:
	import trollius as asyncio

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(levelname)s [%(name)s] %(message)s")

Interest.setDefaultCanBePrefix(True)

ALPHABET = string.ascii_lowercase + string.digits

SERVER_RESTART_TIMEOUT = 5000.0  # ms
FRESHNESS_PERIOD = 10000.0  # ms

def rand_string(length):
    return ''.join([choice(ALPHABET) for _ in range(length)])

if __name__ == '__main__':

    log = logging.getLogger("app:main")
    arg_parser = ArgumentParser()

    arg_parser.add_argument("-p", "--prefix", type=str, default="", help="Prefix for all requests")
    arg_parser.add_argument("-rf", "--requestsFile", type=str, help="File containing the requests")
    arg_parser.add_argument("-f", "--freshness", type=float, default=FRESHNESS_PERIOD, help="Data packet freshness in ms")
    args = arg_parser.parse_args()
    log.info(args)

    requests = pd.read_csv(args.requestsFile)["Full request URI"]

    # read domain according to number of producers and index of producers
    domain = None
    if args.requestsFile is not None:
        domain = ["/%s/%s" % (args.prefix.strip("/"), d.lstrip("/")) for d in requests]
        domain = set(domain)
        log.info("Domain size: %d" % len(domain))

    loop = asyncio.get_event_loop()
    face = ThreadsafeFace(loop)

    keyChain = KeyChain()
    face.setCommandSigningInfo(keyChain, keyChain.getDefaultCertificateName())

    def onRegisterSuccess(prefix, *k):
        log.info("%s listening on %s" % (log.name, prefix))
        pass


    def onRegisterFailed(prefix, *k):
        log.error("Failed to register prefix %s" % prefix)
        loop.call_later(
            SERVER_RESTART_TIMEOUT / 1000.0,
            face.registerPrefix,
            prefix,
            onInterest,
            onRegisterFailed,
            onRegisterSuccess)

    def onInterest(prefix, interest, *k):
        should_respond = True

        if domain is not None:
            should_respond = False
            target = unquote(str(interest.getName().toUri()))
            log.info("Target is %s" % target)
            if target in domain:
                should_respond = True

        if should_respond:
            content = rand_string(10)
            data = Data(interest.getName())
            meta = MetaInfo()
            meta.setFreshnessPeriod(args.freshness)
            data.setMetaInfo(meta)
            data.setContent(content)
            keyChain.sign(data, keyChain.getDefaultCertificateName())
            face.putData(data)
            log.info("Replied to %s" % interest.getName())
        else:
            nack = NetworkNack()
            nack.setReason(NetworkNack.Reason.NO_ROUTE)
            face.putNack(interest=interest, networkNack=nack)

    face.registerPrefix(
        Name(args.prefix), onInterest,
        onRegisterFailed, onRegisterSuccess)

    try:
    	loop.run_forever()

    except SystemExit:
    	print("Caught SystemExit...")
    	raise
        #sys.exit("Ok, bye!")
    finally:
    	loop.close()
