#######################################################################
# Created on:  11/23/2013
# File:        backupMinecraft.py
# Version:     0.1
# Description: Backups minecraft daily.
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
# add feature to MD5 the file, compare and then scp it back home

import datetime
import os.path
import tarfile
import datetime
import smtplib


def main():
    source = "/root/spigot"
    est_datetime = datetime.datetime.now()
    formated_string = est_datetime.strftime("%Y-%m-%d-%H%M_EST") # //Result: '2011-12-12-0939Z'
    filename = '/data/backup/spigot_backup_%s.tar.gz'% formated_string
    if os.path.exists(source):
        #print filename + " does exist!"
        make_tarfile(filename, source)
        sendSMS()
    else:
        exit

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def sendSMS():
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login( 'xxxxxxxxxxxxxx', 'xxxxxxx' )
    server.sendmail( 'IP address:  10.x.x.x', '<cell phone number>@vtext.com', 'Spigot directory on vmforensics.org was successful!' )


if __name__ == '__main__':
    main()
