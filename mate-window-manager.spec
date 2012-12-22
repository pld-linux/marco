# TODO
# - subpackages for themes (see metacity.spec)
# - -libs subpackage
#rpm -Uhv  mate-window-manager-devel-1.5.2-0.4.i686.rpm
#        libmarco-private.so.0 is needed by mate-window-manager-devel-1.5.2-0.4.i686
#        mate-window-manager = 1.5.2-0.4 is needed by mate-window-manager-devel-1.5.2-0.4.i686
Summary:	MATE Desktop window manager
Name:		mate-window-manager
Version:	1.5.2
Release:	0.4
License:	LGPLv2+ and GPLv2+
Group:		X11/Window Managers
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# https://bugzilla.gnome.org/show_bug.cgi?id=622517
Patch0:		Allow-breaking-out-from-maximization-during-mouse.patch
# https://bugs.launchpad.net/ubuntu/+source/metacity/+bug/583847
Patch1:		initialise_all_workspace_names.patch
# upstream patch
# https://github.com/mate-desktop/mate-window-manager/commit/6404a98fb79e7bb4c3e9c5ca9919e12c946679d7
Patch2:		0001-fix-startup-rendering-effect-with-composite-enabled.patch
URL:		http://mate-desktop.org/
BuildRequires:	desktop-file-utils
BuildRequires:	mate-common
BuildRequires:	mate-dialogs
BuildRequires:	pkgconfig(MateCORBA-2.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra)
BuildRequires:	pkgconfig(libcanberra-gtk)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(mate-doc-utils)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Suggests:	mate-control-center
Requires(post):	/sbin/ldconfig
Obsoletes:	mate-window-manager-libs < 1.4.1-2
# http://bugzilla.redhat.com/873342
#Provides:	firstboot(windowmanager) = mate-window-manager

#filter_from_requires /^libmarco-private.so/d;

%description
MATE Desktop window manager

%package devel
Summary:	Development files for mate-window-manager
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for mate-window-manager

%prep
%setup -q
%patch0 -p1
#patch1 -p1
%patch2 -p1
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
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

find $RPM_BUILD_ROOT -name '*.la' -exec rm -vf {} ';'

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
%{_datadir}/marco
%{_datadir}/mate-control-center/keybindings/50-marco*.xml
%{_datadir}/mate/help/creating-marco-themes/C/creating-marco-themes.xml
%{_datadir}/mate/wm-properties
%{_datadir}/glib-2.0/schemas/org.mate.marco.gschema.xml
%{_mandir}/man1/marco.1.*
%{_mandir}/man1/marco-message.1.*

# -libs
%attr(755,root,root) %{_libdir}/libmarco-private.so.*.*.*
%ghost %{_libdir}/libmarco-private.so.0

# XXX find proper packages
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings
%dir %{_datadir}/mate/help/creating-marco-themes
%dir %{_datadir}/mate/help/creating-marco-themes/C

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/marco-theme-viewer
%attr(755,root,root) %{_bindir}/marco-window-demo
%{_includedir}/marco-1
%{_libdir}/libmarco-private.so
%{_pkgconfigdir}/libmarco-private.pc
%{_mandir}/man1/marco-theme-viewer.1.*
%{_mandir}/man1/marco-window-demo.1.*
