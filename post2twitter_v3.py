#######################################################################
# Created on:  3/7/2014
# File:        post2twitter.py
# Version:     0.1
# Description: Post to you twitter page when you someone logs into 
# you minecraft server
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
import twitter
import os
import time
import datetime
import sys
import re

api = twitter.Api(consumer_key='', 
consumer_secret='', 
access_token_key='', 
access_token_secret='')

# tail functionality shamelessly stolen from stackoverflow, gracias gents.
def tail(f):
    f.seek(0, 2)
    while True:
        line = f.readline()

        if not line:
            time.sleep(0.1)
            continue

        yield line

def process_matches(matchtext):
    while True:
        line = (yield)  
        if matchtext in line:
           protected = ['n','s','vmgeek']
           # do_something_useful() # email alert, etc.
           #print "matching %s" % matchtext
           #print line # this prints line
	   namematch = re.search('^(\S+) (\S+) (\S+) (\S+) (.*)', line)
	   date = namematch.group(1)
           login =  namematch.group(4)
           postline = "%s - %s" % (date, login)
	   for p in protected:
	       if re.search(p, postline):
                   localmessage = "%s just logged in -  %s" % (p,date)
                   status = api.PostUpdate(localmessage)
		   break
               else:
		   print "got here %s" % postline
                   status = api.PostUpdate(postline)
		   #break


list_of_matches = ['logged in']
matches = [process_matches(string_match) for string_match in list_of_matches]    

for m in matches: # prime matches
    m.next()

while True:
    auditlog = tail( open('/root/bukkit/logs/latest.log') )
    for line in auditlog:
        #print line
        for m in matches:
            m.send(line)
