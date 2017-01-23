######################################################
# Created on:  3/22/2014
# File:        rebooter.py
# Version:     0.1
# Description: reboots minecraft when called.
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
from subprocess import PIPE
import twitter
import time
import re

api = twitter.Api(consumer_key='', 
consumer_secret='', 
access_token_key='', 
access_token_secret='')


CWD = "/root/bukkit/" # Path to where Minecraft lives
JAVA_EXE = "/usr/bin/java"
MINECRAFT_JAR = "craftbukkit-beta.jar"
#MINECRAFT_COMMAND = "{0} -Xmx1024M -Xms1024M -jar {1} nogui".format(JAVA_EXE, MINECRAFT_JAR).split()
MINECRAFT_COMMAND = "{0} -jar {1} nogui".format(JAVA_EXE, MINECRAFT_JAR).split()
SCREEN_COMMAND = "screen -d -m -S minecraft".split()
minecraft_process = "java"


def check_minecraft(process):
    #print 'process name = %s' % process.name()   
    if process.name() == minecraft_process:
        print "process name MATCHED**************** = %s" % process.name()
        print "Minecraft is up and running"
        return True

def start_minecraft():
    current_time = time.strftime("%H:%M:%S")
    message = "[%s]: VMFORENSICS MC Server restarted" % current_time
    #print "Current time is %s" % current_time
    print "Minecraft isn't running. Starting it with following command: {0}".format(
            " ".join(SCREEN_COMMAND + MINECRAFT_COMMAND))
    process = psutil.Popen(SCREEN_COMMAND + MINECRAFT_COMMAND, stdout=PIPE, cwd=CWD)
    status = api.PostUpdate(message)
    current_time = time.strftime("%H:%M:%S")
    
def main():

    
    current_time = time.strftime("%H:%M:%S")
    print "Current time is %s" % current_time
    for proc in psutil.process_iter():
        if check_minecraft(proc):
            pid = proc.pid
            cmdline = proc.cmdline()[1:]
            if 'craftbukkit-beta.jar' in cmdline:
                #print "pid and cmdline %s and %s- reboot here" % (pid, cmdline)
                #print "Killing proc id:  %s" % proc.pid
                proc.kill()
                time.sleep(5)
                process = psutil.Popen(SCREEN_COMMAND + MINECRAFT_COMMAND, stdout=PIPE, cwd=CWD)
                #print "Restarting with new process id:  %s" % process.pid
                startmessage = "[%s]: Restarting VMFORENSICS Minecraft Server now!" % current_time
                status = api.PostUpdate(startmessage)
                break
        else:
            #start_minecraft()
            #print "minecraft is not up"
	    pass


if __name__ == '__main__':
    main()
