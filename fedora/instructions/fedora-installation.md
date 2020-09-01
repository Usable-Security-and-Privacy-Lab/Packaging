# How to install the ssa-daemon on fedora

First, make sure the package manager is up to date and reboot.   
    sudo yum (or dnf) update.    
    reboot. 

## Add private repo to be recognized by your computer
git clone https://github.com/Usable-Security-and-Privacy-Lab/Packaging.   
cp Packaging/ssa.repo  /etc/yum.repos.d/.    

You can verify that this worked by running.    
sudo dnf list available | grep ssa-daemon.    
A package named ssa-daemon should be listed.    

## Install daemon
sudo dnf install ssa-daemon.   

Note that the scriptlet after the Installation will take longer, this is because it is setting up the kernel module.   
If you aren't using the latest kernel, try sudo dnf install kernel-devel-\`uname -r\` to install software necessary to set up the kernel. 
If you need to do this, remove and reinstall the daemon.  
 Verify daemon is running with following.   
 systemctl status ssa-daemon.service.    
 You should get a message that says that the daemon is active and running. 
 
You can stop and start daemon with the following.  
sudo systemctl start ssa-daemon.service.  
sudo systemctl stop ssa-daemon.service.  


# Resources

If this guide doesn't work for you, try looking up instructions for your specific fedora distribution.  
Also make sure make and other dependencies to compile programs are installed on system.   
 for example, sudo yum install dnf, sudo yum install git.   
