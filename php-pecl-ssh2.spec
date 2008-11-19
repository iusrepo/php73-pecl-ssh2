%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%define pecl_name ssh2

Name:           php-pecl-ssh2
Version:        0.10
Release:        2%{?dist}
Summary:        Bindings for the libssh2 library

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/ssh2
Source0:        http://pecl.php.net/get/ssh2-%{version}.tgz
Source1:        PHP-LICENSE-3.01
Source2:        php-pecl-ssh2-0.10-README

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         libssh2.diff

BuildRequires:  libssh2-devel php-devel php-pear >= 1:1.4.9-1.2
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(ssh2) = %{version}

%if %{?php_zend_api}0
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
# for EL-5
Requires:       php-api = %{php_apiver}
%endif


%description
Bindings to the functions of libssh2 which implements the SSH2 protocol.
libssh2 is available from http://www.sourceforge.net/projects/libssh2

%prep
%setup -c -q 
%{__mv} package.xml %{pecl_name}-%{version}/%{pecl_name}.xml

%{__install} -m 644 -c %{SOURCE1} LICENSE
%{__install} -m 644 -c %{SOURCE2} README


cd %{pecl_name}-%{version}
%patch0 -p0


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 %{pecl_name}.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
%{__install} -d %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/ssh2.ini << 'EOF'
; Enable ssh2 extension module
extension=ssh2.so
EOF


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README
%config(noreplace) %{_sysconfdir}/php.d/ssh2.ini
%{php_extdir}/ssh2.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sat Nov 15 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.10-2
- Install pecl xml, license and readme files

* Wed Jul 16 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.10-1
- Initial release
