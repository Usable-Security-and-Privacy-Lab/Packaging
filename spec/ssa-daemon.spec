%define module ssa-daemon
%define version 1

Name:    %{module}
Version: %{version}
Release: 1%{?dist}
Summary: Installs the Secure Socket API (SSA) Linux daemon

License: Public Domain
BuildArch: x86_64
URL: https://owntrust.org/ssa
# Requires: kernel-devel = %{current_kernel}
# Requires: kernel-headers = %{current_kernel}
#Requires: kmod-ssa
#Requires: ssa-kmod-common
# Fedora
#Requires: avahi-devel, elfutils-libelf-devel, glib-devel, gtk3-devel, libconfig, libconfig-devel, libevent-devel, libnl3-devel, libnotify-devel, openssl-devel
# Ubuntu
# Requires: libavahi-client-dev, libconfig-dev, libelf-dev, libevent-dev, libglib2.0-dev, libnl-3-dev, libnl-genl-3-dev, libnotify-dev, openssl

%description
The SSA is a Linux kernel module that allows programmers to easily create
secure TLS connections using the standard POSIX socket API. This allows
programmers to focus more on the developement of their apps without having
to interface with complicated TLS libraries. The SSA also allows system
administrators and other power users to customize TLS settings for all
connections on the machines they manage, according to their own needs.

%prep
echo "1.Updating repo"
mkdir -p %{_builddir}/%{_usrsrc}
cd %{_builddir}/%{_usrsrc}
if cd ssa-daemon; then git pull; else git clone https://github.com/Usable-Security-and-Privacy-Lab/ssa-daemon.git ssa-daemon; fi

%build
echo "2.Build daemon"
cd %{_builddir}/%{_usrsrc}/ssa-daemon
./install_packages.sh
make clean
make

%install
mkdir -p %{buildroot}/%{_usrsrc}/ssa-daemon-%{version}
cp -r %{_builddir}/%{_usrsrc}/ssa-daemon/* %{buildroot}/%{_usrsrc}/ssa-daemon-%{version}

%pre
%post
cd /usr/src/ssa-daemon-%{version}/

git clone https://github.com/Usable-Security-and-Privacy-Lab/ssa.git
cd ssa
make
sudo cp ssa.ko /lib/modules/`uname -r`
sudo depmod -a
sudo modprobe ssa
sudo sh -c "printf \"# Load ssa.ko at boot\nssa\" > /etc/modules-load.d/ssa.conf"
cd ..
rm -r ssa

chmod +x /usr/src/ssa-daemon-%{version}/ssa_daemon
sudo sh -c "printf \"[Unit]\nAfter=network-online.target\n\n[Service]\nExecStart=/bin/bash -c 'cd /usr/src/ssa-daemon-%{version} && PATH=/usr/src/ssa-daemon-%{version}:/usr/bin/ssa-daemon-%{version}/test_files:/usr/bin/ssa-${version}:$PATH exec ./ssa_daemon'\n\n[Install]\nWantedBy=network-online.target\n\n\" > /etc/systemd/system/ssa-daemon.service"
systemctl daemon-reload
systemctl enable ssa-daemon.service
systemctl start ssa-daemon.service

%preun
echo -e "Uninstall of %{module} (version %{version}) beginning:"

sudo rm /lib/modules/`uname -r`/ssa.ko
sudo modprobe -r ssa
sudo rm -f /etc/modules-load.d/ssa.conf

systemctl stop ssa-daemon.service
systemctl disable ssa-daemon.service

sudo rm -f /etc/systemd/system/ssa-daemon.service

%files
%{_usrsrc}/ssa-daemon-%{version}/*

%changelog
