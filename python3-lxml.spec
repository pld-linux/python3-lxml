#
%define		module	lxml
#
Summary:	A Pythonic binding for the libxml2 and libxslt libraries
Summary(pl.UTF-8):	Pythonowe wiązanie do bibliotek libxml2 i libxslt
Name:		python3-%{module}
Version:	2.2.6
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	http://codespeak.net/lxml/%{module}-%{version}.tgz
# Source0-md5:	b1f700fb22d7ee9b977ee3eceb65b20c
Patch0:		2to3.patch
URL:		http://codespeak.net/lxml/
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	python3-Cython
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lxml is a Pythonic binding for the libxml2 and libxslt libraries.

%description -l pl.UTF-8
lxml to pythonowe wiązanie do bibliotek libxml2 i libxslt.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p0

%build
%{__python3} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python3} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py3_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* CHANGES.txt CREDITS.txt TODO.txt
%dir %{py3_sitedir}/lxml
%{py3_sitedir}/lxml/*.py[co]
%dir %{py3_sitedir}/lxml/html
%{py3_sitedir}/lxml/html/*.py[co]
%attr(755,root,root) %{py3_sitedir}/lxml/etree.so
%attr(755,root,root) %{py3_sitedir}/lxml/objectify.so
%{py3_sitedir}/lxml-*.egg-info
