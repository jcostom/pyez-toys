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
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

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
        ("set interfaces", args.port, "disable")
    )
    disableComment = " ".join(
        ("shut port", args.port)
    )
    rollbackComment = " ".join(
        ("rollback shut of port", args.port)
    )

    dev = Device(host=args.switch, user=args.user)
    print("Connecting to: {}".format(args.switch))
    dev.open()
    dev.bind(cu=Config)
    print("Locking the configuration on: {}".format(args.switch))
    dev.cu.lock()
    print("Now shutting port: {}".format(args.port))
    dev.cu.load(disableCommand, format='set')
    dev.cu.commit(comment=disableComment, timeout=180)
    print("Now executing rollback on: {}".format(args.switch))
    dev.cu.rollback(rb_id=1)
    dev.cu.commit(comment=rollbackComment, timeout=180)
    print("Unlocking the configuration on: {}".format(args.switch))
    dev.cu.unlock()
    dev.close()
    print("Done!")


if __name__ == "__main__":
    main()
