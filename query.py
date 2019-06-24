#!/usr/bin/env python3
#             _                       ____
#  _   _ _ __| |___  ___ __ _ _ __   |  _ \ _ __ ___
# | | | | '__| / __|/ __/ _` | '_ \  | |_) | '__/ _ \
# | |_| | |  | \__ \ (_| (_| | | | | |  __/| | | (_) |
#  \__,_|_|  |_|___/\___\__,_|_| |_| |_|   |_|  \___/
# 
# urlscan Pro Python API - (c) 2019 by Johannes Gilger - Web Security

from gevent import monkey
monkey.patch_all()
import gevent

import argparse
import requests
import arrow
import logging
import sys
from pydash import _
import pprint
pp = pprint.PrettyPrinter(indent=2)

session = requests.Session()

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="urlscan Pro API get")
parser.add_argument("action", type=str, default="showbrands", help="Action to perform: showbrands or showlatest")
parser.add_argument("--apikey", type=str, default="", help="API-Key for urlscan Pro", required=True)

parser.add_argument("--brand", type=str, default="all", help="Brand name")
parser.add_argument("--limit", type=int, default=10, help="Return at most this many results")

parser.add_argument("--since", type=str, default="7d", help="Show phishing pages detected in the last minutes (m), hours (h), days (d), weeks (w), months (M)")
args = parser.parse_args()

session.headers.update({'api-key': args.apikey})

query = "*"
if args.since:
    query = "date%%3A>now-%s" % args.since

if args.action == "showbrands":
    r = session.get("https://pro.urlscan.com/api/v1/pro/kits")
    if not r.status_code == requests.codes.ok:
        logging.error("Error fetching brand definitions: %s" % r.json())
        sys.exit(1)
    for kit in r.json()["kits"]:
        print("="*80)
        print("%s - %s (%s)\nKey: %s\nWhitelisted domains: %s" % (
            kit["name"],
            _.head(_.get(kit, "vertical", [])),
            _.head(_.get(kit, "country", [])),
            kit["key"],
            _.get(kit, "terms.domains", [])
        ))
        print("URL: https://pro.urlscan.com/search?filter=%%24phishing_%s" % kit["key"])
        print("API: https://pro.urlscan.com/api/v1/pro/search?filter=%%24phishing_%s" % kit["key"])
elif args.action == "showlatest":
    r = session.get("https://pro.urlscan.com/api/v1/pro/search?q=%s&filter=$phishing_%s&size=%d" % (query, args.brand, args.limit))
    print("\nSearching for brand '%s' with query '%s' and limit '%d'" % (args.brand, query, args.limit))
    print("Show in Pro: https://pro.urlscan.com/search?query=%s&filter=$phishing_%s" % (query, args.brand))
    if not r.status_code == requests.codes.ok:
        logging.error("Error fetching brand definitions: %s" % r.json())
        sys.exit(1)
    print("%d/%d results returned\n\n" % (len(r.json()["results"]), r.json()["total"]))
    for res in r.json()["results"]:
        print("="*80)
        print("Submitted URL: %s" % _.get(res, "task.url"))
        print("Actual URL: %s" % _.get(res, "page.url"))
        print("Submitted: %s via %s" % (_.get(res, "task.time"), _.get(res, "task.method")))
        print("Page IP: %s - %s (%s)" % (_.get(res, "page.ip"), _.get(res, "page.asn"), _.get(res, "page.asnname")))
        print("Scan: https://urlscan.io/result/%s/" % res["_id"])
        print("API: https://urlscan.io/api/v1/result/%s/" % res["_id"])
        print("")

        #pp.pprint(res)
else:
    logging.error("Unknown command '%s', quitting..." % args.action)
    sys.exit(1)
