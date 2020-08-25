# Package Building and  Installation Instructions - Fedora (Red Hat)

# How to Build the Fedora Package:

1. Verify that ssa-daemon.spec has these lines.  
sudo echo "  Entering post install"                                                 .                                                 
git clone https://github.com/Usable-Security-and-Privacy-Lab/ssa.git                .   
cd ssa                                                                              .   
make                                                                                .  
cp ssa.ko /lib/modules/`uname -r`                                                   .   
sudo depmod -a                                                                      .  
sudo modprobe ssa                                                                   .   
sudo sh -c "printf \"# Load ssa.ko at boot\nssa\" > /etc/modules-load.d/ssa.conf"   .  
.  
sudo echo "  Entering pre uninstall"    .   
sudo rm /lib/modules/`uname -r`/ssa.ko  .  
sudo modprobe -r                        .  
sudo rm -f /etc/modules-load.d/ssa.conf .  

2. How to create repository to store packages(rpm files) 
yum install createrepo httpd                 .  
mkdir -p /var/www/html/fedora                .  
sudo createrepo /var/www/html/fedora/        .  
systemctl enable httpd.service               .   
systemctl start httpd.service                .  
firewall-cmd --permanent --add-service=http  .  
firewall-cmd --add-service=http              .  
 

3. Install dependencies
If this is the first time, you may need to do a yum install for any missing dependencies              .   
eg                                                                                                    .   
sudo dnf install kernel-devel-`uname -r` kernel-headers-`uname -r`                                    .   
sudo yum install avahi-devel elfutils-libelf-devel glib-devel gtk3-devel libconfig libconfig-devel libevent-devel libnl3-devel libnotify-devel openssl-devel elfutils-libelf-devel qrencode fedpkg libyaml-devel  .          

4. Set up structure for package building directory.   
The structure of the directory where the package is built is crtical for it to work.  
For example on the structure should be, chack tarballs in Packaging/fedora/compressed folder.  
mkdir package-builder                                                        .  
cd package-builder                                                           .  
mkdir usr/src/                                                               .  
cd usr/src                                                                   .  
git clone https://github.com/Usable-Security-and-Privacy-Lab/ssa-daemon.git  .  
cd ../..    
git clone https://github.com/Usable-Security-and-Privacy-Lab/Packaging.git   .    
cp Packaging/fedora/spec/ssa-daemon.spec ./                                  .  
rm -r Packaging                                                              .   
5. Build package for the ssa-daemon and copy it to the package repository       .    
fedpkg --release <desired fedora release eg f32, f33,...> local              .  
sudo cp x86_64/ssa-daemon-1-1.fc29.x86_64.rpm <repository>                   .  

6. Update the repo                                                       .  
sudo createrepo </path/to/repository> (if local, /var/www/html/fedora).   


# Resources
0.a How to install new kernel (eg 28 to 29) .  
sudo dnf upgrade --refresh                  .  
sudo dnf install dnf-plugin-system-upgrade  .  
sudo dnf system-upgrade download --refresh --releasever=29 (the version of the release).  
sudo dnf system-upgrade reboot              .  

0.b Upgrade kernel (eg 4.18 to 4.20)        .  
sudo dnf update                             .  
This is a helpful guide for working with kernel modules in fedora.  
 https://docs.fedoraproject.org/en-US/fedora/rawhide/system-administrators-guide/kernel-module-driver-configuration/Working_with_Kernel_Modules/
.  
Note for new developers making install packages, a .rpm packages purpose is to allow fedora to automatically update source code.  
.  
Also note on general plan for fedora packaging.  
There are three ways to provide source code to public.  

1. Manually download and compile source code from github
2. Set up private repository that anyone can access with public key
3. Get set up in fedora public repositories( a lot of work)

We are adding support for the second option.   

Here is a guide for .target files that you need to know of you ever have to debug network-online.target.    
https://www.freedesktop.org/software/systemd/man/systemd.target.html  .  

General overview of writing Fedora packages   .  
https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/ .  
Here is a guide on working with kernel modules in fedora   .  
https://docs.fedoraproject.org/en-US/fedora/rawhide/system-administrators-guide/kernel-module-driver-configuration/Working_with_Kernel_Modules/

