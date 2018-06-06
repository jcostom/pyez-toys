#!/usr/bin/env python3

# Based (heavily) on the work of @macrujugl
# https://github.com/macrujugl/pyez

from jnpr.junos.factory import loadyaml
from jnpr.junos import Device
from jnpr.junos.exception import *
import yaml

user = 'autobot'
password = 'juniper123'
yamlfile = 'bgp_table-op.yml'
vars = 'routers.yml'

config = yaml.load(open(vars).read())


def main():
    globals().update(loadyaml(yamlfile))
    hosts = config.get('hosts')

    for host in hosts:
        dev = Device(host=host, user=user, password=password)
        try:
            dev.open()
        except Exception as err:
            print("Cannot connect to device: {}".format(err))
            return

        peerTable = BgpNeighborTable(dev)
        peerTable.get()
        for entry in peerTable:
            print(entry.items())
            print("-----")
            print()

        dev.close()


if __name__ == "__main__":
    main()
