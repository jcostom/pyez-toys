#!/usr/bin/env python3

from jnpr.junos import Device
from jnpr.junos.op.inventory import ModuleTable
from jnpr.junos.exception import *
import json
import yaml

user = 'autobot'
password = 'juniper123'
vars = 'hosts.yml'

config = yaml.load(open(vars).read(), Loader=yaml.FullLoader)


def main():
    hosts = config.get('hosts')

    for host in hosts:
        dev = Device(host=host, user=user, password=password)
        try:
            dev.open()
        except Exception as err:
            print("Cannot connect to device: {}".format(err))
            return
        print("System: {} / {} / {}"
              .format(host, dev.facts['model'], dev.facts['serialnumber']))
        # Pretty output
        # print(json.dumps(ModuleTable(dev).get().items(), sort_keys=False,
        #       indent=4, separators=(',', ': ')))
        # Dense output
        print(json.dumps(ModuleTable(dev).get().items()))
        dev.close()


if __name__ == "__main__":
    main()
