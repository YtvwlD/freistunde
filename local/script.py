#!/usr/bin/env python3

REMOTE_URL = "https://pub.ytvwld.de/freistunde/" # change later on
INTERVAL = 15*60 # 15 min

# Copyright © 2017 Niklas Sombert <niklas@ytvwld.de>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

from socket import getfqdn
from requests import Session
import asyncio

loop = asyncio.get_event_loop()
requests = Session()

def run():
    print("Checking... ", end="")
    if "chaosdorf.dn42" in getfqdn():
        result = True
    else:
        result = False
    print("...result: {}. Sending... ".format(result), end="")
    try:
        r = requests.post(REMOTE_URL, json={"value": result})
        r.raise_for_status()
        print("...sending successful.")
        loop.call_later(INTERVAL, run)
    except Exception as exc:
        print("...sending failed: {} Retrying soon.".format(exc))
        loop.call_later(20, run)

loop.call_soon(run)

print("Running.")
print("Please press ^C to quit.")

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("\nExiting...")
    loop.stop()
    loop.close()
