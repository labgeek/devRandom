
'''
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.


Tool:  profileExtractor.py
Description:  Forensic tool that pulls out the ProductName and ServicePack in the SW hive and the Architecture in the SYSTEM hive.
              The values will then be mapped to profile strings to be used with Volatility.  Very beta and quickly written.
              The plan was to use this with hibAnalyzer.py which brute forces the profile to be used with Volatility.
              
              
              The first step would be to fun profileExtractor, then hibAnalyzer - both need to be combined.
              
Usage:  python profileExtractor -d /directory/where/hives/are/located (requires both SOFTWARE and SYSTEM)

''' 

'''
TODO:
1.  Error checking
2.  combine with hibAnalyzer
'''

import os
from optparse import OptionParser
import subprocess # not used
import re
import threading # not used
import Queue # not used
import sys
import datetime

try:
    from Registry import Registry
except ImportError:
    print("[!] Python-Registry not found")

__version__ = "0.1"
__status__ = "Development - BETA"


def reghandle(regFile):
    try:
        registry = Registry.Registry(regFile)
        return registry

    except Registry.RegistryKeyNotFoundException:
        print "Couldn't  open the biatch"
        return False


def control_set_check(sys_reg):
    """
    Determine which Control Set the system was using
    """
    registry = reghandle(sys_reg)
    key = registry.open("Select")
    for v in key.values():
        if v.name() == "Current":
            return v.value()
        
def findctrlsets(sys_reg):
    '''
    Nice little function to return ALL the controlsets found within the SYSTEM hive 
    '''
    controls = []
    reg = reghandle(sys_reg)
    root = reg.open("")
    keys = root.subkeys()
    for j in keys:
        if 'ControlSet' in j.path():
            #print j.path()[-13:]
            controls.append(j.path()[-13:])
    return controls

def arch_check(sys_reg):
    """
    Architecture Check
    """
    registry = reghandle(sys_reg)
    key = registry.open("%s\\Control\\Session Manager\\Environment" % findctrlsets(sys_reg)[0])
    for v in key.values():
        if v.name() == "PROCESSOR_ARCHITECTURE":
            return v.value()
 
def getProfiles():
    '''
    Gets the profiles found in the profile.conf file.
    Returns the list of profile names in a list form.
    '''
    plist=[]
    # hard coded for now, will put in config later
    with open("profile.conf") as f:
        for line in f:
            fields = line.split('-')
            plist.append(fields[0].lower())
    return plist       

def readFiles(dir):
    '''
    Simple function to read the files out of a certain directory into a
    list and return that list.
    '''
    dirlist = []
    for dirpath, _, filenames in os.walk(dir):
        for f in filenames:
            dirlist.append(os.path.abspath(os.path.join(dirpath, f)))
    return dirlist


def findRegistryFiles(directory):
    '''
    Takes the directory path and checks the first four bytes for 'regf' to make sure
    the files are actually registry files.  Only wants system and software hives.
    '''
    regList = []
    fileList = []
    fileList = readFiles(directory)
    for file in fileList:
        with open(file, 'rb') as regFile:
            bytes = regFile.read(0x04)
            if 'regf' in bytes:
                if 'software' in file.lower():
                    regList.append(file)
                if 'system' in file.lower():
                    regList.append(file)
    return regList

def os_check(soft_reg):
    """
    Determine the Operating System and do some small checks against certain versions.  
    This needs to be re-written.
    """
    registry = Registry.Registry(soft_reg)
    key = registry.open("Microsoft\\Windows NT\\CurrentVersion")
    for v in key.values():
        if v.name() == "ProductName":
            print "Actual value = %s" % v.value()
            if 'xp' in v.value().lower():
                return 'WinXP'
            elif 'vista' in v.value().lower():
                return 'Vista'
            elif '7' in v.value().lower():
                return 'Win7'
            elif '8' in v.value().lower():
                return 'Win8'
            elif '2003' in v.value().lower():
                return 'Win2003'
            elif '2012' in v.value().lower():
                return 'Win2012'
            else:
                return False
               
        
def getServicePack(soft_reg):
    """
    Determine the Service Pack.
    """
    registry = Registry.Registry(soft_reg)
    key = registry.open("Microsoft\\Windows NT\\CurrentVersion")
    for v in key.values():
        if v.name() == "CSDVersion":
            for x in range(0, 4): # Service pack ranges
                if str(x) in v.value():
                    sp = 'SP'+str(x)
                    return sp


def usage():
    print "python profileExtractor -d <directory registry hives>\n"
    print "Version 0.1 Beta\n"
    exit()

def main():
    '''
    Main function
    '''
    
    fileList = []
    results = []
    prefix = '--profile='
    parser = OptionParser()
    parser = OptionParser(usage="usage: %prog -d <directory>", version="%prog 0.1")
    parser.add_option("-d", "--directory", dest="directory", help="directory path", type="string")
    (options, args) = parser.parse_args()
    dirname = options.directory
    workingList = findRegistryFiles(dirname)
    
    
    if dirname:
        for filePath in workingList:
            if 'software' in filePath.lower():
                productName = os_check(filePath)
         
                results.append(productName)
                servicePack = getServicePack(filePath)
                results.append(servicePack)
            if 'system' in filePath.lower():
                architecture = arch_check(filePath)
                results.append(architecture)

        '''
        print "Product Name = %s" % productName
        print "Service Pack = %s" % servicePack
        print "Arch = %s" % architecture
        '''
        
        iProfile = ''.join([productName, servicePack, architecture]) 
        profile = prefix + iProfile
        print "Here is the profile to use:  %s" % profile
    else:
        usage()
  


if __name__ == '__main__':
    main()

