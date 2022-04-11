#!/usr/bin/env python3

# You ever need to bounce a port on a switch, but don't
# want to, or just plain can't walk up to the switch
# and pull a cable out? Don't feel like doing the
# disable/commit/enable/commit dance manually?
# This does the work for you.
# Yes, you could also drop to a root shell and
# use ifconfig, but JTAC might give you stern looks
# for doing that.

import argparse
import os
import logging
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# Setup logger
logger = logging.getLogger()
ch = logging.StreamHandler()
logger.setLevel(logging.INFO)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

parser = argparse.ArgumentParser(
    description='Juniper Switch Port Bounce Utility'
)

parser.add_argument('--switch', action="store")
parser.add_argument('--port', action="store")
parser.add_argument('--user', action="store",
                    default=os.getenv('USER'),
                    help="Will default to your current username.")
parser.add_argument('--password', action="store", help="Omit this option if you're using ssh keys to authenticate")  # noqa: E501
args = parser.parse_args()


def main():
    disableCommand = " ".join(
        ["set interfaces", args.port, "disable"]
    )
    disableComment = " ".join(
        ["shut port", args.port]
    )
    rollbackComment = " ".join(
        ["rollback shut of port", args.port]
    )

    dev = Device(host=args.switch, user=args.user)
    logger.info("Connecting to: {}".format(args.switch))
    dev.open()
    dev.bind(cu=Config)
    logger.info("Locking the configuration on: {}".format(args.switch))
    dev.cu.lock()
    logger.info("Now shutting port: {}".format(args.port))
    dev.cu.load(disableCommand, format='set')
    dev.cu.commit(comment=disableComment, timeout=180)
    logger.info("Now executing rollback on: {}".format(args.switch))
    dev.cu.rollback(rb_id=1)
    dev.cu.commit(comment=rollbackComment, timeout=180)
    logger.info("Unlocking the configuration on: {}".format(args.switch))
    dev.cu.unlock()
    dev.close()
    logger.info("Done!")


if __name__ == "__main__":
    main()
