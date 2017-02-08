%global libsepolver 2.6-0

Name:           secilc
Version:        2.6
Release:        0.2%{?dist}
Summary:        The SELinux CIL Compiler

License:        BSD
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20161014/secilc-2.6.tar.gz
# download https://raw.githubusercontent.com/fedora-selinux/scripts/master/selinux/make-fedora-selinux-patch.sh
# run:
# $ VERSION=2.6 ./make-fedora-selinux-patch.sh secilc
# HEAD https://github.com/fedora-selinux/selinux/commit/4bfb84c7ff7b33cf06b9a6b2317d24054b9db562
# Patch1: secilc-fedora.patch

BuildRequires:  libsepol-static >= %{libsepolver}, dblatex, flex, xmlto, pandoc

%description
The SELinux CIL Compiler is a compiler that converts the CIL language as
described on the CIL design wiki into a kernel binary policy file.
Please see the CIL Design Wiki at:
http://github.com/SELinuxProject/cil/wiki/
for more information about the goals and features on the CIL language.

%package doc
Summary:        Documentation for the SELinux CIL Compiler
BuildArch:      noarch

%description doc
The SELinux CIL Compiler is a compiler that converts the CIL language as
described on the CIL design wiki into a kernel binary policy file.
Please see the CIL Design Wiki at:
http://github.com/SELinuxProject/cil/wiki/
for more information about the goals and features on the CIL language.

%prep
%setup -q -n secilc-%{version}


%build
make %{?_smp_mflags} CFLAGS="%{optflags}" LIBSEPOL_STATIC=%{_libdir}/libsepol.a
pushd docs
make %{?_smp_mflags}
popd


%install
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR="%{buildroot}" SBINDIR="%{buildroot}%{_sbindir}" LIBDIR="%{buildroot}%{_libdir}" install


%files
%{_bindir}/secilc
%{_mandir}/man8/secilc.8.gz
%license COPYING

%files doc
%doc docs/html
%doc docs/pdf
%license COPYING

%changelog
* Wed Feb 08 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-0.2
- Update to upstream release 2016-10-14

* Tue Oct 04 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-6
- Rebuilt with libsepol-2.5-10

* Mon Aug 01 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-5
- Rebuilt with libsepol-2.5-9

* Thu Jun 23 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-4
- Rebuilt with libsepol-2.5-7

* Wed May 11 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-3
- Rebuilt with libsepol-2.5-6

* Fri Apr 08 2016  - 2.5-2
- Add documentation and test rule for portcon dccp protocol

* Tue Feb 23 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-1
- Update to upstream release 2016-02-23

* Sun Feb 21 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-0.1.rc1
- Update to upstream rc1 release 2016-01-07

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 01 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.4-6
- tell make where libsepol.a is to fix FTBFS on non-x86 64-bit archs - rhbz#1249522

* Wed Jul 29 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-5
- secilc-doc do not need the base package
- Fedora package review https://bugzilla.redhat.com/show_bug.cgi?id=1245270

* Thu Jul 23 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-4
- add license file

* Wed Jul 22 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-3
- remove unnecessary dependencies
- don't build libsepol

* Tue Jul 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-2
- make secilc-doc package noarch

* Tue Jul 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-1
- initial build based on libsepol-2.4 sources
