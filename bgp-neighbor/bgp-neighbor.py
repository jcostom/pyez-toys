#!/usr/bin/env python

# Based (heavily) on the work of @macrujugl
# https://github.com/macrujugl/pyez

from jnpr.junos.factory import loadyaml
from jnpr.junos import Device

host = 'srx1'
user = 'autobot'
password = 'juniper123'
yamlfile = 'bgp_table.yml'

def main():
    globals().update(loadyaml(yamlfile))
    dev = Device(host=host, user=user, password=password)
    dev.open()
    peerTable = bgpNeighbor(dev)
    peerTable.get()
    for peer in peerTable:
        print peer.items()

    dev.close()

if __name__ == "__main__":
    main()
