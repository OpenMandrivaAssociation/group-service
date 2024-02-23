%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

Summary:	Borrowing DBUS services to manage user groups
Name:		group-service
Version:	1.4.0
Release:	1
License:	GPLv3+
Group:		System/Libraries
URL:		https://github.com/zhuyaliang/%{name}
Source0:	https://github.com/zhuyaliang/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	meson
BuildRequires:	gettext
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libxcrypt)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-rpm-macros

Requires:	polkit
Requires:	shadow
Requires:	%{libname} = %{EVRD}
%{?systemd_requires}

%description
Using Dbus to manage user groups, you can complete the
addition and deletion of user groups, add/remove users
to groups, and change the name of user groups.

%files -f %{name}.lang
%doc README.md
%license COPYING
%{_sysconfdir}/dbus-1/system.d/org.group.admin.conf
%{_libexecdir}/group-admin-daemon
%{_datadir}/dbus-1/interfaces/org.group.admin.list.xml
%{_datadir}/dbus-1/interfaces/org.group.admin.xml
%{_datadir}/dbus-1/system-services/org.group.admin.service
%{_datadir}/polkit-1/actions/org.group.admin.policy
%{_unitdir}/group-admin-daemon.service

#-----------------------------------------------------------------------

%package -n %{libname}
Summary:	Client-side library to talk to group-service
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the shared library for %{name}.

%files -n %{libname}
%{_libdir}/libgroup-service.so.%{major}*

#-----------------------------------------------------------------------

%package -n %{devname}
Summary:	Support for developing back-ends for group-service
Requires:	%{name} = %{version}-%{release}

%description -n %{devname}
This package contains libraries and header files needed for
group-service back-ends development.

%files -n %{devname}
%{_includedir}/group-service-1.0/
%{_libdir}/libgroup-service.so
%{_libdir}/pkgconfig/group-service.pc

#-----------------------------------------------------------------------


%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

# locales
%find_lang %{name} --with-gnome --all-name

%post
%systemd_post group-admin-daemon.service

%preun
%systemd_preun group-admin-daemon.service

%postun
%systemd_postun group-admin-daemon.service

