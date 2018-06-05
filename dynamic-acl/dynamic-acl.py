#!/usr/bin/env python3

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
import yaml

user = 'autobot'
password = 'juniper123'
template = 'acl.j2'
vars = 'acl.yml'

config = yaml.load(open(vars).read())


def main():
    hosts = config.get('hosts')

    for host in hosts:
        dev = Device(host=host, user=user, password=password)
        # Open the connection & config
        try:
            print("Opening connnection to: {}".format(host))
            dev.open()
        except Exception as err:
            print("Cannot connect to device: {}".format(err))
            return
        dev.bind(cu=Config)
        # Lock the configuration, load changes, commit
        print("Locking the configuration on: {}".format(host))
        try:
            dev.cu.lock()
        except LockError:
            print("Error: Unable to lock configuration on: {}".format(host))
            dev.close()
            return
        print("Loading configuration changes on: {}".format(host))
        try:
            set_commands = """
            delete policy-options prefix-list edge-block
            delete policy-options prefix-list edge-block-exceptions
            """
            dev.cu.load(set_commands, format='set')
            dev.cu.load(template_path=template,
                        template_vars=config, format='text')
        except ValueError as err:
            print(err.message)
        except Exception as err:
            if err.rsp.find('.//ok') is None:
                rpc_msg = err.rsp.findtext('.//error-message')
                print("Unable to load config changes: {}".format(rpc_msg))
            print("Unlocking the configuration on: {}".format(host))
            try:
                dev.cu.unlock()
            except UnlockError:
                print("Error: Unable to unlock config on: {}".format(host))
            dev.close()
            return
        print("Committing the configuration on: {}".format(host))
        try:
            dev.cu.commit()
            # print(dev.cu.diff())
        except CommitError:
            print("Error: Unable to commit configuration on: {}".format(host))
            print("Unlocking the configuration on: {}".format(host))
            try:
                dev.cu.unlock()
            except UnlockError:
                print("Error: Unable to unlock config on: {}".format(host))
            dev.close()
            return
        print "Unlocking the configuration on:", host
        try:
            dev.cu.unlock()
        except UnlockError:
            print("Error: Unable to unlock config on: {}".format(host))
        print("Closing connection to: {}".format(host))
        dev.close()


if __name__ == "__main__":
    main()
