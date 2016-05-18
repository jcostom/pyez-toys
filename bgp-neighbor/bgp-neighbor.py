#!/usr/bin/env python

# Based (heavily) on the work of @macrujugl
# https://github.com/macrujugl/pyez

from jnpr.junos.factory import loadyaml
from jnpr.junos import Device
from jnpr.junos.exception import *

host = 'srx1'
user = 'autobot'
password = 'juniper123'
yamlfile = 'bgp_table.yml'

def main():
    globals().update(loadyaml(yamlfile))
    dev = Device(host=host, user=user, password=password)
    try:
        dev.open()
    except Exception as err:
        print "Cannot connect to device:", err
        return

    peerTable = bgpNeighbor(dev)
    peerTable.get()
    for peer in peerTable:
        #print peer.items()
        #print "-----"
        #print
        peerDict = dict(peer)
        print "Neighbor: {}:{}".format(peerDict["neighbor"], peerDict["peer-as"])
        print "    Description: {}".format(peerDict["description"])
        print "    State: {}".format(peerDict["state"])
        print "    RIB: {}".format(peerDict["rib-name"])
        print "    Stats:"
        print "        Accepted Prefixes: {}".format(peerDict["accepted-prefix"])
        print "        Suppressed Prefixes: {}".format(peerDict["suppressed-prefix"])
        print "        Active Prefixes: {}".format(peerDict["active-prefix"])
        print "        Received Prefixes: {}".format(peerDict["received-prefix"])
        print

    dev.close()

if __name__ == "__main__":
    main()
