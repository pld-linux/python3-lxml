#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	tests		# unit tests

%define		module	lxml
Summary:	Python binding for the libxml2 and libxslt libraries
Summary(pl.UTF-8):	Wiązanie Pythona do bibliotek libxml2 i libxslt
Name:		python3-%{module}
Version:	5.3.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/lxml/
Source0:	https://files.pythonhosted.org/packages/source/l/lxml/%{module}-%{version}.tar.gz
# Source0-md5:	9d94cc157fb6db0c062ef80cdc0ed307
URL:		https://lxml.de/
BuildRequires:	libxml2-devel >= 1:2.9.2
BuildRequires:	libxslt-devel >= 1.1.28
BuildRequires:	pkgconfig
%if %{with python3}
BuildRequires:	python3-Cython >= 0.29.36-2
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lxml is a Pythonic binding for the libxml2 and libxslt libraries.

%description -l pl.UTF-8
lxml to pythonowe wiązanie do bibliotek libxml2 i libxslt.

%package apidocs
Summary:	lxml API documentation
Summary(pl.UTF-8):	Dokumentacja API modułu lxml
Group:		Documentation
BuildArch:	noarch

%description apidocs
lxml API documentation.

%description apidocs -l pl.UT8-8
Dokumentacja API modułu lxml.

%prep
%setup -q -n %{module}-%{version}

# force cython regeneration
%{__rm} src/lxml/{_elementpath.c,builder.c,etree.c,etree.h,etree_api.h,lxml.etree.h,lxml.etree_api.h,objectify.c,sax.c}

%build
%py3_build

%if %{with tests}
install -d testdir-3/src/lxml
cd testdir-3/src/lxml
ln -snf ../../../build-3/lib.linux-*/lxml/* ../../../src/lxml/tests .
cd ../..
ln -snf ../doc ../samples ../test.py .
%{__python3} test.py -v
cd ..
%endif

%if %{with apidocs_rebuild}
PYTHONPATH=$(echo $(pwd)/build-3/lib.linux-*) \
%{__python} doc/mkhtml.py doc/html $(pwd) %{version}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt CREDITS.txt LICENSE.txt LICENSES.txt README.rst TODO.txt doc/licenses/{BSD,elementtree}.txt
%dir %{py3_sitedir}/lxml
%attr(755,root,root) %{py3_sitedir}/lxml/_elementpath.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/lxml/builder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/lxml/etree.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/lxml/objectify.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/lxml/sax.cpython-*.so
%{py3_sitedir}/lxml/*.pxi
%{py3_sitedir}/lxml/*.py
%{py3_sitedir}/lxml/__pycache__
%{py3_sitedir}/lxml/etree.pyx
%{py3_sitedir}/lxml/objectify.pyx
%{py3_sitedir}/lxml/etree*.h
%{py3_sitedir}/lxml/lxml.etree*.h
%{py3_sitedir}/lxml/includes
%{py3_sitedir}/lxml/isoschematron
%dir %{py3_sitedir}/lxml/html
%{py3_sitedir}/lxml/html/*.py
%{py3_sitedir}/lxml/html/__pycache__
%attr(755,root,root) %{py3_sitedir}/lxml/html/diff.cpython-*.so
%{py3_sitedir}/lxml-%{version}-py*.egg-info

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
