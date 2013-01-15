# TODO
# - subpackages for themes (see metacity.spec)
# - find proper packages for %files
Summary:	MATE Desktop window manager
Name:		mate-window-manager
Version:	1.5.3
Release:	0.10
License:	LGPL v2+ and GPL v2+
Group:		X11/Window Managers
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	b3ce71f9db8563db1571f8ed80a543e3
# https://bugzilla.gnome.org/show_bug.cgi?id=622517
Patch0:		Allow-breaking-out-from-maximization-during-mouse.patch
# https://bugs.launchpad.net/ubuntu/+source/metacity/+bug/583847
Patch1:		initialise_all_workspace_names.patch
URL:		http://wiki.mate-desktop.org/mate-window-manager
BuildRequires:	desktop-file-utils
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libsoup-devel
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils
BuildRequires:	startup-notification-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Suggests:	mate-control-center
# can use any gtk+2 themes nicely, Adwaita specially
Suggests:	%{name}-themes
Requires(post):	/sbin/ldconfig
Requires:	mate-icon-theme
Requires:	mate-settings-daemon
Obsoletes:	mate-window-manager-libs < 1.4.1-2
# http://bugzilla.redhat.com/873342
#Provides:	firstboot(windowmanager) = mate-window-manager
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop window manager.

%package libs
Summary:	marco library
Summary(pl.UTF-8):	marco biblioteka
Group:		X11/Libraries

%description libs
This package contains libraries for MATE window manager.

%description libs -l pl.UTF-8
Pakiet zawierający biblioteki zarządcy okien MATE.

%package devel
Summary:	Development files for mate-window-manager
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for mate-window-manager

%package themes
Summary:	Themes for Mate Window Manager
Group:		Themes/GTK+
Requires:	%{name} = %{version}-%{release}

%description themes
Themes for Mate Window Manager.

%prep
%setup -q
%patch0 -p1
#patch1 -p1

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	MATEDIALOG=%{_bindir}/matedialog \
	--disable-static \
	--disable-scrollkeeper \
	--with-gnu-ld \
	--with-gtk=2.0 \
	--with-x

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmarco-private.la

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/marco.convert

desktop-file-install \
	--remove-category="MATE" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir}  \
$RPM_BUILD_ROOT%{_desktopdir}/marco.desktop

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_bindir}/marco
%attr(755,root,root) %{_bindir}/marco-message
%{_desktopdir}/marco.desktop
%{_datadir}/marco
%{_datadir}/mate-control-center/keybindings/50-marco*.xml
%{_datadir}/mate/help/creating-marco-themes/C/creating-marco-themes.xml
%{_datadir}/mate/wm-properties
%{_datadir}/glib-2.0/schemas/org.mate.marco.gschema.xml
%{_mandir}/man1/marco.1.*
%{_mandir}/man1/marco-message.1.*

# XXX find proper packages
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings
%dir %{_datadir}/mate/help/creating-marco-themes
%dir %{_datadir}/mate/help/creating-marco-themes/C

%files themes
%defattr(644,root,root,755)
%{_datadir}/themes/ClearlooksRe
%{_datadir}/themes/Dopple-Left
%{_datadir}/themes/Dopple
%{_datadir}/themes/DustBlue
%{_datadir}/themes/Spidey-Left
%{_datadir}/themes/Spidey
%{_datadir}/themes/Splint-Left
%{_datadir}/themes/Splint
%{_datadir}/themes/WinMe
%{_datadir}/themes/eOS

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmarco-private.so.*.*.*
%ghost %{_libdir}/libmarco-private.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/marco-theme-viewer
%attr(755,root,root) %{_bindir}/marco-window-demo
%{_includedir}/marco-1
%{_libdir}/libmarco-private.so
%{_pkgconfigdir}/libmarco-private.pc
%{_mandir}/man1/marco-theme-viewer.1.*
%{_mandir}/man1/marco-window-demo.1.*
