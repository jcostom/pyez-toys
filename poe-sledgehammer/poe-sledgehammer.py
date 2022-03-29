#!/usr/bin/env python3

# This tool is a blunt instrument - HANDLE WITH CARE.
# It disables PoE on all ports, commits the configuration,
# then executes a rollback 1 and commits again.
# You would only use this tool if you wanted to completely
# disable PoE then rollback that change.

import argparse
import os
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

parser = argparse.ArgumentParser(
    description='Juniper Switch PoE Bounce Utility'
)

parser.add_argument('--switch', action="store")
parser.add_argument('--user', action="store",
                    default=os.getenv('USER'),
                    help="Will default to your current username.")
parser.add_argument('--password', action="store", help="Omit this option if you're using ssh keys to authenticate")  # noqa: E501
args = parser.parse_args()


def main():
    disableCommand = "set poe interface all disable"
    disableComment = "drop the PoE sledgehammer on all ports"
    rollbackComment = "rollback - restoring PoE"

    dev = Device(host=args.switch, user=args.user)
    print("Connecting to: {}".format(args.switch))
    dev.open()
    dev.bind(cu=Config)
    print("Locking the configuration on: {}".format(args.switch))
    dev.cu.lock()
    print("Now shutting down PoE on all ports: {}".format(args.port))
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
