#!/usr/bin/env python3

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from jinja2 import Template
from requests import get
import sys

# If testing, you can feed IP on the CLI as an arg, or you could always
# determine it on the fly with the 2 lines belowself.

# myip = get('http://ipv4.icanhazip.com/').text.rstrip()
myip = sys.argv[1]

user = 'autobot'
password = 'juniper123'
host = 'router1'
vars = {'ip': myip}

# Hurrican Electric Tunnel Info
he_user = 'heuser'
he_pass = 'hepass'
he_tunnelid = 'tunnelid'

# Prepare J2 Template
template = """
interfaces {
    ip-0/0/0 {
        unit 0 {
            tunnel {
                source {{ ip }};
            }
        }
    }
}
"""
j2_template = Template(template)


def main():
    dev = Device(host=host, user=user, password=password)
    try:
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
        dev.cu.load(template=j2_template,
                    template_vars=vars, format='text', merge=True)
    except ValueError as err:
        print(err.message)
    except Exception as err:
        if err.rsp.find('.//ok') is None:
            rpc_msg = err.rsp.findtext('.//error-message')
            print("Unable to load config changes: {}".format(rpc_msg))

        print("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError:
            print("Error: Unable to unlock configuration")
        dev.close()
        return
    print("Committing the configuration on: {}".format(host))
    try:
        dev.cu.commit()
        # print dev.cu.diff()
    except CommitError:
        print("Error: Unable to commit configuration")
        print("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError:
            print("Error: Unable to unlock configuration")
        dev.close()
        return

    print("Unlocking the configuration")
    try:
        dev.cu.unlock()
    except UnlockError:
        print("Error: Unable to unlock configuration")

    dev.close()

    # Update HE Tunnel
    he_url = "https://ipv4.tunnelbroker.net/nic/update?username=" + he_user + \
        "&password=" + he_pass + "&hostname=" + he_tunnelid + \
        "&myip=" + myip
    he_update = get(he_url).text
    print(he_update)


if __name__ == "__main__":
    main()
