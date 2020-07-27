# Package Building and  Installation Instructions - Fedora (Red Hat)
#######################################
# How to Build package for a new kernel:

0.a Install your new kernel (eg 28 to 29)
sudo dnf upgrade --refresh
sudo dnf install dnf-plugin-system-upgrade
sudo dnf system-upgrade download --refresh --releasever=29 (the version of the release)
sudo dnf system-upgrade reboot

0.b Upgrade kernel (eg 4.18 to 4.20)
sudo dnf update

1.If you have upgraded your kernel, you will need to make sure your kmodtool has the modification(what modification?). It may have gotten overridden by the kernel update. Edit /usr/bin/kmodtool and make sure it has these lines. (you may need to do a "yum install kmodtool" first). use sudo vim(or another text editor) to write to a readonly file

%if 0%{?rhel}.       
...
%else
%post -n kmod-${kmodname}-${kernel_uname_r}
/usr/sbin/depmod -aeF /boot/System.map-4.18.16-300.fc29.x86_64 4.18.16-300.fc29.x86_64 > /dev/null || : 

#Start change
sudo echo "  Entering post install"
sudo depmod -a //For me: creates module dependencies on all kernel modules
sudo modprobe ssa //For me: adds dependency on ssa kernel module
sudo sh -c "printf \"# Load ssa.ko at boot\nssa\" > /etc/modules-load.d/ssa.conf" //sets to be loaded at boot
%preun -n kmod-${kmodname}-${kernel_uname_r}

sudo echo "  Entering pre uninstall"
sudo modprobe -r //ssa removes ssa kernel module
sudo rm -f /etc/modules-load.d/ssa.conf //doesn't attempt to load at boot
#End change

2.
If this is your first time building, create repo to store your rpm files

yum install createrepo httpd
mkdir -p /var/www/html/fedora
sudo createrepo /var/www/html/fedora/
systemctl enable httpd.service
systemctl start httpd.service
firewall-cmd --permanent --add-service=http
firewall-cmd --add-service=http

Also download the following pieces:
git clone https://github.com/Usable-Security-and-Privacy-Lab/fedora-packaging.git
cd fedora-packaging
cp ssa-kmod.spec /var/www/html/fedora (update your ip in the ssa-kmod.spec)
tar xvf ssa-kmod.tar.gz
tar xvf ssa-daemon.tar.gz

3.
If this is the first time, you may need to do a yum install for any missing dependencies
eg
sudo dnf install kernel-devel-`uname -r` kernel-headers-`uname -r`
sudo yum install avahi-devel elfutils-libelf-devel glib-devel gtk3-devel libconfig libconfig-devel libevent-devel libnl3-devel libnotify-devel openssl-devel elfutils-libelf-devel qrencode fedpkg libyaml-devel

Note: If the kernel-devel command failed, try this one instead    
kernel=`uname -r | sed 's/-/\//' | sed 's/\(.*\)\./\1\//'`
sudo yum install https://kojipkgs.fedoraproject.org//packages/kernel/${kernel}/kernel-devel-`uname -r`.rpm

4.
Build the newest version of the ssa-daemon and copy to fedora.
cd ssa-daemon
fedpkg --release f29 local
sudo cp x86_64/ssa-daemon-1-1.fc29.x86_64.rpm /var/www/html/fedora

cd ../ssa-kmod
fedpkg --release f29 local
cp x86_64/kmod-ssa-<kernel version> /var/www/html/fedora

#ok, if this fails you need to downgrade to the latest kernel with buildsys-build-rpmfusion. Or just build the akmod version. A little annoying
go here to see the latest, good luck on this path.
https://www.rpmfind.net/linux/rpm2html/search.php?query=buildsys-build-rpmfusion-kerneldevpkgs-current
https://www.rpmfind.net/linux/rpm2html/search.php?query=buildsys-build-rpmfusion
https://www.rpmfind.net/linux/rpm2html/search.php?query=kernel-devel-uname-r
Install the latest buildsys-build-rpmfusion-kerneldevpkgs-current with the corresponding kernel-debug-devel and buildsys-build that it requires.
OR - build the akmod version (uncomment which one you want with ssa-kmod.spec)

4.
Update the repo
sudo createrepo /var/www/html/fedora/


# Resources

This is a helpful guide for working with kernel modules in fedora
 https://docs.fedoraproject.org/en-US/fedora/rawhide/system-administrators-guide/kernel-module-driver-configuration/Working_with_Kernel_Modules/

Note for new developers making install packages, a .rpm packages purpose is to allow fedora to automatically update source code

Also note on general plan for fedora packaging There are three ways to provide source code to public

1. Manually download and compile source code from github
2. Set up private repository that anyone can access with public key
3. Get set up in fedora public repositories( a lot of work)

We are adding support for the second option    

Here is a guide for .target files that you need to know of you ever have to debug network-online.target
https://www.freedesktop.org/software/systemd/man/systemd.target.html

General overview of writing Fedora packages
https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/
