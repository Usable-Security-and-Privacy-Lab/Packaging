#How to install the ssa kernel module and ssa-daemon on fedora
##Install Kernel module
1. Make sure the package manager is up to date and reboot
    sudo yum update
    reboot

2. Install kernel module

curl http://(your local ip)/fedora/ssa.repo > /etc/yum.repos.d/ssa.repo
Note: .repo says to disable official repositories, as of fedora 32 you can disable the first part of the files in fedora.repo and fedora-updates.repo and it should be fine. You can reenable them after installation. Disabling helps to verify that the repo is working with
sudo dnf list available
there should be two packages listed from ssa called ssa-daemon and ssa-kmod
TODO: instructions for akmods?
//alternate
curl https://github.com/brightcandlelight/fedora-packaging/ssa.repo > /etc/yum.repos.d/ssa.repo
//end alternate

yum check-update ssa --refresh
#

sudo yum install ssa-kmod-`uname -r` (or akmod-ssa if we don't have the kmod for that version)
NOTE: 'uname' is automatically replaced by the computer with distribution info
sudo yum install ssa-daemon
systemctl enable ssa-daemon.service
#To start daemon, Use:
 systemctl start ssa-daemon.service
 can verify by running
systemctl status ssa-daemon.service



It will ask for authentification to run daemon

 if the ssa kernel module isn't properly installed, you'll get a message something like this
  Loaded: error (Reason: Unit ssa-daemon.service failed to load properly: Bad message.)

QUESTION: what should status say?  TODO: write down what it looks like when it's working
#If you upgrade to a new kernel version and have installed kmod instead of akmod you will need to install the newest ssa and potentially also ssa-daemon.


#Resources

How to find your IP address
https://www.techwalla.com/articles/how-to-find-an-ip-address-in-fedora
if this guide doesn't work for you, try looking up instructions for your specific fedora distribution
Also make sure make and other dependencies to compile programs are installed on system
 for example, sudo yum install dnf, sudo yum install make
