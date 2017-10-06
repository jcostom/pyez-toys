# Automated Network Edge Filter for Junos
Rid yourself of annoying traffic across many systems in a snap.

## The problem? Nuisance traffic.

Got someone beating on your door trying the same attack over and over and over?  Someone who thinks it's fun to run nmap scans all day against your network? Dump their traffic with a simple firewall filter at the edge.

## How to make this work

### Step 1: Create 2 prefix-lists on your system.  

First is the `edge-block` prefix-list, which is your set of blocked IP addresses or subnets. Second is `edge-block-exceptions`, your list of exceptions to the edge-block prefix-list.
```
{master:0}
user@router> show configuration policy-options
prefix-list edge-block {
    1.1.1.0/24;
    2.2.2.0/24;
    3.3.3.0/24;
}
prefix-list edge-block-exceptions {
    1.1.1.1/32;
    2.2.2.2/32;
    3.3.3.3/32;
}
```
### Step 2: Create a firewall filter.  

It's going to be super simple.  Essentially, it says, "drop everything to & from the blocked list, apart from the exceptions list, and allow all else."  You can (obviously) customize this to your heart's content, but this is the minimum you'll need.
```
user@router> show configuration firewall family inet
filter internet-edge-block {
    term 1 {
        from {
            prefix-list {
                edge-block;
                edge-block-exceptions except;
            }
        }
        then {
            count blocked;
            syslog;
            discard;
        }
    }
    term 2 {
        then accept;
    }
}
```
### Step 3. Apply this filter to your external-facing interface.

Our example assumes you're using ge-0/0/0 as your external-facing interface.
```
user@router> show configuration interfaces ge-0/0/0
description "Peering: ISP1";
unit 0 {
    family inet {
        filter {
            input internet-edge-block;
        }
        address X.Y.Z.2/30;
    }
}
```
### Step 4: Edit the included YAML file (acl.yml).

It should be pretty self-explanatory how to maintain the info contained therein.

### Step 5: Use the dynamic-acl.py script to push updates out.

Change the YAML file to:

* Add/change hosts
* Add/remove blocked IPs/subnets
* Add/remove exceptions to block list
