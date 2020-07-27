# (un)define the next line to either build for the newest or all current kernels
#define buildforkernels newest
#define buildforkernels current
%define buildforkernels akmod

%define module ssa-kmod
%define version 1
%define repo rpmfusion

# name should have a -kmod suffix
Name: ssa-kmod

Version:        %{version}
Release:        1%{?dist}.1
Summary:        Kernel module(s)

Group:          System Environment/Kernel

License:        Public Domain
URL:            https://github.com/Usable-Security-and-Privacy-Lab/ssa.git
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

mkdir -p %{_builddir}/%{_usrsrc}
cd %{_builddir}/%{_usrsrc}
if cd ssa; then git pull; else git clone https://github.com/markoneill/ssa ssa; fi

cd %{_builddir}/%{_usrsrc}/ssa/
for kernel_version in %{?kernel_versions} ; do
    mkdir -p ../_kmod_build_${kernel_version%%___*}
    cp -a %{_builddir}/%{_usrsrc}/ssa/* %{_builddir}/%{_usrsrc}/_kmod_build_${kernel_version%%___*}
done

%build
#mkdir -p %{buildroot}/%{_usrsrc}/ssa-%{version}
#cp -r %{_builddir}/%{_usrsrc}/ssa/* %{buildroot}/%{_usrsrc}/ssa-%{version}

cd %{_builddir}/%{_usrsrc}/ssa/
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=%{_builddir}/%{_usrsrc}/_kmod_build_${kernel_version%%___*} modules
done

%build
#mkdir -p %{buildroot}/%{_usrsrc}/ssa-%{version}
#cp -r %{_builddir}/%{_usrsrc}/ssa/* %{buildroot}/%{_usrsrc}/ssa-%{version}

cd %{_builddir}/%{_usrsrc}/ssa/
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=%{_builddir}/%{_usrsrc}/_kmod_build_${kernel_version%%___*} modules
done

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
     echo "${kernel_version}"
     mkdir -p "${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}"
#    make install DESTDIR=${RPM_BUILD_ROOT} KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
     install -D -m 755 %{_builddir}/%{_usrsrc}/_kmod_build_${kernel_version%%___*}/ssa.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ssa.ko
done
#chmod u+x ${RPM_BUILD_ROOT}/lib/modules/*/extra/*/*
%{?akmod_install}

%post
sudo echo "Entering post install"
sudo depmod -a
sudo modprobe ssa-kmod
sudo sh -c "printf \"# Load ssa.ko at boot\nssa\" > /etc/modules-load.d/ssa.conf"

%preun
sudo echo "Entering pre uninstall"
sudo modprobe -r ssa
sudo rm -f /etc/modules-load.d/ssa.conf

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
