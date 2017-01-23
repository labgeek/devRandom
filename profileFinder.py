import threading
import Queue
import os
from optparse import OptionParser
import subprocess
import threading
import time
import sys
import datetime
import signal
import commands


__author__ = "JD Durick"
__email__ = "labgeek@gmail.com"
__version__ = "0.1"
__status__ = "Development - BETA"

volatility = "/data/volatility-2.4/vol.py"
python = "/usr/bin/python"

# Python-Registry is essential to the functionality of the script

try:
    from Registry import Registry
except ImportError:
    print("[!] Python-Registry not found")

def getProfiles():
    plist=[]
    with open("profile2.conf") as f:
        for line in f:
            fields = line.split('-')
            plist.append(fields[0])
    return plist

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

# thread class to run a command
class VolatilityWorker(threading.Thread):
    def __init__(self, cmd, queue):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.queue = queue

    def run(self):
        # execute the command, queue the result
        (status, output) = commands.getstatusoutput(self.cmd)
        #proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self.queue.put((self.cmd, output, status))

def volWorker(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    print "PID = %s" % proc.pid
    for line in iter(proc.stdout.readline, b''):
        if 'System' in line:
            print "PASSED LINE = " + line
            break
        else:
            pass

def readFiles(dir):
    dirlist = []
    for dirpath, _, filenames in os.walk(dir):
        for f in filenames:
            dirlist.append(os.path.abspath(os.path.join(dirpath, f)))
    return dirlist

def main():
    threads = []
    if sys.version_info < (2, 7, 0):
        sys.stderr.write("Volatility requires python version 2.7, please upgrade your python installation.")
        sys.exit(1)
    print "Version of python:  %s" % (sys.version_info) 
    parser = OptionParser()
    parser = OptionParser(usage="usage: %prog -s <search type> -d <directory> -o <output file>", version="%prog 0.1")
    parser.add_option("-d", "--directory", dest="directory", help="directory path", type="string")
    (options, args) = parser.parse_args()

    dirname = options.directory
    if dirname:
        filelist = readFiles(dirname)
        for f in filelist:
            cmds = commandCreator(f)

        lenofcommands = len(cmds)
        print "len = %s" % lenofcommands
        for c in cmds:
            t = threading.Thread(target=volWorker, args=(c,))
            t.start()
            threads.append(t)            
            
                
        for t in threads:
            t.join()
    print "THE END"

if __name__ == '__main__':
    main()
