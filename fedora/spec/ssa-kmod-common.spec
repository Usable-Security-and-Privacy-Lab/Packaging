%define module ssa-kmod-common
%define version 1

Name:    %{module}
Version: %{version}
Release: 1%{?dist}
Summary: Installs the Secure Socket API (SSA) Linux kernel module and daemon

Group:   System Environment/Kernel

License: Public Domain
#Source0: /home/bright19/Documents/packages/ssa/howdy
BuildArch: x86_64
URL: https://owntrust.org/ssa

%description

%prep
mkdir -p %{_builddir}/%{_usrsrc}
cd %{_builddir}/%{_usrsrc}
if cd ssa; then git pull; else git clone https://github.com/markoneill/ssa ssa; fi

%build

%install
mkdir -p %{buildroot}/%{_usrsrc}/ssa-kmod-common-%{version}
cp -r %{_builddir}/%{_usrsrc}/ssa/test_files %{buildroot}/%{_usrsrc}/ssa-kmod-common-%{version}/
cp -r %{_builddir}/%{_usrsrc}/ssa/README.md %{buildroot}/%{_usrsrc}/ssa-kmod-common-%{version}/
cp -r %{_builddir}/%{_usrsrc}/ssa/config_parse %{buildroot}/%{_usrsrc}/ssa-kmod-common-%{version}/

%pre

%post

%preun

%files
%{_usrsrc}/ssa-kmod-common-%{version}/*

%changelog
