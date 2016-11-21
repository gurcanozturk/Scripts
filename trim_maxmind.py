#!/usr/bin/env python
# Truncates ISP/Organization field to 30 chars in Maxmind's GeoIP-ISP DB file (GeoIP-142)
# for NetScaler GeoIP check mechanism. (NetScaler fails if ISP field greater than 32 character)
# A. Gurcan OZTURK, gurcan@gurcanozturk.com, Sep 2015

import sys
import csv
import re
import string
import argparse

parser = argparse.ArgumentParser(usage='%(prog)s -i <input_file> -o <output_file> [-h]')
parser.add_argument('-i','--input-file', help='GeoIP DB file to process', required=True)
parser.add_argument('-o','--output-file', help='GeoIP DB output file', required=True)

if len(sys.argv) < 2:
  parser.print_usage()
  sys.exit(1)
else:
  args = parser.parse_args()

input_file  = args.input_file
output_file = args.output_file

ofile  = open(output_file, "w")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

count = 0
array = []
with open(input_file, 'rb') as f:
    reader = csv.reader(f, delimiter=',')

    line_count = 0
    for row in reader:
        count +=1
        m = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', row[0])

        if m is not None:
            beginIP  = row[0]
            finishIP = row[1]
            country  = row[2]
            isp      = row[3][:30]

            writer.writerow((beginIP,finishIP,country,isp))
            line_count += 1
        else:
            array.append(row)

ofile.close()

if count != line_count:
    print "Input file %s file has %s lines" % (input_file, count)
    print "Output file %s file has %s lines" % (output_file, line_count)
    print "\r"
    print "Excluded lines:"
    for line in array:
        print line
