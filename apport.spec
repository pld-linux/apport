Summary:	Read, write, and modify problem reports
Name:		apport
Version:	0.106
Release:	1
License:	GPL
Group:		Applications/System
Source0:	https://launchpad.net/ubuntu/hardy/+source/apport/%{version}/+files/%{name}_%{version}.tar.gz
# Source0-md5:	128c5b362708bc9e54e4bd167075d45d
Source1:	%{name}.init
URL:		https://wiki.ubuntu.com/Apport
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	python-devel >= 1:2.5
#BuildRequires:	tetex-format-pdflatex
#BuildRequires:	tetex-latex
# Need the ability to use pipes in /proc/sys/kernel/core_pattern
# seems only 2.6.24 allows command line params
Requires:	uname(release) >= 2.6.24
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun):	/sbin/service
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires:	python-rpm
Requires:	yum
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
apport automatically collects data from crashed processes and compiles
a problem report in /var/crash/.

This package also provides apport's python libraries and a command
line frontend for browsing and handling the crash reports.

See https://wiki.ubuntu.com/AutomatedProblemReports for more
information.

%package gtk
Summary:	GTK frontend for the apport crash report system
Group:		Applications/System
Requires:	procps
Requires:	python-pygtk-gtk
Requires:	python-pygtk-glade
Requires:	python-pyxdg

%description gtk
apport automatically collects data from crashed processes and compiles
a problem report in /var/crash/.

This package provides a GTK frontend for browsing and handling the
crash reports.

%package qt
Summary:	Qt4 frontend for the apport crash report system
Group:		Applications/System
Requires:	procps
Requires:	python-PyQT
Requires:	python-pyxdg

%description qt
apport automatically collects data from crashed processes and compiles
a problem report in /var/crash/.

This package provides a Qt4 frontend for browsing and handling the
crash reports.

%package retrace
Summary:	Tools for reprocessing Apport crash reports
Group:		Applications/System

%description retrace
apport-retrace recombines an Apport crash report (either a file or a
Launchpad bug) and debug symbol packages (.ddebs) into fully symbolic
stack traces.

This package also ships apport-chroot. This tool can create and manage
chroots for usage with apport-retrace. If the fakeroot and fakechroot
libraries are available (either by installing the packages or by
merely putting their libraries somewhere and setting two environment
variables), the entire process of retracing crashes in chroots can
happen with normal user privileges.

%prep
%setup -q -n ubuntu

%build
python setup.py build
%{__make} -C po
%{__make} -C gtk
%{__make} -C qt4
#%{__make} -C doc
# set up the packaging backend
cp backends/packaging_rpm.py backends/packaging_fedora.py apport
ln -s packaging_fedora.py apport/packaging_impl.py

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT \
	--install-scripts %{_datadir}/apport

%py_postclean

# Do the man pages
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install man/apport-*.1 $RPM_BUILD_ROOT%{_mandir}/man1
# cron job
install -d $RPM_BUILD_ROOT/etc/cron.daily
install debian/apport.cron.daily $RPM_BUILD_ROOT/etc/cron.daily/apport
# create the dir for crash reports
install -d $RPM_BUILD_ROOT/var/crash
# install initscript
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %SOURCE1 $RPM_BUILD_ROOT/etc/rc.d/init.d/apport

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Add proper symlinks in %{_sysconfdir}/rc*.d
/sbin/chkconfig --add apport
%update_mime_database
%update_icon_cache hicolor

%preun
if [ "$1" == "0" ]; then
    %service apport stop > /dev/null
    /sbin/chkconfig --del apport
fi

%postun
if [ "$1" -ge "1" ]; then
    %service apport condrestart > /dev/null || :
fi
%update_mime_database
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%dir /var/crash
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/apport.svg
%{_datadir}/mime/packages/apport.xml
%{py_sitescriptdir}/apport-0.0.0-py*.egg-info
%dir %{_datadir}/apport
%attr(755,root,root) %{_datadir}/apport/apport
%attr(755,root,root) %{_datadir}/apport/apport-cli
%attr(755,root,root) %{_datadir}/apport/gcc_ice_hook
%attr(755,root,root) %{_datadir}/apport/apport-checkreports
%attr(755,root,root) %{_datadir}/apport/package_hook
%attr(755,root,root) %{_datadir}/apport/kernel_hook
%attr(755,root,root) %{_datadir}/apport/apport-unpack
%attr(755,root,root) %{_datadir}/apport/testsuite/
%dir %{_datadir}/apport/general-hooks/
%attr(755,root,root) %{_datadir}/apport/general-hooks/*.py
%dir %{_datadir}/apport/package-hooks/
%attr(755,root,root) %{_datadir}/apport/package-hooks/*.py
%{py_sitescriptdir}/apport_python_hook.py[co]
%{py_sitescriptdir}/problem_report*.py[co]
%dir %{py_sitescriptdir}/apport
%{py_sitescriptdir}/apport/*.py[co]
%dir %{py_sitescriptdir}/apport/crashdb_impl
%{py_sitescriptdir}/apport/crashdb_impl/*.py[co]
%{_sysconfdir}/cron.daily/apport
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/apport
%dir %{_sysconfdir}/apport
%config %{_sysconfdir}/apport/crashdb.conf
%{_sysconfdir}/apport/blacklist.d

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_datadir}/apport/apport-gtk
%{_datadir}/apport/apport-gtk.glade

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_datadir}/apport/apport-qt
%{_datadir}/apport/*.ui

%files retrace
%defattr(644,root,root,755)
%{_mandir}/man1/apport-retrace.1*
%attr(755,root,root) %{_datadir}/apport/apport-retrace
%attr(755,root,root) %{_datadir}/apport/apport-chroot
%attr(755,root,root) %{_datadir}/apport/dupdb-admin
