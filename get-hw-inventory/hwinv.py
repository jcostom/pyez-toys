#!/usr/bin/env python

from jnpr.junos import Device
from jnpr.junos.op.inventory import ModuleTable
from jnpr.junos.exception import *
import json
import yaml

user = 'autobot'
password = 'juniper123'
vars = 'hosts.yml'

config = yaml.load(open(vars).read())


def main():
    hosts = config.get('hosts')

    for host in hosts:
        dev = Device(host=host, user=user, password=password)
        try:
            dev.open()
        except Exception as err:
            print "Cannot connect to device:", err
            return
        print "System: {} / {} / {}" \
            .format(host, dev.facts['model'], dev.facts['serialnumber'])
        print (json.dumps(ModuleTable(dev).get().items(), sort_keys=False,
                          indent=4, separators=(',', ': ')))
        # print (yaml.dump(ModuleTable(dev).get().items()))
        dev.close()


if __name__ == "__main__":
    main()
