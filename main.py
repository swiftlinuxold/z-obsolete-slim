#! /usr/bin/env python

import getpass, sys
#import subprocess
#import sys

#import sys, commands # Allows checking for root
#import os # Needed for removing files
#import shutil # Needed for copying files

username = getpass.getuser() 

if username != 'root':
	sys.exit( 'You must be root to run this script.' )


# Presence of /srv directory indicated chroot mode in antiX Linux
is_chroot = os.path.exists('/srv')
dir_develop=''

if (is_chroot):
	dir_develop='/usr/local/bin/develop'	
else:
	username=commands.getoutput("logname")
	dir_develop='/home/'+username+'/develop'


