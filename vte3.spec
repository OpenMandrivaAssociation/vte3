%define api3		2.91
%define apigtk4               3.91

%define lib3_major	0
%define lib3_name	%mklibname vte %{api3} %{lib3_major}
%define gir3name	%mklibname vte-gir %{api3}
%define develname3	%mklibname -d %{name}
#--------------
%define libgtk4name     %mklibname vte-gtk4_ %{api3} %{lib3_major}
%define girgtk4name     %mklibname vte-gir %{apigtk4}
%define develgtk4name   %mklibname -d %{name}-gtk4

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name:		vte3
Version:	0.72.0
Release:	1
Summary:	A terminal emulator widget
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org/
Source0:	https://download.gnome.org/sources/vte/%{url_ver}/vte-%{version}.tar.xz

BuildRequires: pkgconfig(gi-docgen)
BuildRequires: pkgconfig(cairo-xlib)
BuildRequires: pkgconfig(fribidi)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(glib-2.0) >= 2.26.0
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gtk+-3.0) >= 3.1.9
BuildRequires: pkgconfig(gtk4)
BuildRequires: pkgconfig(pango) >= 1.22.0
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(gnutls)
BuildRequires: pkgconfig(libpcre2-8)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: automake
BuildRequires: cmake
BuildRequires: gtk-doc
BuildRequires: gobject-introspection-devel
BuildRequires: intltool
BuildRequires: vala-devel
BuildRequires: gperf
BuildRequires: meson
Requires:	%{name}-profile

%description
VTE is a terminal emulator widget for use with GTK+ 3.0.

%package -n %{lib3_name}
Summary:	A terminal emulator widget
Group:		System/Libraries
Requires:	%{name} >= %{version}

%description -n %{lib3_name}
VTE is a terminal emulator widget for use with GTK+ 3.0.

%package -n %{develname3}
Summary:	Files needed for developing applications which use VTE
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires: 	%{lib3_name} = %{version}-%{release}
Requires:	%{gir3name} = %{version}-%{release}

%description -n %{develname3}
VTE is a terminal emulator widget for use with GTK+ 3.0.  This
package contains the files needed for building applications using VTE.

%package -n %{gir3name}
Summary:	GObject Introspection interface description for vte with GTK+ 3.0
Group:		System/Libraries
Requires:	%{lib3_name} = %{version}-%{release}
Conflicts:	%{lib3_name} < 0.28.1-2

%description -n %{gir3name}
GObject Introspection interface description for vte with GTK+ 3.0.

%package profile
Summary:	Profile script for VTE terminal emulator library
BuildArch:	noarch
Conflicts:	%{name} < 0.37.90-2

%description profile
This package package contains a profile.d script for the VTE terminal
emulator library.

#--------------------
%package -n %{libgtk4name}
Summary:        GTK4 terminal emulator library
Group:          System/Libraries
Requires:       %{name} >= %{version}-%{release}
 
%description -n %{libgtk4name}
VTE is a library implementing a terminal emulator widget for GTK 4. VTE
is mainly used in gnome-terminal, but can also be used to embed a console/terminal in games, editors, IDEs, etc.

%package -n %{develgtk4name}
Summary:        Files needed for developing applications which use VTE for GTK+ 4
Group:          Development/C
Requires:       %{libgtk4name} = %{version}-%{release}
Requires:       %{girgtk4name} = %{version}-%{release}

%description -n %{develgtk4name}
VTE is a terminal emulator widget for use with GTK+ 4.0.  This
package contains the files needed for building applications using VTE.

%package -n %{girgtk4name}
Summary:        GObject Introspection interface description for vte with GTK+ 4.0
Group:          System/Libraries
Requires:       %{libgtk4name} = %{version}-%{release}

%description -n %{girgtk4name}
GObject Introspection interface description for vte with GTK+ 4.0.


%prep
%setup -qn vte-%{version}
%autopatch -p1

%build
export CXXFLAGS="%{optflags} -std=c++20"
# Build 0.68.0 failing with clang 14. ld.lld: error: undefined symbol: void std::__cxx11::basic_string<char32_t, std::char_traits<char32_t>, 
# std::allocator<char32_t> >::_M_construct<char32_t const*>(char32_t const*, char32_t const*, std::forward_iterator_tag)
export CC=gcc
export CXX=g++
%meson  \
          --buildtype=release \
          -Ddocs=true \
          -Dgtk3=true \
          -Dgtk4=true
%meson_build

%install
%meson_install

#we don't want these
find %{buildroot} -name "*.la" -delete
%find_lang vte-%{api3}

%files -f vte-%{api3}.lang
%{_bindir}/vte-%{api3}
%{_bindir}/vte-%{api3}-gtk4
%{_libexecdir}/vte-urlencode-cwd
%{_userunitdir}/vte-spawn-.scope.d/defaults.conf
%{_datadir}/glade/catalogs/vte-%{api3}.xml
%{_datadir}/glade/pixmaps/hicolor/*x*/actions/widget-vte-terminal.png

%files profile
%{_sysconfdir}/profile.d/vte.sh
%{_sysconfdir}/profile.d/vte.csh

%files -n %{lib3_name}
%{_libdir}/libvte-%{api3}.so.%{lib3_major}.*
%{_libdir}/libvte-%{api3}.so.0

%files -n %{gir3name}
%{_libdir}/girepository-1.0/Vte-%{api3}.typelib

%files -n %{develname3}
%doc %{_datadir}/doc/vte-*
%{_includedir}/vte-%{api3}
%{_libdir}/libvte-%{api3}.so
%{_libdir}/pkgconfig/vte-%{api3}.pc
%{_datadir}/gir-1.0/Vte-%{api3}.gir
%{_datadir}/vala/vapi/vte-%{api3}.vapi
%{_datadir}/vala/vapi/vte-2.91.deps

#-----------------
%files -n %{libgtk4name}
%{_libdir}/libvte-%{api3}-gtk4.so.%{lib3_major}{,.*}

%files -n %{girgtk4name}
%{_libdir}/girepository-1.0/Vte-%{apigtk4}.typelib

%files -n %{develgtk4name}
%{_includedir}/vte-%{api3}-gtk4/
%{_libdir}/libvte-%{api3}-gtk4.so
%{_libdir}/pkgconfig/vte-%{api3}-gtk4.pc
%{_datadir}/gir-1.0/Vte-%{apigtk4}.gir
%{_datadir}/vala/vapi/vte-%{api3}-gtk4.deps
%{_datadir}/vala/vapi/vte-%{api3}-gtk4.vapi
