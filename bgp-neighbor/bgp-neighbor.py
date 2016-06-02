#!/usr/bin/env python

# Based (heavily) on the work of @macrujugl
# https://github.com/macrujugl/pyez
# 

from jnpr.junos.factory import loadyaml
from jnpr.junos import Device
from jnpr.junos.exception import *

host = 'srx1'
user = 'autobot'
password = 'juniper123'
yamlfile = 'bgp_table-op.yml'

def main():
    globals().update(loadyaml(yamlfile))
    dev = Device(host=host, user=user, password=password)
    try:
        dev.open()
    except Exception as err:
        print "Cannot connect to device:", err
        return

    peerTable = BgpNeighborTable(dev)
    peerTable.get()
    for entry in peerTable:
        #print peer.items()
        #print "-----"
        #print
        peer = dict(entry)
        print "Neighbor: {}:{}".format(peer["peer-address"], peer["peer-as"])
        print "    Description: {}".format(peer["description"])
        print "    State: {}".format(peer["peer-state"])
        print "    RIB: {}".format(peer["rib-name"])
        print "    Stats:"
        print "        Accepted Prefixes: {}".format(peer["accepted-prefix"])
        print "        Suppressed Prefixes: {}".format(peer["suppressed-prefix"])
        print "        Active Prefixes: {}".format(peer["active-prefix"])
        print "        Received Prefixes: {}".format(peer["received-prefix"])
        print

    dev.close()

if __name__ == "__main__":
    main()
