
######################################################
# Created on:  3/18/2014
# File:        restartWatcher.py
# Version:     0.1
# Description: Restarts the post2twitter.py script
#
# @author(s) labgeek@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, using version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
######################################################

import psutil
import re
import os
import twitter

PROCESS = 'post2twitter_v2.py'
api = twitter.Api(consumer_key='', 
consumer_secret='', 
access_token_key='', 
access_token_secret='')

for proc in psutil.process_iter():
    pid = proc.pid
    cmdline = proc.cmdline()[1:]
    #print "cmdline = %s" % cmdline
    if 'post2twitter_v2.py' in cmdline:
        print "pid is %s" % pid
        proc.kill()
