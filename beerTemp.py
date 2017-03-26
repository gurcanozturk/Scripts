#!/usr/bin/python
# Script for reading temperature and sending notification if temperature low or high for beer brewing.
# A.Gurcan OZTURK, gurcan@gurcanozturk.com, 03/2017

import urllib2
import time
import os
import subprocess
import logging

logging.basicConfig(filename="/var/log/beertemp.log", level=logging.INFO)
simdi = time.strftime("%Y/%m/%d-%H:%M:%S")

p = subprocess.Popen(["/usr/local/bin/pcsensor", "-c"], stdout=subprocess.PIPE)
output, err = p.communicate()
beerTemp = output.split()[-1]
degree   = int(beerTemp.split('.')[0])
notify_url = "http://google.com/beertemp?title=Bira+yaniyor+(%s)&note=Bira+Sicakligi:+%s" % (simdi, beerTemp)
log_msg    = "Su an: %s - Bira Sicakligi: %s" % (simdi, beerTemp)

print beerTemp
if (degree <= 16 or degree >= 25):
	request = urllib2.urlopen(notify_url).read()
	logging.warning(log_msg)
else:
	logging.info(log_msg)
