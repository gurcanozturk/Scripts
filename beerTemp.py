#!/usr/bin/python
# Script to read temperature from DSB1820 temperature sensor and send notification in case temperature low or high to beer brewing.
# mySQL db used to store historical data and Domoticz used to draw graphs and trends.
# A.Gurcan OZTURK, gurcan@gurcanozturk.com, 03/2017

#!/usr/bin/python

import os                                                  # import os module
import glob                                                # import glob module
import time                                                # import time module
import urllib2
import subprocess
import logging
import MySQLdb
import base64
from math import trunc

os.system('modprobe w1-gpio')                              # load one wire communication device kernel modules
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'                          # point to the address
device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from 28*
device_file = device_folder + '/w1_slave'                  # store the details

logging.basicConfig(filename="/var/log/beertemp.log", level=logging.INFO)
simdi = time.strftime("%Y/%m/%d-%H:%M:%S")

def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()                                   # read the device details
   f.close()
   return lines

def read_temp():
   lines = read_temp_raw()
   while lines[0].strip()[-3:] != 'YES':                   # ignore first line
      time.sleep(0.2)
      lines = read_temp_raw()
   equals_pos = lines[1].find('t=')                        # find temperature in the details
      if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0                 # convert to Celsius
      #temp_f = temp_c * 9.0 / 5.0 + 32.0                  # convert to Fahrenheit
      #return temp_c, temp_f
      return temp_c


beerTemp = read_temp()
username = 'domoticz_admin'
password = 'domoticz_password'
domoticz_url = "http://localhost:8080/json.htm?type=command&param=udevice&idx=7&nvalue=0&svalue=" + str(beerTemp)
request = urllib2.Request(domoticz_url)
request.add_header('Authorization', b'Basic ' + base64.b64encode(username + b':' + password))
result = urllib2.urlopen(request)

log_msg      = "%s - Bira Sicakligi: %s" % (simdi, beerTemp)
logging.warning(log_msg)

connection = MySQLdb.connect(host="localhost", user="dbUser", passwd="dbPassword", db="dbName")
cursor = connection.cursor()

try:
   cursor.execute("""INSERT INTO tblName (temperature) VALUES (%s)""",(beerTemp))
   connection.commit()
except:
   connection.rollback()

connection.close()


if  beerTemp <= 16 or beerTemp >= 25:
    notify_url = "https://notification_url_here/?title=Bira+Sicakligi&note=Bira+Sicakligi:%s" % (beerTemp)
    request    = urllib2.urlopen(notify_url).read()
