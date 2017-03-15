# TODO
# - subpackages for themes (see metacity.spec)
# - find proper packages for %files
#
Summary:	MATE Desktop window manager
Summary(pl.UTF-8):	Zarządca okien środowiska MATE Desktop
Name:		marco
Version:	1.18.0
Release:	1
License:	LGPL v2+ and GPL v2+
Group:		X11/Window Managers
Source0:	http://pub.mate-desktop.org/releases/1.18/%{name}-%{version}.tar.xz
# Source0-md5:	c0d14cd1d2524e460cb84819cbd863ea
# https://bugzilla.gnome.org/show_bug.cgi?id=622517
Patch0:		Allow-breaking-out-from-maximization-during-mouse.patch
# https://bugs.launchpad.net/ubuntu/+source/metacity/+bug/583847
Patch1:		initialise_all_workspace_names.patch
URL:		http://wiki.mate-desktop.org/mate-window-manager
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	gettext-tools >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gtk+3-devel >= 3.14
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libgtop-devel
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.9.3
BuildRequires:	pango-devel >= 1:1.2.0
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	startup-notification-devel >= 0.7
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel >= 0.3
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.32.0
Requires:	gsettings-desktop-schemas
Requires:	mate-icon-theme
Requires:	mate-settings-daemon
Requires:	zenity
Suggests:	mate-control-center
# can use any gtk+2 themes nicely, Adwaita specially
Suggests:	%{name}-themes
Obsoletes:	mate-window-manager
Obsoletes:	mate-window-manager-libs < 1.4.1-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE Desktop window manager. MATE Marco is a fork of GNOME Metacity.

%description -l pl.UTF-8
Zarządca okien środowiska MATE Desktop. MATE Marco to odgałęzienie
pakietu GNOME Metacity.

%package libs
Summary:	Marco (MATE window manager) library
Summary(pl.UTF-8):	Biblioteka Macro (zarządcy okien MATE)
Group:		X11/Libraries
Requires:	glib2 >= 1:2.32.0
Requires:	gtk+3 >= 3.14
Requires:	mate-desktop-libs >= 1.9.3
Requires:	pango >= 1:1.2.0
Requires:	startup-notification >= 0.7
Requires:	xorg-lib-libXcomposite >= 0.3
Obsoletes:	mate-window-manager-libs >= 1.4.1-2

%description libs
This package contains the shared library for Marco, the MATE window
manager.

%description libs -l pl.UTF-8
Pakiet zawierający bibliotekę współdzieloną Marco (zarządcy okien
MATE).

%package devel
Summary:	Development files for Marco (Mate window manager)
Summary(pl.UTF-8):	Pliki programistyczne Marco (zarządcy okien MATE)
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	gtk+3-devel >= 3.14
Requires:	mate-desktop-devel >= 1.9.3
Obsoletes:	mate-window-manager-devel

%description devel
Development files for Marco (Mate window manager).

%description devel -l pl.UTF-8
Pliki programistyczne Marco (zarządcy okien MATE).

%package themes
Summary:	Themes for MATE Window Manager
Summary(pl.UTF-8):	Motywy dla zarządcy okien MATE
Group:		Themes/GTK+
Requires:	%{name} = %{version}-%{release}
Obsoletes:	mate-window-manager-themes

%description themes
Themes for MATE Window Manager.

%description themes -l pl.UTF-8
Motywy dla zarządcy okien MATE

%prep
%setup -q
%patch0 -p1
#patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	ZENITY=%{_bindir}/zenity \
	--disable-scrollkeeper \
	--disable-silent-rules \
	--disable-static \
	--with-gnu-ld \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmarco-private.la

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{ku_IQ,jv}

desktop-file-install \
	--remove-category="MATE" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/marco.desktop

%find_lang %{name} --all-name --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/marco
%attr(755,root,root) %{_bindir}/marco-message
%{_datadir}/marco
%{_datadir}/mate-control-center/keybindings/50-marco*.xml
%dir %{_datadir}/mate/wm-properties
%{_datadir}/mate/wm-properties/marco-wm.desktop
%{_datadir}/glib-2.0/schemas/org.mate.marco.gschema.xml
%{_desktopdir}/marco.desktop
%{_mandir}/man1/marco.1*
%{_mandir}/man1/marco-message.1*

# TODO: find better packages
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmarco-private.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmarco-private.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/marco-theme-viewer
%attr(755,root,root) %{_bindir}/marco-window-demo
%attr(755,root,root) %{_libdir}/libmarco-private.so
%{_includedir}/marco-1
%{_pkgconfigdir}/libmarco-private.pc
%{_mandir}/man1/marco-theme-viewer.1*
%{_mandir}/man1/marco-window-demo.1*

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
