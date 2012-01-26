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
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================

# THIS IS THE SCRIPT FOR REPLACING THE DEFAULT LMDE LOGIN MANAGER WITH A LIGHTER ONE.

# Remove GDM3 login manager
os.system('apt-get purge -y gdm3')

# if (os.path.exists('/usr/share/gdm')):
#	shutil.rmtree('/usr/share/gdm')

# Install SLiM login manager
os.system('apt-get install -y slim')

# ============================
# Configure SLiM login manager
import shutil

# Delete the debian-moreblue, debian-moreblue-orbit, debian-spacefun, and default themes
# Checking for their existence is redundant but avoids error messages when testing multiple times on the desktop
if (os.path.exists('/usr/share/slim/themes/debian-moreblue/')):
	shutil.rmtree('/usr/share/slim/themes/debian-moreblue/')
if (os.path.exists('/usr/share/slim/themes/debian-moreblue-orbit/')):
	shutil.rmtree('/usr/share/slim/themes/debian-moreblue-orbit/')
if (os.path.exists('/usr/share/slim/themes/debian-spacefun/')):
	shutil.rmtree('/usr/share/slim/themes/debian-spacefun/')
if (os.path.exists('/usr/share/slim/themes/default/')):
	shutil.rmtree('/usr/share/slim/themes/default/')

# If /usr/share/slim/themes/swift/ exists, delete it.
if (os.path.exists('/usr/share/slim/themes/swift/')):
	shutil.rmtree('/usr/share/slim/themes/swift/')

# Create /usr/share/slim/themes/swift/
os.mkdir('/usr/share/slim/themes/swift/')

# Use the panel.png file from antiX Linux
src = dir_develop + '/ui-login/usr_share_slim_themes_swift/panel.png'
dest = '/usr/share/slim/themes/swift/panel.png'
shutil.copy (src, dest)

# Use the slim.theme file from antiX Linux
src = dir_develop + '/ui-login/usr_share_slim_themes_swift/slim.theme'
dest = '/usr/share/slim/themes/swift/slim.theme'
shutil.copy (src, dest)

# Provide the SLiM wallpaper
# WARNING: If the background.jpg file is not present in the theme directory to be used,
# SLiM will NOT work.
if (os.path.exists('/usr/share/slim/themes/swift/background.jpg')):
	os.remove('/usr/share/slim/themes/swift/background.jpg')
src = dir_develop + '/edition-regular/login-regular.jpg'
dest = '/usr/share/slim/themes/swift/background.jpg'
shutil.copy (src, dest)

# Replace /etc/slim.conf
# Changes the available sessions (DE/WM)
# Changes the default theme
os.remove ('/etc/slim.conf')
src = dir_develop + '/ui-login/etc/slim.conf'
dest = '/etc/slim.conf'
shutil.copy (src, dest)

# Replace /etc/adduser.conf and /etc/group
# The original /etc/adduser.conf and /etc/group do NOT enable sound.
# The original LMDE setup relies on GDM3 to enable many features that
# are disabled upon removing GDM3.

def change_text (filename, text_old, text_new):
    # Replaces text within a file
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)

def copy_file (file_old, file_new, text_old, text_new):
    # Copies a file and replaces text within the new file
    ret = os.access(file_new, os.F_OK)
    if (ret):
        os.remove (file_new)
    shutil.copy2 (file_old, file_new)
    change_text(file_new, text_old, text_new)

src = dir_develop + '/ui-login/etc/adduser.conf'
dest = '/etc/adduser.conf'
shutil.copy (src, dest)

if (is_chroot):
    src = dir_develop + '/ui-login/etc/group'
    dest = '/etc/group'
    shutil.copy (src, dest)
else:
    file1 = dir_develop + '/ui-login/etc/group'
    file2 = '/etc/group'
    text1 = 'mint'
    text2 = uname
    copy_file (file1, file2, text1, text2)
