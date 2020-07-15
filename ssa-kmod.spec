# (un)define the next line to either build for the newest or all current kernels
#define buildforkernels newest
#define buildforkernels current
%define buildforkernels akmod

%define module ssa
%define version 1
%define repo rpmfusion

# name should have a -kmod suffix
Name: ssa-kmod

Version:        %{version}
Release:        1%{?dist}.1
Summary:        Kernel module(s)

Group:          System Environment/Kernel

License:        Public Domain
URL:            test
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{_bindir}/kmodtool
