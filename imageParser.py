'''
Created on Aug 12, 2016
'''

import sys
import pytsk3
import datetime
import re
import psutil


def directoryRecurse(directoryObject, parentPath):
  for entryObject in directoryObject:
      if entryObject.info.name.name in [".", ".."]:
          continue
      try:
        f_type = entryObject.info.name.type
        #size = entryObject.info.meta.size
      except Exception as error:
          print "Cannot retrieve type or size of",entryObject.info.name.name
          print error.message
          continue
      
      #print entryObject.info.name.name
      filepath = '/%s/%s' % ('/'.join(parentPath),entryObject.info.name.name)
      #print filepath
      if f_type == pytsk3.TSK_FS_NAME_TYPE_DIR:
            sub_directory = entryObject.as_directory()
            print "Entering Directory: %s" % filepath
            parentPath.append(entryObject.info.name.name)
            directoryRecurse(sub_directory,parentPath)
            parentPath.pop(-1)
            print "Leaving Directory: %s" % filepath
      
imagefile = "/home/jd/mobile/heather_image.dd"
imagehandle = pytsk3.Img_Info(imagefile)
partitionTable = pytsk3.Volume_Info(imagehandle)
dirPath = "/"
for partition in partitionTable:
    print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len
    if 'system' in partition.desc: # sometimes this is not found in the partition desc?
        filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start*512))
        fileobject = filesystemObject.open("build.prop")
        #directoryObject = filesystemObject.open_dir(path=dirPath)
        #print "Directory:",dirPath
        #print "File Inode:",fileobject.info.meta.addr
        print "File Name:",fileobject.info.name.name
        #print "File Creation Time:",datetime.datetime.fromtimestamp(fileobject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')
        #print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len
        #directoryObject = filesystemObject.open_dir(path=dirPath)
        #print "Directory:",dirPath
        #directoryRecurse(directoryObject,[])






    
