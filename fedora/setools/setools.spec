# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

# % define setools_pre_ver beta.1.8e09d95


%global setools_maj_ver 4.1
%global setools_min_ver 0
# %global gitver f1e5b20
%global sepol_ver 2.6-0
%global selinux_ver 2.6-0

Name:           setools
Version:        %{setools_maj_ver}.%{setools_min_ver}
Release:        0.3%{?setools_pre_ver:.%{setools_pre_ver}}%{?dist}
Summary:        Policy analysis tools for SELinux

License:        GPLv2
URL:            https://github.com/TresysTechnology/setools/wiki
Source0:        https://github.com/TresysTechnology/setools/archive/%{version}%{?setools_pre_ver:-%{setools_pre_ver}}.tar.gz
Source1:        setools.pam
Source2:        apol.desktop
Patch1:         0001-Fix-build.patch

Obsoletes:     setools < 4.0.0, setools-devel < 4.0.0
BuildRequires: flex,  bison
BuildRequires: glibc-devel gcc
BuildRequires: libsepol-devel, libsepol-static
BuildRequires: qt5-qtbase-devel
BuildRequires: swig
BuildRequires: python-devel

# BuildArch:      
BuildRequires:  python-devel
%if %{with python3}
Requires:       %{name}-python3 = %{version}-%{release}
BuildRequires:  python3-devel
%else
Requires:       %{name}-python = %{version}-%{release}
%endif # with python3

%description
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.

%package console
Summary: Policy analysis command-line tools for SELinux
Group: System Environment/Base
License: GPLv2
Requires: setools-python3 = %{version}-%{release}
Requires: libselinux >= %{selinux_ver}

%description console
SETools is a collection of graphical tools, command-line tools, and
libraries designed to facilitate SELinux policy analysis.

This package includes the following console tools:

  sediff       Compare two policies to find differences.
  sedta        Perform domain transition analyses.
  seinfo       List policy components.
  seinfoflow   Perform information flow analyses.
  sesearch     Search rules (allow, type_transition, etc.)




%package     python
Summary:     Policy analysis tools for SELinux  
Requires:    python-networkx

%description python
SETools is a collection of graphical tools, command-line tools, and
Python 2 modules designed to facilitate SELinux policy analysis.

%if %{with python3}
%package     python3
Summary:     Policy analysis tools for SELinux  
Obsoletes:   setools-libs < 4.0.0, setools-libs-tcl
Requires:    python3-networkx

%description python3
SETools is a collection of graphical tools, command-line tools, and
Python 3 modules designed to facilitate SELinux policy analysis.

%endif # with python3

%package     gui
Summary:     Policy analysis graphical tools for SELinux
Requires:    python-qt5

%description gui
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.


%prep
%setup -c
# % patch1 -p 0
sed -i "s%'-Werror', '-Wextra'%'-Wextra'%" setools-4.1.0/setup.py

mv setools-%{version}%{?setools_pre_ver:-%{setools_pre_ver}} python2

%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python2} setup.py build
popd

%if %{with python3}
pushd python3
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with python3


%install
rm -rf %{buildroot}
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd python3
%{__python3} setup.py install --root %{buildroot}
popd
%endif # with python3

pushd python2
%{__python2} setup.py install --root %{buildroot}
popd


%check
%if %{?_with_check:1}%{!?_with_check:0}
pushd python2
%{__python2} setup.py test
popd

%if %{with python3}
pushd python3
%{__python2} setup.py test
popd
%endif
%endif

%files
%defattr(-,root,root,-)

%files -n setools-console
%{_bindir}/sediff
%{_bindir}/sedta
%{_bindir}/seinfo
%{_bindir}/seinfoflow
%{_bindir}/sesearch
%{_mandir}/man1/*

%files -n setools-python
%doc
# For noarch packages: sitelib
# %{python2_sitelib}/*
# For arch-specific packages: sitearch
%{python2_sitearch}/*

%if %{with python3}
%files -n setools-python3
%doc
# For noarch packages: sitelib
# %{python3_sitelib}/*
# For arch-specific packages: sitearch
%{python3_sitearch}/*
%endif # with python3

%files gui
%{_bindir}/apol


%changelog
* Wed May  4 2016 Petr Lautrbach <plautrba@redhat.com> 4.0.0-0.1

* Thu Feb 25 2016 Petr Lautrbach <plautrba@redhat.com> 4.0.0-0.beta.1
- 

* Wed Jul 01 2015 Petr Lautrbach <plautrba@redhat.com> 4.0.0-0.alpha2.1.9b28cbe3c7.2
- initial release
