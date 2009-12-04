%define name	nagvis
%define version 1.4.5
%define release %mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Visualization addon for nagios
License:	GPL
Group:		Networking/WWW
URL:		http://nagvis.org
Source:     http://downloads.sourceforge.net/nagvis/%{name}-%{version}.tar.gz
Requires:   mod_php
Requires:   php-xml
Requires:   php-gd
Requires:   php-mysql
Requires:   php-mbstring
# webapp macros and scriptlets
Requires(post):		rpm-helper >= 0.16
Requires(postun):	rpm-helper >= 0.16
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	rpm-mandriva-setup >= 1.23
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
NagVis is a visualization addon for the well known network managment system
Nagios. NagVis can be used to visualize Nagios Data, e.g. to display IT
processes like a mail system or a network infrastructure.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 644 index.php %{buildroot}%{_datadir}/%{name}
cp -r nagvis %{buildroot}%{_datadir}/%{name}
cp -r wui %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
pushd %{buildroot}%{_datadir}/%{name}
ln -s ../../..%{_sysconfdir}/%{name} etc
popd
install -m 644 etc/nagvis.ini.php-sample %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php
cp -r etc/maps %{buildroot}%{_sysconfdir}/%{name}

install -d -m 755 %{buildroot}%{_var}/lib/%{name}
pushd %{buildroot}%{_datadir}/%{name}
ln -s ../../..%{_var}/lib/%{name} var
popd

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
Alias /%{name}/var %{_var}/lib/%{name}
Alias /%{name} %{_datadir}/%{name}

<Directory %{_datadir}/%{name}>
    Order allow,deny
    Allow from 127.0.0.1
    Deny from all
    ErrorDocument 403 "Access denied per %{_webappconfdir}/%{name}.conf"

    # nagvis complains if no user is defined
    SetEnv REMOTE_USER nagios
</Directory>

<Directory %{_var}/lib/%{name}>
    Order allow,deny
    Allow from 127.0.0.1
    Deny from all
    ErrorDocument 403 "Access denied per %{_webappconfdir}/%{name}.conf"
</Directory>
EOF

# nagvis configuration
perl -pi \
    -e 's|;base=.*|base="%{_datadir}/nagvis/"|;' \
    -e 's|;htmlbase=.*|htmlbase="/nagvis"|;' \
    %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php 

# make configuration apache-writable
chmod 664 %{buildroot}%{_sysconfdir}/%{name}/maps/*.cfg
chmod 660 %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php

cat > README.mdv <<EOF
Mandriva RPM specific notes

setup
-----
The setup used here differs from default one, to achieve better FHS compliance.
- the constant files are in %{_datadir}/%{name}
- the variable files are in %{_var}/lib/%{name}
- the configuration files are in %{_sysconfdir}/%{name}
EOF

%clean
rm -rf %{buildroot}

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc INSTALL LICENCE README README.mdv docs/*
%config(noreplace) %{_webappconfdir}/%{name}.conf
%dir %{_sysconfdir}/nagvis
%dir %{_sysconfdir}/nagvis/maps
%attr(-,root,apache) %config(noreplace) %{_sysconfdir}/nagvis/nagvis.ini.php
%attr(-,root,apache) %config(noreplace) %{_sysconfdir}/nagvis/maps/*.cfg
%attr(-,apache,apache) %{_var}/lib/%{name}
%{_datadir}/%{name}
