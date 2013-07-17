Name:		nagvis
Version:	1.5.9
Release:	4
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
BuildArch:	noarch

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
				#	if (braces == 0) {
				#		if (length(line) > 0) {
				#			print line
				#		}
				#		line = ""
				#	}
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
	cmp ExtStacktrace.js
	cmp nagvis.js
	cmp popupWindow.js
	cmp ExtBase.js
	cmp frontendMessage.js
	cmp frontendEventlog.js
	cmp frontendHover.js
	cmp hover.js
	cmp frontendContext.js
	cmp ajax.js
	cmp dynfavicon.js
	cmp frontend.js
	cmp lines.js
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

pushd %{buildroot}%{_datadir}/%{name}/share/frontend/wui/js/
	OUT=WuiCompressed.js
	>$OUT
	cmp wui.js
	cmp ajax.js
	cmp addmodify.js
	cmp EditMainCfg.js
	cmp ManageBackgrounds.js
	cmp ManageBackends.js
	cmp ManageMaps.js
	cmp ManageShapes.js
	cmp MapManageTmpl.js
	cmp wz_jsgraphics.js
	cmp ExtGenericResize.js
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
    Require all granted

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


%changelog
* Tue Jul 05 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.9-1mdv2011.0
+ Revision: 688912
- update to new version 1.5.9

* Thu Mar 10 2011 Funda Wang <fwang@mandriva.org> 1.5.8-2
+ Revision: 643231
- rebuild to obsolete old packages

* Thu Feb 03 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.8-1
+ Revision: 635667
- new version
- new version

* Sun Jan 23 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.7-1
+ Revision: 632444
- new version

* Sat Jan 01 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.6-1mdv2011.0
+ Revision: 627040
- update to new version 1.5.6

* Mon Dec 06 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.5-1mdv2011.0
+ Revision: 612527
- new version

* Fri Aug 13 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.1-1mdv2011.0
+ Revision: 569472
- new version
- drop README.mdv, the setup is self-explaining

* Mon Apr 26 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.7-1mdv2010.1
+ Revision: 538956
- new version

* Sun Mar 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.6-1mdv2010.1
+ Revision: 518978
- update to new version 1.4.6

* Wed Feb 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.5-2mdv2010.1
+ Revision: 507266
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- switch to "open to all" default access policy

* Fri Dec 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.5-1mdv2010.1
+ Revision: 473620
- ensure followsymlink is always disabled
- new version
- don't attempt to isolate files from web root, to match upstream setup better
- enforce new default access policy

* Sat Nov 07 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.4-1mdv2010.1
+ Revision: 462214
- update to new version 1.4.4

* Sun Aug 23 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.2-1mdv2010.0
+ Revision: 419925
- new version

* Wed Jun 10 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.1-1mdv2010.0
+ Revision: 384878
- new version
- mv all files under %%_datadir/%%name, %%_var/www is not FHS compliant
- better default configuration file

* Wed Feb 18 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.2-1mdv2009.1
+ Revision: 342730
- new version
- drop additional noprefix patch, fixed upstream

* Sat Sep 20 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.1-3mdv2009.0
+ Revision: 286172
- new version
- use symlinks rather than code patch to achieve FHS compliance
- make maps and configuration apache writable

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.2.2-3mdv2009.0
+ Revision: 253560
- rebuild

* Mon Feb 25 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.2-1mdv2008.1
+ Revision: 175068
- new version

* Mon Feb 11 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.1-1mdv2008.1
+ Revision: 165532
- new version
  rediff FHS patch

* Tue Dec 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.2-1mdv2008.1
+ Revision: 132113
- final version
  include wui
- patch1: allow dbprefix to be mepty
- import nagvis


* Fri Dec 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.2-0.%%{rc}.1mdv2008.1
- first mdv release
