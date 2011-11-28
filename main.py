#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'	
else:
	dir_develop='/home/'+uname+'/develop'

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================

# THIS IS THE SCRIPT FOR REPLACING THE DEFAULT LMDE LOGIN MANAGER WITH A LIGHTER ONE.

# Remove GDM3 login manager
os.system('apt-get remove -y gdm3')

# Install SLiM login manager
os.system('apt-get install -y slim')

# ============================
# Configure SLiM login manager

# If /usr/share/slim/themes/swift/ exists, delete it.
if (os.path.exists('/usr/share/slim/themes/swift/')):
	os.rmdir('/usr/share/slim/themes/swift/')

# Create /usr/share/slim/themes/swift/
os.mkdir('/usr/share/slim/themes/swift/')

import shutil
# Use the panel.png file from antiX Linux
src = dir_develop + '/ui-login/usr_share_slim_themes_swift/panel.png'
dest = '/usr/share/slim/themes/swift/panel.png'
shutil.copy (src, dest)

# Use the slim.theme file from antiX Linux
src = dir_develop + '/ui-login/usr_share_slim_themes_swift/slim.theme'
dest = '/usr/share/slim/themes/swift/slim.theme'
shutil.copy (src, dest)

# Replace /etc/slim.conf
# Changes the available sessions (DE/WM)
# Changes the default theme
os.remove ('/etc/slim.conf')
src = dir_develop + '/ui-login/etc/slim.conf'
dest = '/etc/slim.conf'
shutil.copy (src, dest)

