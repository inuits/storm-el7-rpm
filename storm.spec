%define __jar_repack 0
%define debug_package %{nil}
%define name         apache-storm
%define _prefix      /opt
%define _conf_dir    %{_sysconfdir}/storm
%define _log_dir     %{_var}/log/storm
%define _data_dir    %{_sharedstatedir}/storm

Summary: Apache Storm is a free and open source distributed realtime computation system
Name: apache-storm
Version: %{version}
Release: %{build_number}
License: Apache License, Version 2.0
Group: Applications/Processing
URL: http://storm.apache.org/
Source0: apache-storm-%{version}.tar.gz
Source1: storm-nimbus.service
Source2: storm-supervisor.service
Source3: storm-logviewer.service
Source4: storm-ui.service
Source5: storm.logrotate
Source6: storm.yaml
Source7: storm_env.ini
Source8: storm.sysconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}
Vendor: Apache Software Foundation
Packager: Tom Van den Abbeele <tom.vda@inuits.eu>
Provides: storm
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Apache Storm is a free and open source distributed realtime computation system. Storm makes it easy to reliably process unbounded streams of data, doing for realtime processing what Hadoop did for batch processing. Storm is simple, can be used with any programming language, and is a lot of fun to use!
Storm has many use cases: realtime analytics, online machine learning, continuous computation, distributed RPC, ETL, and more. Storm is fast: a benchmark clocked it at over a million tuples processed per second per node. It is scalable, fault-tolerant, guarantees your data will be processed, and is easy to set up and operate.
Storm integrates with the queueing and database technologies you already use. A Storm topology consumes streams of data and processes those streams in arbitrarily complex ways, repartitioning the streams between each stage of the computation however needed. Read more in the tutorial.

%prep
%setup

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/storm/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/storm/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/storm/external
mkdir -p $RPM_BUILD_ROOT%{_prefix}/storm/extlib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/storm/extlib-daemon
mkdir -p $RPM_BUILD_ROOT%{_prefix}/storm/log4j2
mkdir -p $RPM_BUILD_ROOT%{_prefix}/storm/public
mkdir -p $RPM_BUILD_ROOT%{_log_dir}
mkdir -p $RPM_BUILD_ROOT%{_data_dir}
mkdir -p $RPM_BUILD_ROOT%{_conf_dir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp -pr bin $RPM_BUILD_ROOT%{_prefix}/storm/
cp -pr lib $RPM_BUILD_ROOT%{_prefix}/storm/
cp -pr external $RPM_BUILD_ROOT%{_prefix}/storm/
cp -pr log4j2 $RPM_BUILD_ROOT%{_prefix}/storm/
cp -pr public $RPM_BUILD_ROOT%{_prefix}/storm/
install -p -D -m 755 %{S:1} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 755 %{S:2} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 755 %{S:3} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 755 %{S:4} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 644 %{S:5} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/storm
install -p -D -m 644 %{S:6} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:7} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/storm

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group storm >/dev/null || /usr/sbin/groupadd -r storm
if ! /usr/bin/getent passwd storm >/dev/null ; then
    /usr/sbin/useradd -r -g storm -m -d %{_prefix}/storm -s /bin/bash -c "Storm" storm
fi

%post
%systemd_post storm-nimbus.service
%systemd_post storm-supervisor.service
%systemd_post storm-logviewer.service
%systemd_post storm-ui.service

%preun
%systemd_preun storm-nimbus.service
%systemd_preun storm-supervisor.service
%systemd_preun storm-logviewer.service
%systemd_preun storm-ui.service

%files
%defattr(-,root,root)
%{_unitdir}/storm-nimbus.service
%{_unitdir}/storm-supervisor.service
%{_unitdir}/storm-logviewer.service
%{_unitdir}/storm-ui.service
%config(noreplace) %{_sysconfdir}/logrotate.d/storm
%config(noreplace) %{_sysconfdir}/sysconfig/storm
%config(noreplace) %{_conf_dir}/*
%attr(-,storm,storm) %{_prefix}/storm
%attr(0755,storm,storm) %dir %{_log_dir}
%attr(0700,storm,storm) %dir %{_data_dir}

