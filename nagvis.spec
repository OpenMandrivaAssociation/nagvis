%define name	nagvis
%define version 1.2
%define beta    rc1
%define release %mkrel 0.%{beta}.1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Visualization addon for nagios
License:	GPL
Group:		Networking/WWW
URL:		http://nagvis.org
Source:     http://garr.dl.sourceforge.net/sourceforge/nagvis/%{name}-%{version}%{beta}.tar.gz
Patch0:      %{name}-1.2rc1-fhs.patch
Patch1:      %{name}-1.2rc1-allow-empty-prefix.patch
Requires:   mod_php
Requires:   php-xml
Requires:   php-gd
Requires:   php-mysql
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
%setup -q -n %{name}-%{version}%{beta}
%patch0 -p 1
%patch1 -p 1

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -d -m 755 %{buildroot}%{_var}/www/%{name}/includes
cp -r nagvis/includes/js %{buildroot}%{_var}/www/%{name}/includes
cp -r nagvis/includes/css %{buildroot}%{_var}/www/%{name}/includes
cp -r nagvis/images %{buildroot}%{_var}/www/%{name}
install -m 644 nagvis/index.php %{buildroot}%{_var}/www/%{name}
install -m 644 nagvis/draw.php %{buildroot}%{_var}/www/%{name}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}/includes
cp -r nagvis/includes/defines %{buildroot}%{_datadir}/%{name}/includes
cp -r nagvis/includes/functions %{buildroot}%{_datadir}/%{name}/includes
cp -r nagvis/includes/languages %{buildroot}%{_datadir}/%{name}/includes
cp -r nagvis/includes/classes %{buildroot}%{_datadir}/%{name}/includes
cp -r nagvis/templates %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/nagvis.ini.php-sample %{buildroot}%{_sysconfdir}/%{name}/nagvis.conf
cp -r etc/maps %{buildroot}%{_sysconfdir}/%{name}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
Alias /%{name} %{_var}/www/%{name}

<Directory %{_var}/www/%{name}>
    Allow from all
</Directory>
EOF

%clean
rm -rf %{buildroot}

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc INSTALL LICENCE README
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/nagvis
%{_var}/www/%{name}
%{_datadir}/%{name}

