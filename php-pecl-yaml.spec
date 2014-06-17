#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname	yaml
Summary:	YAML-1.1 parser and emitter
Name:		%{php_name}-pecl-%{modname}
Version:	1.1.1
Release:	1
License:	MIT
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	5ea624ec23fe9ad20e4f24ee43da72b1
URL:		http://pecl.php.net/package/yaml/
%{?with_tests:BuildRequires:    %{php_name}-cli}
BuildRequires:	%{php_name}-devel >= 4:5.2.0
BuildRequires:	rpmbuild(macros) >= 1.666
%{?requires_php_extension}
Provides:	php(yaml) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Support for YAML 1.1 (YAML Ain't Markup Language) serialization using
the LibYAML library.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%if %{with tests}
# simple module load test
%{__php} -n -q \
	-d extension_dir=modules \
	-d extension=%{modname}.so \
	-m > modules.log
grep %{modname} modules.log

export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
%{__make} test \
	PHP_EXECUTABLE=%{__php}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
