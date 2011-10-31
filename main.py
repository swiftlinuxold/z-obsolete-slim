#! /usr/bin/env python

import os, sys
#import subprocess
#import sys

#import sys, commands # Allows checking for root
#import shutil # Needed for copying files

user = os.environ['USER'] # is root or your regular user name
username = os.environ['USERNAME'] # your regular user name, EVEN when you execute as root

if user != 'root':
	sys.exit( 'You must be root to run this script.' )

# Presence of /home/mint directory indicates chroot mode in LMDE
is_chroot = os.path.exists('/home/mint')
dir_develop=''

if (is_chroot):
	dir_develop='/usr/local/bin/develop'	
else:
	dir_develop='/home/'+username+'/develop'

# Remove GDM3 login manager
os.system('apt-get remove -y gdm3')

# Install SLiM login manager
os.system('apt-get install -y slim')

# Configure SLiM login manager
