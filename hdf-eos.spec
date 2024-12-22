#
# Conditional build:
%bcond_without	szip		# SZIP support (must match hdf build bcond)
%bcond_without	tests		# unit tests
#
Summary:	HDF-EOS 2 library
Summary(pl.UTF-8):	Biblioteka HDF-EOS 2
Name:		hdf-eos
Version:	3.0
Release:	2
License:	MIT-like
Group:		Libraries
Source0:	https://git.earthdata.nasa.gov/projects/DAS/repos/hdfeos/raw/hdf-eos2-%{version}-src.tar.gz?at=3128a738021501c821549955f6c78348e5f33850#/hdf-eos2-%{version}-src.tar.gz
# Source0-md5:	1b8660bac298c0ae6c2c56e76fbe8623
Patch0:		hdf-eos2-config.patch
Patch1:		%{name}-link.patch
Patch2:		stack-overuse.patch
Patch3:		hdf-eos2-includes.patch
Patch4:		hdf-eos2-types.patch
Patch5:		hdf-eos2-api-const.patch
URL:		http://hdfeos.org/software/library.php#HDF-EOS2
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	hdf-devel >= 4.2.13
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
%{?with_szip:BuildRequires:	libaec-szip-devel >= 1.0}
BuildRequires:	zlib-devel >= 1.2.11
Requires:	hdf >= 4.2.13
%{?with_szip:Requires:	libaec-szip >= 1.0}
Requires:	zlib >= 1.2.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HDF-EOS is a software library designed to support EOS-specific data
structures, namely Grid, Point, and Swath. The new data structures are
constructed from standard HDF data objects, using EOS conventions,
through the use of a software library. A key feature of HDF-EOS files
is that instrument-independent services, such as subsetting by
geolocation, can be applied to the files across a wide variety of data
products. The library is extensible and new data structures can be
added.

%description -l pl.UTF-8
HDF-EOS to biblioteka programowa zaprojektowana w celu obsługi
struktur danych związanych z EOS, takich jak Grid, Point i Swath. Nowe
struktury danych są tworzone z obiektów danych HDF, przy użyciu
konwencji EOS, poprzez bibliotekę programową. Kluczową cechą plików
HDF-EOS jest to, że usługi niezależne od przyrządu, takie jak na
przykład podział według geolokalizacji, można wykonywać na plikach
zawierających różnorodne zbiory danych. Biblioteka jest rozszerzalna i
pozwala na dodawanie nowych struktur danych.

%package devel
Summary:	Header files for HDF-EOS 2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HDF-EOS 2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	hdf-devel >= 4.2.13
Requires:	libjpeg-devel
%{?with_szip:Requires:	libaec-szip-devel >= 1.0}
Requires:	zlib-devel >= 1.2.11

%description devel
Header files for HDF-EOS 2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HDF-EOS 2.

%package static
Summary:	Static HDF-EOS 2 library
Summary(pl.UTF-8):	Statyczna biblioteka HDF-EOS 2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HDF-EOS 2 library.

%description static -l pl.UTF-8
Statyczna biblioteka HDF-EOS 2.

%prep
%setup -q -n hdf-eos2-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# as hdf 4 extension, use the same include dir as hdf 4
%configure \
	--includedir=%{_includedir}/hdf \
	--enable-shared \
	%{?with_szip:--with-szlib}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/README
%attr(755,root,root) %{_libdir}/libGctp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGctp.so.0
%attr(755,root,root) %{_libdir}/libhdfeos.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhdfeos.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGctp.so
%attr(755,root,root) %{_libdir}/libhdfeos.so
%{_libdir}/libGctp.la
%{_libdir}/libhdfeos.la
%{_includedir}/hdf/HdfEosDef.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libGctp.a
%{_libdir}/libhdfeos.a
