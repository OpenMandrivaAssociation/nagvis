%define name	nagvis
%define version 1.5.7
%define release %mkrel 1

%define _requires_exceptions pear(\\(/var/www/.*\\|dwoo/dwooAutoload.php\\|Zend/.*\\))

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
Requires:   php-mbstring
Requires:   php-sockets
Requires:   php-gettext
Requires:   php-session
Requires:   php-pdo_sqlite
Requires:   php-ZendFramework
Requires:   graphviz
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
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
cp -r share %{buildroot}%{_datadir}/%{name}
cp -r docs %{buildroot}%{_datadir}/%{name}/share

cmp() {
    cat $1 | sed 's#\(var\)\s*\(\S*\)\s*=\s*#\1 \2=#;s#^\s*##;s#\s*$##;s#\t+# #g' | awk '
    BEGIN { OK=1; braces=0 }
    {
        # Remove /* */ one line comments
        sub(/\/\*[^@]*\*\//,"");
        # Remove // comments (line beginning)
        sub(/^\/\/.*/,"");
        
        # Count braces
        anz1 = gsub(/\{/,"{");
        anz2 = gsub(/}/,"}");
        
        if (OK == 1) {
            braces += anz1;
            braces -= anz2;
        }
    }
    /\/\*/ {
        c = gsub(/\/\*[^@]*$/,"");
        if(c > 0) {
            OK=0;
        }
    }
    /\*\/$/ {
        c = gsub(/^[^@]*\*\//,"");
        if(c > 0) {
            OK=1;
        }
    }
    {
        line = $0;
        #anz = gsub(/function/," function");
        #ch = substr(line,length(line));
        if (OK == 1) {
            if (length(line) > 0) {
                #if (ch == "}") {
                #   if (braces == 0) {
                #       if (length(line) > 0) {
                #           print line
                #       }
                #       line = ""
                #   }
                #}
                #line = line $0;
                
                print line;
            }
        }
    }
    ' >> $OUT
}




pushd %{buildroot}%{_datadir}/%{name}/share/frontend/nagvis-js/js/
OUT=NagVisCompressed.js
    >$OUT
    cmp nagvis.js
    cmp popupWindow.js
    cmp ExtBase.js
    cmp frontendMessage.js
    cmp frontendEventlog.js
    cmp hover.js
    cmp frontendContext.js
    cmp ajax.js
    cmp dynfavicon.js
    cmp frontend.js
    cmp lines.js
    cmp overlib.js
    cmp NagVisObject.js
    cmp NagVisStatefulObject.js
    cmp NagVisStatelessObject.js
    cmp NagVisHost.js
    cmp NagVisService.js
    cmp NagVisHostgroup.js
    cmp NagVisServicegroup.js
    cmp NagVisMap.js
    cmp NagVisShape.js
    cmp NagVisLine.js
    cmp NagVisTextbox.js
    cmp NagVisRotation.js
    cmp wz_jsgraphics.js
popd

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
cp -r etc/maps %{buildroot}%{_sysconfdir}/%{name}
cp -r etc/automaps %{buildroot}%{_sysconfdir}/%{name}
cp -r etc/geomap %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/nagvis.ini.php-sample \
    %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php
pushd %{buildroot}%{_datadir}/%{name}
ln -s ../../..%{_sysconfdir}/%{name} etc
popd

install -d -m 755 %{buildroot}%{_var}/lib/%{name}
install -d -m 755 %{buildroot}%{_var}/lib/%{name}/tmpl
install -d -m 755 %{buildroot}%{_var}/lib/%{name}/tmpl/cache
install -d -m 755 %{buildroot}%{_var}/lib/%{name}/tmpl/compile
pushd %{buildroot}%{_datadir}/%{name}
ln -s ../../..%{_var}/lib/%{name} var
popd

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
Alias /%{name} %{_datadir}/%{name}/share

<Directory %{_datadir}/%{name}/share>
    Order allow,deny
    Allow from all

    Options FollowSymLinks
</Directory>
EOF

# nagvis configuration
perl -pi \
    -e 's|;base=.*|base="%{_datadir}/nagvis/"|;' \
    -e 's|;htmlbase=.*|htmlbase="/nagvis"|;' \
    %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php 

# make configuration apache-writable
chmod -R g=u %{buildroot}%{_sysconfdir}/%{name}
chmod 660 %{buildroot}%{_sysconfdir}/%{name}/nagvis.ini.php

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc INSTALL LICENCE README
%config(noreplace) %{_webappconfdir}/%{name}.conf
%attr(-,root,apache) %dir %{_sysconfdir}/nagvis
%attr(-,root,apache) %dir %{_sysconfdir}/nagvis/maps
%attr(-,root,apache) %dir %{_sysconfdir}/nagvis/automaps
%attr(-,root,apache) %dir %{_sysconfdir}/nagvis/geomap
%attr(-,root,apache) %config(noreplace) %{_sysconfdir}/nagvis/nagvis.ini.php
%attr(-,root,apache) %config(noreplace) %{_sysconfdir}/nagvis/maps/*.cfg
%attr(-,root,apache) %config(noreplace) %{_sysconfdir}/nagvis/automaps/*.cfg
%attr(-,root,apache) %config(noreplace) %{_sysconfdir}/nagvis/geomap/*.xml
%attr(-,apache,apache) %{_var}/lib/%{name}
%{_datadir}/%{name}
