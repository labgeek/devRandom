#!/usr/bin/python
'''
Tool:  pyhibBeta.py
Author:  JD Durick
Date:  12/23/2014
Description:  Tool grabs a hiberfil.sys file and brute forces the profile via Volatility 2.4.
Additionally, the tool guess at the correct profile however imageinfo and kdbgscan should be used

TODO:  need to be provided SOFTWARE and SYSTEM hives for correct profile(s) instead of using brute force.
Additionally, would like to integrate threading.
''' 

import os
from optparse import OptionParser
import subprocess
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
    '''
    Executes the plugins after the profile has been found.  Creates directory 
    and appends output of proc results to filename.
    Input:  plugin list, filename of the hiberfil.sys file, and profile name
    Output:  nothing yet
    '''
    name, ext = os.path.splitext(fileName)
    if not os.path.exists(name):
        os.makedirs(name)
    
    for pluginName in plugins:
        fullPath = name + "/" + pluginName + '.txt'
        pargs = [python, volatility, '-f', fileName, profile, pluginName]
        print "\nParsing with the %s plugin:\n" % pluginName
        proc = subprocess.Popen(pargs, stdout=subprocess.PIPE)

        results = proc.communicate()[0]
        with open(fullPath, 'a') as f:
            f.write(results)
            f.close()
    

def getProfiles():
    '''
    Gets the profiles found in the profile.conf file.
    Returns the list of profile names in a list form.
    '''
    plist=[]
    with open("profile.conf") as f:
        for line in f:
            fields = line.split('-')
            plist.append(fields[0])
    return plist

def createProfileList():
    '''
    Creates a profile list with the --profile= 
    added onto the front.
    Not currently being used yet
    '''
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
    '''
    Gets the plugins from the file plugin.conf
    Returns a list of plugins.
    '''
    pluginList = []
    with open("plugin.conf") as f:
        for line in f:
            fields = line.split(' ')
            plugName = fields[0].strip()
            pluginList.append(plugName)
    return pluginList


def readFiles(dir):
    '''
    Reads a directory.
    Input:  directory name
    Output:  list of files with their abosulte path
    '''
    dirlist = []
    for dirpath, _, filenames in os.walk(dir):
        for f in filenames:
            dirlist.append(os.path.abspath(os.path.join(dirpath, f)))
    return dirlist



def main():
    
    parser = OptionParser()
    parser = OptionParser(usage="usage: %prog -s <search type> -d <directory> -o <output file>", version="%prog 0.1")
    parser.add_option("-d", "--directory", dest="directory", help="directory path", type="string")
    parser.add_option("-o", "--outdir", dest="outdir", help="write report to FILE")
    (options, args) = parser.parse_args()

    dirname = options.directory
    outputDir = options.outdir

    cmd = 'pslist'
    prefix = '--profile='
    if dirname and outputDir:
        pluglist = getPlugins()
        newplist = getProfiles()
        filelist = readFiles(dirname)
        for fileName in filelist:
            print '*****ANALYZING******' + fileName
            for profile in newplist:
                profileName = prefix + profile
                formattedProfilename = profileName.rstrip()
                pargs = [python, volatility, '-f', fileName, formattedProfilename, cmd]
		print pargs
		proc = subprocess.Popen(pargs, stdout=subprocess.PIPE)
		for line in iter(proc.stdout.readline, b''):
		    if 'System' in line:
		        print "PASSED LINE = " + line
			break
		    else:
		        pass
		else:
		    continue
		break
	    

            print "\nBroke out of loop, profile found = %s\n" % profile
            goodprofile = prefix + profile
            formattedFoundProfile = goodprofile.rstrip()
            executePlugins(pluglist, fileName, formattedFoundProfile)

if __name__ == '__main__':
    main()
