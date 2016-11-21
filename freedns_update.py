#!/usr/bin/env python
#
# Dynamic DNS update script for freedns.afraid.org
# Gets public IP and update DNS record on freedns.afraid.org
# and notifies via pushingbox.com
# A.Gurcan OZTURK, gurcan@gurcanozturk.com, 02/2014

# UPDATE_KEY = Update key for DNS record on freedns.afraid.org 
# DEVID      = Device ID from pushingbox.com

import urllib2
import time
import os

update_key    = "<UPDATE_KEY>"
devid         = "<DEVID>"
oldipfile     = "/var/lib/misc/oldip"
simdi         = time.strftime("%Y%m%d-%H%M%S")

public_ip_url = "http://ip.dnsexit.com"
public_ip     = urllib2.urlopen(public_ip_url).read().strip()

notify_url    = "http://api.pushingbox.com/pushingbox?devid=%s&ext_ip=%s&saat=%s" % (devid, public_ip, simdi)
update_url    = "http://freedns.afraid.org/dynamic/update.php?%s" % (update_key)

if not os.path.isfile(oldipfile) :
        with open(oldipfile, "a") as myfile:
                myfile.write("0.0.0.0")

with open (oldipfile, "r") as myfile:
    oldip=myfile.read().replace('\n', '')

if public_ip != oldip :
    urllib2.urlopen(update_url).read()
    urllib2.urlopen(notify_url).read()

    with open(oldipfile, "w") as myfile:
     myfile.write(public_ip)
