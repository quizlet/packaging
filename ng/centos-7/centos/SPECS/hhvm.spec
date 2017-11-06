Name:             hhvm
Version:          3.22.0
Release:          1%{?dist}
Summary:          HHVM virtual machine, runtime, and JIT for the PHP and Hack languages

Group:            Development/Languages
License:          PHP / Zend
URL:              http://hhvm.com 
Vendor:           HHVM Open Source <hhvm-oss@fb.com>
Source0:           https://github.com/facebook/hhvm/archive/%{name}-%{version}.tar.gz

BuildRequires: ImageMagick-devel sqlite-devel tbb-devel bzip2-devel openldap-devel readline-devel
BuildRequires: elfutils-libelf-devel gmp-devel lz4-devel pcre-devel libxslt-devel libevent-devel
BuildRequires: yaml-devel vpx-devel png-devel zip-devel icu-devel mcrypt-devel memcached-devel
BuildRequires: cap-devel dwarf-devel libedit-devel libcurl-devel libxml2-devel xslt-devel glog-devel
BuildRequires: oniguruma-devel ocaml gperf enca libjpeg-turbo-devel openssl-devel expect-devel
BuildReuires: unixODBC-devel git psmisc binutils-devel boost-devel numactl-devel

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
HHVM is an open-source virtual machine designed for executing programs written in Hack and PHP.
HHVM uses a just-in-time (JIT) compilation approach to achieve superior performance while
maintaining the development flexibility that PHP provides.

%prep
%setup -q -n %{name}-%{version}

%pre
getent group hhvm >/dev/null || groupadd -r hhvm
getent passwd hhvm >/dev/null || \
    useradd -r -g hhvm -d %{hhvm_dir} -s /sbin/nologin -c "HHVM" hhvm
exit 0

%build
export HPHP_HOME=`pwd`
git submodule update --init --recursive
cmake3 -DCMAKE_INSTALL_PREFIX:PATH=/usr .
make -j8

%install
make install

%files
%defattr(-,hhvm,hhvm,-)
%{_unitdir}/hhvm.service
%dir %{_var}/hhvm
%dir %{_var}/run/%{name}
%dir %{_var}/log/%{name}

%defattr(-,root,root,-)
%dir %{_sysconfdir}/hhvm
%config(noreplace) %{_sysconfdir}/hhvm/php.ini
%config(noreplace) %{_sysconfdir}/hhvm/server.hdf
%config(noreplace) %{_sysconfdir}/hhvm/config.hdf
%{_bindir}/hackfmt
%{_bindir}/hh_client
%{_bindir}/hh_parse
%{_bindir}/hh_server
%{_bindir}/hhvm
%{_bindir}/hhvm-repo-mode


%files devel
%defattr(-,root,root,-)
%{_prefix}/lib64/hhvm/hphpize/*
%{_prefix}/lib64/hhvm/CMake/*.cmake
%{_prefix}/lib64/hhvm/libpcre.a
%{_prefix}/lib64/hhvm/libpcreposix.a
%{_prefix}/lib64/hhvm/libpcrecpp.a
%{_prefix}/include/hhvm/pcre.h
%{_prefix}/include/hhvm/pcreposix.h
%{_prefix}/include/hhvm/pcrecpp.h
%{_prefix}/include/hhvm/pcre_scanner.h
%{_prefix}/include/hhvm/pcrecpparg.h
%{_prefix}/include/hhvm/pcre_stringpiece.h
%{_prefix}/bin/pcregrep
%{_prefix}/bin/pcretest
%{_prefix}/bin/pcrecpp_unittest
%{_prefix}/bin/pcre_scanner_unittest
%{_prefix}/bin/pcre_stringpiece_unittest
%{_prefix}/man/man3/*
%{_prefix}/share/doc/pcre/html/*

%doc CONTRIBUTING.md LICENSE.PHP LICENSE.ZEND README.md hphp/NEWS

%changelog

* Mon Nov 6 2017 Ryan Gordon <ryan@quizlet.com> - 3.22.0
- Initial built for centos7