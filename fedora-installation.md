## How to install the ssa kernel module and ssa-daemon on fedora
## Install Kernel module
1. Make sure the package manager is up to date and reboot.   
    sudo yum update.  
    reboot. 

# Add private repo to be recognized by your computer
curl https://github.com/Usable-Security-and-Privacy-Lab/fedora-packaging/ssa.repo > /etc/yum.repos.d/ssa.repo
Note: .repo says to disable official repositories, as of fedora 32 you can disable the first part of the files in fedora.repo and fedora-updates.repo and it should be fine. You can reenable them after installation. Disabling helps to verify that the repo is working with availability lists

You can verify that this worked by running
sudo dnf list available
there should be two packages listed from ssa called ssa-daemon and ssa-kmod

Make sure everythings updated
yum check-update ssa-kmod --refresh TODO:verify command

## Install Kernel module
sudo yum install ssa-kmod-`uname -r` (or akmod-ssa if we don't have the kmod for that version)
NOTE: 'uname' is automatically replaced by the computer with distribution info

## Install daemon
sudo yum install ssa-daemon
systemctl enable ssa-daemon.service
##### To start daemon, Use:
 systemctl start ssa-daemon.service
 can verify by running
 systemctl status ssa-daemon.service

It will ask for authentification to run daemon

 if the ssa kernel module isn't properly installed, you'll get a message something like this
  Loaded: error (Reason: Unit ssa-daemon.service failed to load properly: Bad message.)


# Resources

How to find your IP address
https://www.techwalla.com/articles/how-to-find-an-ip-address-in-fedora
if this guide doesn't work for you, try looking up instructions for your specific fedora distribution
Also make sure make and other dependencies to compile programs are installed on system
 for example, sudo yum install dnf, sudo yum install make
