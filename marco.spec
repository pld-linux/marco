# TODO
# - subpackages for themes (see metacity.spec)
# - find proper packages for %files
#
Summary:	MATE Desktop window manager
Summary(pl.UTF-8):	Zarządca okien środowiska MATE Desktop
Name:		marco
Version:	1.28.1
Release:	1
License:	LGPL v2+ and GPL v2+
Group:		X11/Window Managers
Source0:	https://pub.mate-desktop.org/releases/1.28/%{name}-%{version}.tar.xz
# Source0-md5:	1d627834570fb84b0145b2715ed4c46c
URL:		https://wiki.mate-desktop.org/mate-desktop/components/marco/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.68.0
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libgtop-devel >= 2.0
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.27.1
BuildRequires:	pango-devel >= 1:1.2.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	startup-notification-devel >= 0.7
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel >= 0.3
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXpresent-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXres-devel >= 1.2.0
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.68.0
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.22.0
Requires:	mate-icon-theme
Requires:	mate-settings-daemon
Requires:	zenity
Suggests:	mate-control-center
# can use any gtk+2 themes nicely, Adwaita specially
Suggests:	%{name}-themes
Obsoletes:	mate-window-manager < 1.8.0
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
Requires:	glib2 >= 1:2.68.0
Requires:	gtk+3 >= 3.22.0
Requires:	mate-desktop-libs >= 1.27.1
Requires:	pango >= 1:1.2.0
Requires:	startup-notification >= 0.7
Requires:	xorg-lib-libXcomposite >= 0.3
Requires:	xorg-lib-libXres >= 1.2.0
Obsoletes:	mate-window-manager-libs < 1.8.0

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
Requires:	glib2-devel >= 1:2.68.0
Requires:	gtk+3-devel >= 3.22.0
Requires:	mate-desktop-devel >= 1.27.1
Obsoletes:	mate-window-manager-devel < 1.8.0

%description devel
Development files for Marco (Mate window manager).

%description devel -l pl.UTF-8
Pliki programistyczne Marco (zarządcy okien MATE).

%package themes
Summary:	Themes for MATE Window Manager
Summary(pl.UTF-8):	Motywy dla zarządcy okien MATE
Group:		Themes/GTK+
Requires:	%{name} = %{version}-%{release}
Obsoletes:	mate-window-manager-themes < 1.8.0

%description themes
Themes for MATE Window Manager.

%description themes -l pl.UTF-8
Motywy dla zarządcy okien MATE

%prep
%setup -q

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

# ku_IQ is outdated version of ku; the rest not supported by glibc
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,ie,jv,ku_IQ}

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
%attr(755,root,root) %ghost %{_libdir}/libmarco-private.so.2

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
%{_datadir}/themes/Atlanta
%{_datadir}/themes/ClearlooksRe
%{_datadir}/themes/Dopple-Left
%{_datadir}/themes/Dopple
%{_datadir}/themes/DustBlue
%{_datadir}/themes/Esco
%{_datadir}/themes/Gorilla
%{_datadir}/themes/Motif
%{_datadir}/themes/Raleigh
%{_datadir}/themes/Spidey-Left
%{_datadir}/themes/Spidey
%{_datadir}/themes/Splint-Left
%{_datadir}/themes/Splint
%{_datadir}/themes/WinMe
%{_datadir}/themes/eOS
