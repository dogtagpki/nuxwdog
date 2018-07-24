Name:           nuxwdog
Version:        1.0.4
Release:        2%{?dist}
Summary:        Watchdog server to start and stop processes, and prompt for passwords
# The entire source code is LGPLv2 except for the perl module, which is GPL+ or Artistic
License:        LGPLv2 and (GPL+ or Artistic)
URL:            http://www.redhat.com/certificate_system

# For epel5 and fc < 20 compatibility
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

BuildRequires:  ant
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils
BuildRequires:  nspr-devel
BuildRequires:  nss-devel
BuildRequires:  pkgconfig
BuildRequires:  libselinux-devel
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  keyutils-libs-devel
BuildRequires:  gcc-c++

Requires:       nss
Requires:       keyutils-libs
Obsoletes:      nuxwdog-client

Source0:        https://fedorahosted.org/released/nuxwdog/%{name}-%{version}.tar.gz

# Note: there is an rpmlint warning about Nuxwdogclient.so being a private-shared-object-provide
# This would ordinarily be fixed by calling the macro perl_default_filter, but 
# this disables rpms file coloring and makes the package fail multilib tests.

%if 0%{?rhel}
ExcludeArch: ppc ppc64 ppcle ppc64le s390 s390x
%endif

%description
The nuxwdog package supplies the nuxwdog watchdog daemon, 
used to start,stop, prompt for passwords and monitor processes.
It also contains C/C++ and Perl client code to allow clients to
interact with the nuxwdog watchdog daemon.

%package devel
Group:        Development/Libraries
Summary:      Development files for the Nuxwdog Watchdog
Requires:     %{name} = %{version}-%{release}
Obsoletes:    nuxwdog-client-devel

%description devel
The nuxwdog-devel package contains the header files needed to build clients
that call WatchdogClient functions, so that clients can interact with the
nuxwdog watchdog server.

%package client-java
Group:        System Environment/Libraries
Summary:      Nuxwdog Watchdog client JNI Package
Requires:     java-headless >= 1:1.6.0
Requires:     jpackage-utils
Requires:     %{name} = %{version}-%{release}

%description client-java
The nuxwdog-client-java package contains a JNI interface to the nuxwdog 
client code, so that Java clients can interact with the nuxwdog watchdog 
server.

%package client-perl
Summary:      Nuxwdog Watchdog client perl bindings
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:     %{name} = %{version}-%{release}

%description client-perl
The nuxwdog-client-perl package contains a perl interface to nuxwdog.

%prep
%setup -q -n %{name}-%{version}

sed -i \
  -e 's,^NUXWDOGCLIENT_DOCUMENTATION=${NUXWDOGCLIENT_BUILD_PREFIX}/.*$,NUXWDOGCLIENT_DOCUMENTATION=${NUXWDOGCLIENT_BUILD_PREFIX}%{_pkgdocdir},' setup_package

%build
ant \
    -Dproduct.ui.flavor.prefix="" \
    -Dproduct.prefix="" \
    -Dproduct="nuxwdog" \
    -Dversion="%{version}"
%configure  --disable-static  \
%if 0%{?__isa_bits} == 64
    --enable-64bit \
%endif
    --docdir=%{_pkgdocdir}
make licensedir=%{_pkgdocdir}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p" licensedir=%{_pkgdocdir}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot}/%{perl_vendorarch} -name .packlist |xargs rm -f {}
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -name "perllocal.pod" |xargs rm -f {}
%{_fixperms} %{buildroot}/%{perl_vendorarch}/*

mkdir -p %{buildroot}/%{_libdir}/nuxwdog-jni
mv %{buildroot}/%{_libdir}/libnuxwdog-jni.so  %{buildroot}/%{_libdir}/nuxwdog-jni
mv %{buildroot}%{_usr}/jars/nuxwdog.jar %{buildroot}/%{_libdir}/nuxwdog-jni/nuxwdog-%{version}.jar
mkdir -p %{buildroot}%{_jnidir}
cd %{buildroot}/%{_jnidir}
ln -s %{_libdir}/nuxwdog-jni/nuxwdog-%{version}.jar nuxwdog.jar
rm -rf %{buildroot}%{_usr}/jars

%post -p /sbin/ldconfig 

%postun -p /sbin/ldconfig

%files
%_pkgdocdir
%{_bindir}/*
%{_libdir}/libnuxwdog.so.*
%{_mandir}/man1/nuxwdog.1*

%files devel
%{_includedir}/nuxwdog/
%{_libdir}/libnuxwdog.so

%files client-java
%{_libdir}/nuxwdog-jni/
%{_jnidir}/*

%files client-perl
%{perl_vendorarch}/Nuxwdogclient.pm
%{perl_vendorarch}/auto/Nuxwdogclient
%{_mandir}/man3/Nuxwdogclient.3pm*

%changelog
* Tue Jul 24 2018 Dogtag PKI Team <pki-devel@redhat.com> 1.0.4
- To list changes in <branch> since <tag>:
$ git log --pretty=oneline --abbrev-commit --no-decorate <tag>..<branch>