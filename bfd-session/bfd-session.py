#!/usr/bin/env python

# Connects to a given router, pulls BFD sessions, presents in a pretty way.

from jnpr.junos import Device
from jnpr.junos.exception import *
from jnpr.junos.op.bfd import BfdSessionTable

host = 'srx1'
user = 'autobot'
password = 'juniper123'


def main():
    dev = Device(host=host, user=user, password=password)
    try:
        dev.open()
    except Exception as err:
        print "Cannot connect to device:", err
        return

    bfdTable = BfdSessionTable(dev)
    bfdTable.get()
    for entry in bfdTable:
        # print bfd.items()
        # print "-----"
        # print
        bfd = dict(entry)
        print "Neighbor: {}".format(bfd["neighbor"])
        print "    Interface: {}".format(bfd["interface"])
        print "    Local/Remote State: {} / {}".format(bfd["state"], bfd["remote_state"])
        print "    Hello/Detection Timers: {}ms / {}s".format(int(float(bfd["transmission_interval"])*1000), bfd["detection_time"])
        print "    Detection Multiplier: {}".format(bfd["detection_multiplier"])
        print "    Echo Mode Desired/State: {} / {}".format(bfd["echo_mode_desired"], bfd["echo_mode_state"])
        print

    dev.close()

if __name__ == "__main__":
    main()
