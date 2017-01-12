#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple python script to send message to hipchat room with color
# Gurcan Ozturk, gurcan@gurcanozturk.com, 2015
# You have to get ROOM_ID and AUTH_TOKEN from HipChat group admin site.
# Example : sendMessage2Hipchat.py -m "message text" -c "color"

import sys
import json
import urllib2
import argparse

AUTH_TOKEN = 'MY_SECRET_TOKEN'
ROOM_ID    = 'ROOM_ID'

parser = argparse.ArgumentParser(usage='%(prog)s -m <message> -c <color> [-h]')
parser.add_argument('-m','--message', help='Message text to send', required=True)
parser.add_argument('-c','--color', help='Message color', required=True)

if len(sys.argv) < 2:
  parser.print_usage()
  sys.exit(1)
else:
  args = parser.parse_args()
  MSG_COLOR = args.color
  MSG_TEXT  = args.message

def send_message(room_id_or_name, message, color):
    url = "https://api.hipchat.com/v2/room/"+ str(room_id_or_name) + "/notification"
    options = { 'message': message,
                'color': color,
                'message_format':'text',
                'notify': True
            }
    data = json.dumps(options)
    header = {'content-type':'application/json'}
    req = urllib2.Request(url+"?auth_token="+AUTH_TOKEN, data, header)
    res = urllib2.urlopen(req)
    return res.read()

send_message(ROOM_ID, MSG_TEXT, MSG_COLOR)
