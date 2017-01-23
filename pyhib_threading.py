#!/usr/bin/python

import os
from optparse import OptionParser
import subprocess
import threading
import time
import Queue
import sys
import datetime

__author__ = "JD Durick"
__email__ = "labgeek@gmail.com"
__version__ = "0.1"
__status__ = "Development - BETA"

volatility = "/data/volatility-2.4/vol.py"
python = "/usr/bin/python"

pattern = 'No suitable address space mapping found'


def executePlugins(plugins, fileName, profile):
    for p in plugins:
        pargs = [python, volatility, '-f', fileName, profile, p]
        print pargs
        print "\nParsing with the %s plugin:\n" % p
        proc = subprocess.Popen(pargs, stdout=subprocess.PIPE)
        print proc.communicate()[0]
        
def commandCreator(fileName):
    commandList = []
    cmd = 'pslist'
    prefix = '--profile='
    newplist = getProfiles()
    for profile in newplist:
        profileName = prefix + profile
        p2 = profileName.rstrip()
        pargs = [python, volatility, '-f', fileName, p2, cmd]
        commandList.append(pargs)
    return commandList
        
def findProfile(commands):
    for c in commands:
        print "command = %s" % c
        proc = subprocess.Popen(c, stdout=subprocess.PIPE)
        for line in iter(proc.stdout.readline, b''):
            if 'System' in line:
                print "PASSED LINE = " + line
                found = True
                break
            else:
                pass
        else:
            continue
        break

# test function
def fp2(cmd):
    found = False
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print("Pid: ", proc.pid)
    for line in iter(proc.stdout.readline, b''):
        if 'System' in line:
            print "PASSED LINE = " + line
            print "CMD ===== %s" % (cmd)
            found = True
            break
        else:
            pass
  
def ghettoProfileFinder(fileName):
    cmd = 'pslist'
    prefix = '--profile='
    pluglist = getPlugins()
    newplist = getProfiles()
    print 'Processing: %s' %  fileName
    for profile in newplist:
        found = False
        profileName = prefix + profile
        p2 = profileName.rstrip()
        pargs = [python, volatility, '-f', fileName, p2, cmd]
        print pargs
        proc = subprocess.Popen(pargs, stdout=subprocess.PIPE)
        print("Pid: ", proc.pid)
        for line in iter(proc.stdout.readline, b''):
            if 'System' in line:
                print "PASSED LINE = " + line
                found = True
                break
            else:
                pass
        else:
            continue
        break
    
    if found is True:
        print "\nBroke out of loop, profile found = %s\n" % profile
        return profile
    else:
        print "No profile found"
        return "NOPROFILEFOUND"
    

def getProfiles():
    plist=[]
    with open("profile.conf") as f:
        for line in f:
            fields = line.split('-')
            plist.append(fields[0])
    return plist

def createProfileList():
    profileList=[]
    prefix = '--profile='
    with open("profile.conf") as f:
        for line in f:
            fields = line.split('-')
            profileName = prefix + fields[0]
            print profileName
            profileList.append(profileName)
    return profileList

def getPlugins():
    pluginList = []
    with open("plugin.conf") as f:
        for line in f:
            fields = line.split(' ')
            plugName = fields[0].strip()
            pluginList.append(plugName)
    return pluginList


def readFiles(dir):
    dirlist = []
    for dirpath, _, filenames in os.walk(dir):
        for f in filenames:
            dirlist.append(os.path.abspath(os.path.join(dirpath, f)))
    return dirlist



def main():
    if sys.version_info < (2, 7, 0):
        sys.stderr.write("Volatility requires python version 2.7, please upgrade your python installation.")
        sys.exit(1)
    print "Version of python:  %s" % (sys.version_info) 
    q = Queue.Queue()
    parser = OptionParser()
    parser = OptionParser(usage="usage: %prog -s <search type> -d <directory> -o <output file>", version="%prog 0.1")
    parser.add_option("-d", "--directory", dest="directory", help="directory path", type="string")
    (options, args) = parser.parse_args()
    start_time = time.time()
    dirname = options.directory
    cmds = []
    threads = []
    if dirname:
        filelist = readFiles(dirname)
        for f in filelist:
            cmds = commandCreator(f)
            
        sizecmds = len(cmds)
        print "Staring %d threads!" % sizecmds
        for c in cmds:
            t = threading.Thread(target=fp2, args=(c,))
            #print threading.active_count()
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print("--- %s seconds ---" % str(time.time() - start_time))           

if __name__ == '__main__':
    main()
