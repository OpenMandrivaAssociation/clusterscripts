%define name clusterscripts
%define version 3.5
%define release %mkrel 4
#define	perl_vendorlib /usr/lib/perl5/vendor_perl/5.8.7

Summary: Tools to setup a cluster server and client
Name: %{name}
Version: %{version}
Release: %{release}
#Source0: %{name}-%{version}.tar.bz2
Source0: %{name}-devel.tar.bz2
License: 	GPL
Group: 		System/Cluster
BuildRoot: 	%{_tmppath}/%{name}-buildroot
Prefix: 	%{_prefix}
URL:		http://www.mandriva.com
buildarch:	noarch
#obsolotes:	clusterautosetup-server

%description
Multiple scripts to setup cluster server or client nodes.


%package        client
Summary:	Script to setup and retrieve information for client node
Group:		System/Cluster
Conflicts:	clusterautosetup-server
Requires:	bind-utils, ypbind, autofs, wget,openssh-clients, openssh-server, tftp, nfs-utils, netkit-rsh-server, ntp, ka-deploy-source-node, oar-user, oar-node, usbutils, urpmi-parallel-ka-run, bc, dhcpcd, smartmontools, ganglia-core, taktuk, clusterscripts-common

%description client
Scripts to retrieve information and setup cluster client node from 
a cluster server.

%package common
Summary:        Common clusterscripts
Group:		System/Cluster

%description common
common libs

%package server-conf
Summary:        clusterscript configuration file
Group:          System/Cluster
Conflicts:      clusterautosetup-client
Requires:       clusterscripts-common

%description server-conf
The configuration file of clusterscripts

%package server 
Summary:        Script to setup a server node
Group:		System/Cluster
Conflicts:	clusterautosetup-client
Requires:	bind, bind-utils, nfs-utils, ypserv, yp-tools, ypbind, make, oar-user, oar-node, oar-server, openssh-server, openssh-clients, ntp, ganglia-gmetad, urpmi-parallel-ka-run, apache, postfix, iptables, ganglia-core, rpm-helper, syslinux, usbutils, bc, php-cli, apache-mod_php, smartmontools, tentakel, ganglia-webfrontend, taktuk, fping, openldap-servers, openldap-clients
Requires:	clusterscripts-common, clusterscripts-server-pxe, clusterscripts-server-conf
Suggests:	phpldapadmin
#gnbd, gnbd-kernel-BOOT, 
#maui

%description server
Scripts to automatically setup some services
NIS, DNS, NFS, PXE, DHCP, NAMED, LDAP, authd and ssh Keys,
tftp server, ganglia server, OAR, SSH.

%package server-pxe
Summary:        Script to setup a PXE server, dhcpd tftp and optiannly a DNS server
Group:          System/Cluster
Conflicts:      clusterautosetup-client
Requires:       pxe, tftp-server, xinetd, dhcp-server, syslinux, clusterscripts-server-conf
Suggests:	ka-deploy-source-node bind bind-utils

%description server-pxe
Scripts to automatically setup a PXE server with DHCP server.
A DNS server is also optionnal

%prep
rm -rf ${buildroot}
%setup -q -n %{name}-devel


%build
#make build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_docdir/%name-%version
make install DESTDIR=$RPM_BUILD_ROOT SHAREDOC=%_docdir/%name-%version


%post server-conf
TESTDHETH=`grep ETHDHCP_CLIENT /etc/clusterserver.conf`
if [ -z "$TESTDHETH" ];	then
	echo " old version of clusterscript, updating"
	echo "ETHDHCP_CLIENT=eth0" >> /etc/clusterserver.conf
fi	
# create a file, to check if it is the first time i launch setup_auto_cluster
touch /tmp/first_setup
	
#perl -Mcluster_xconfig -e 'set_xconfig()'

%post client
%_post_service clusterautosetup-client
# horrible hack to avoid dhclient.....
#perl -pi -e "s/\-x\s\/sbin\/dhclient/-x \/sbin\/dhclientsux/" /sbin/ifup

%preun client
%_preun_service clusterautosetup-client

%preun server
#%_preun_service rapidnat

%clean
rm -fr %{buildroot}

%files client
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/setup_client_cluster.pl
%attr(755,root,root) %{_bindir}/setup_ka_deploy.pl
%attr(755,root,root) %{_initrddir}/clusterautosetup-client
%{perl_vendorlib}/ka_deploy_cluster.pm
%{perl_vendorlib}/client_cluster.pm
%{perl_vendorlib}/fs_client.pm
%{perl_vendorlib}/cluster_clientconf.pm

%files common
#%attr(755,root,root) %{_bindir}/fdisk_to_desc
%{_bindir}/ib-burn-firmware.pl
%{perl_vendorlib}/cluster_commonconf.pm
%{perl_vendorlib}/cluster_fonction_common.pm

%files server-conf
%attr(755,root,root) %{_sysconfdir}/muttrc
%attr(755,root,root) %{_sysconfdir}/rc.sysinit_diskless
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/clusterserver.conf
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/clusternode.conf
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/dhcpd.conf.pxe.single
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/dhcpd.conf.cluster
%{perl_vendorlib}/cluster_serverconf.pm

%files server-pxe
%attr(755,root,root) %{_bindir}/dhcpnode
%{perl_vendorlib}/add_nodes_to_dhcp_cluster.pm
%{perl_vendorlib}/pxe_server_cluster.pm
%{perl_vendorlib}/dhcpnode_cluster.pm
%{perl_vendorlib}/dhcpdconf_server_cluster.pm
%{perl_vendorlib}/wakeup_node_cluster.pm
%{perl_vendorlib}/dns_cluster.pm
%attr(755,root,root) %{_bindir}/setup_add_nodes_to_dhcp.pl
%attr(755,root,root) %{_bindir}/setup_pxe_server.pl
%attr(755,root,root) %{_bindir}/setup_dhcpdconf_server.pl
%attr(755,root,root) %{_bindir}/setup_dns.pl
%attr(755,root,root) %{_bindir}/prepare_diskless_image


%files server
%doc ldap_base.ldif sldap_cluster.conf
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/ib-cluster-configurator.pl
%attr(755,root,root) %{_bindir}/rapidnat
%attr(755,root,root) %{_bindir}/sauvegarde
%attr(755,root,root) %{_bindir}/setup_xconfig.pl
#%{_initrddir}/rapidnat
%attr(755,root,root) %{_bindir}/setup_test_user
%attr(644,root,root) /var/spool/pbs/pbs_config.sample
%{perl_vendorlib}/cluster_xconfig.pm
%{perl_vendorlib}/fs_server.pm
%{perl_vendorlib}/nis_cluster.pm
%{perl_vendorlib}/ldap_cluster.pm
%{perl_vendorlib}/install_cluster.pm
%{perl_vendorlib}/auto_add_nodes_cluster.pm
%{perl_vendorlib}/maui_cluster.pm
%{perl_vendorlib}/auto_remove_nodes_cluster.pm
%{perl_vendorlib}/cluster_set_admin.pm
%{perl_vendorlib}/cluster_set_compute.pm
%{perl_vendorlib}/user_common_cluster.pm
%{perl_vendorlib}/postfix_cluster.pm
%{perl_vendorlib}/pbs_cluster.pm
%{perl_vendorlib}/server_cluster.pm
%attr(755,root,root) %{_bindir}/setup_pbs.pl
%attr(755,root,root) %{_sbindir}/setup_auto_cluster
%attr(755,root,root) %{_bindir}/setup_add_node.pl
%attr(755,root,root) %{_bindir}/setup_install_cluster.pl
%attr(755,root,root) %{_bindir}/setup_server_cluster.pl
%attr(755,root,root) %{_bindir}/setup_recup_cpus.pl
%attr(755,root,root) %{_bindir}/setup_nis.pl
%attr(755,root,root) %{_bindir}/setup_ldap.pl
%attr(755,root,root) %{_bindir}/setup_auto_remove_nodes.pl
%attr(755,root,root) %{_sbindir}/deluserNis.pl
%attr(755,root,root) %{_bindir}/wakeup_node.pl
%attr(755,root,root) %{_bindir}/setup_maui.pl
%attr(755,root,root) %{_bindir}/setup_auto_add_nodes.pl
%attr(755,root,root) %{_sbindir}/adduserNis.pl
%attr(755,root,root) %{_bindir}/setup_postfix.pl
%attr(755,root,root) %{_bindir}/setup_admin.pl
%attr(755,root,root) %{_bindir}/setup_compute.pl
%attr(755,root,root) %{_bindir}/update_cfg_after_ar_node.pl



%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 3.5-4mdv2011.0
+ Revision: 663385
- mass rebuild

* Thu Jul 22 2010 Funda Wang <fwang@mandriva.org> 3.5-3mdv2011.0
+ Revision: 556989
- rebuild

* Mon Jun 28 2010 Antoine Ginies <aginies@mandriva.com> 3.5-2mdv2010.1
+ Revision: 549278
- re-organise pakackaging
- new release (fix some nis and pxe bugs)

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix upgrade 2010.0 > 2010.1

* Thu May 06 2010 Antoine Ginies <aginies@mandriva.com> 3.5-1mdv2010.1
+ Revision: 542810
- move wakup perl module to server-pxe package

* Wed May 05 2010 Antoine Ginies <aginies@mandriva.com> 3.4-1mdv2010.1
+ Revision: 542324
- release 3.4

* Tue May 04 2010 Antoine Ginies <aginies@mandriva.com> 3.3-1mdv2010.1
+ Revision: 542091
- remove a cp in the Makefile
- update the source (remove fdisk_to_desc)
- two more packages: server-pxe and server-conf

* Fri Feb 12 2010 Antoine Ginies <aginies@mandriva.com> 3.2-4mdv2010.1
+ Revision: 504650
- add suggests, fix ldap  module

* Fri Feb 12 2010 Antoine Ginies <aginies@mandriva.com> 3.2-3mdv2010.1
+ Revision: 504509
- new source
- fix setup_server_cluster.pl error

* Thu Feb 11 2010 Antoine Ginies <aginies@mandriva.com> 3.2-2mdv2010.1
+ Revision: 504252
- fix name of conf files

* Thu Feb 11 2010 Antoine Ginies <aginies@mandriva.com> 3.2-1mdv2010.1
+ Revision: 504163
- add a basic description for common package
- create a common package, remove conflict between client and server

* Tue Feb 09 2010 Antoine Ginies <aginies@mandriva.com> 3.0-4mdv2010.1
+ Revision: 502814
- fix spec file to avoid rejection
- fix group
- release 3.0

* Sun Jul 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.0-21mdv2010.0
+ Revision: 400287
- fix dependencies

* Tue Jul 22 2008 Thierry Vignaud <tv@mandriva.org> 2.0-20mdv2009.0
+ Revision: 240507
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 22 2007 Nicolas Vigier <nvigier@mandriva.com> 2.0-18mdv2008.0
+ Revision: 92234
- add pure-ftpd-anon-upload buildrequire
- fix apache2-mod_php dependency (now apache-mod_php)
- remove broken dependency on proftpd-anonymous
 - add dependency on pure-ftpd-anonymous
 - clean up

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 2.0-17mdv2008.0
+ Revision: 70158
- convert prereq

* Fri Jun 22 2007 Thierry Vignaud <tv@mandriva.org> 2.0-16mdv2008.0
+ Revision: 42999
- partial cleaning
- fix group

* Thu May 31 2007 Adam Williamson <awilliamson@mandriva.org> 2.0-15mdv2008.0
+ Revision: 32984
- fix groups (fixes #27319 and #27320)


* Fri Mar 02 2007 Antoine Ginies <aginies@mandriva.com> 2.0-14mdv2007.0
+ Revision: 131006
- define a perlvendorlib directory
- Import clusterscripts

* Tue Feb 06 2007 Antoine Ginies <aginies@mandriva.com> 2.0-14mdviggi
- remove dssh require

* Thu Jan 18 2007 Antoine Ginies <aginies@mandriva.com> iggi 2.0-13mdv
- improve MySQL configuration

* Thu Nov 30 2006 Antoine Ginies <aginies@mandriva.com> 2.0-12mdviggi
- various fix to be able to use clusterscripts on a CS4
- add rpmsrate and compssUsers.pl
- add boot flag on first partition (ka deploy)
- add log suuport with kamethod

* Wed Nov 29 2006 Antoine Ginies <aginies@mandriva.com> 2.0-11mdviggi
- add CSH support (/etc/profile.d/cluster.csh)
- remove CLUSTER image

* Wed Nov 15 2006 Antoine Ginies <aginies@mandriva.com> 2.0-10mdviggi
- fix OAR problem in diskless mode

* Fri Nov 10 2006 Antoine Ginies <aginies@mandriva.com> 2.0-9mdviggi
- Add a script to prepare diskless image
- add cloop-utils require
- remove pcp require

* Thu Nov 09 2006 Antoine Ginies <aginies@mandriva.com> 2.0-8mdviggi
- fix regenerate_rhosts file

* Wed Nov 08 2006 Antoine Ginies <aginies@mandriva.com> 2.0-7mdviggi
- add symlink for nfs installation
- fix fs_server and fs_client gfs part

* Tue Nov 07 2006 Antoine Ginies <aginies@mandriva.com> 2.0-6mdviggi
- fix path to draktab_config
- remove maui in add_user_nis
- remove unwanted message

* Mon Nov 06 2006 Antoine Ginies <aginies@mandriva.com> 2.0-5mdviggi
- remove AmIroot
- try to fix hdlist script (mkcd create a bad media.cfg file....)
- fix tentakel configuration
- fix hostname bug if interface != to eth0

* Fri Nov 03 2006 iggi Antoine Ginies <aginies@mandriva.com> 2.0-4mdviggi
- fix shorewall zone
- launch draktab_config at first launch (if drakcluster installed)
- fix pssh configuration
- add prologue/epilogue timeout in oar configuration
- fix tentakel configuration

* Thu Nov 02 2006 Antoine Ginies <aginies@mandriva.com> 2.0-3mdviggi
- add pssh and tentakel support

* Thu Nov 02 2006 Antoine Ginies <aginies@mandriva.com> 2.0-2mdviggi
- fix linux.0 problem in default dhcpd.conf configuration file (thx T.I. Toth report)
- fix ssh-keygen problem (server side)
- create oar user .ssh directory
- fix the use of CS4 rescue in ka method

* Tue Oct 31 2006 Antoine Ginies <aginies@mandriva.com> 2.0-1mdviggi
- fix oar state

* Mon Oct 30 2006 Antoine Ginies <aginies@mandriva.com> 1.9-3mdviggi
- fix mysql skip-network option
- auto declare node Alive
- fix set_oar_servername (client side)
- add taktuk2 and fping requires
- add fping in oar configuration

* Fri Oct 27 2006 Antoine Ginies <aginies@mandriva.com> 1.9-2mdv2007.0
- remove compute DOMAIN and compute node name
- switch pbs to oar group
- remove /etc/node_list.admin file
- only exec command on Alive node (using OAR status)

* Wed Oct 25 2006 Antoine Ginies <aginies@mandriva.com> 1.9-1mdviggi
- first IGGI devel release
- remove torque require
- add oar require
- add OAR support (ssh public key, tftpdir, oar.conf)
- remove call to PBS script
- Now use Bind 9.2, so adjust all DNS configuration
- add support of menu311.c32 in PXE configuration file
- add alt1 vmlinuz and all.rdz in PXE menu entry
- update information in PXE help.txt file
- update auto_inst.cfg.pl RPM list

* Wed Nov 30 2005 Antoine Ginies <aginies@n3.mandriva.com> 1.3-1mdk
- copy freedos.img only if exist
- nodename now support '-'
- add generate_ex_dolly_conf
- disable gam server only if exist
- disable auto_cluster icon in icewm toolbar
- remove require on ganglia-script
- clean %%post
- remove unwanted services
- add drakpxelinux require
- add gnbd and rescue in PXE menu 
- fix generation of cluster.conf file
- fix pb of missgin lam directory on nodes
- use vga=text in ka mode
- fix fs_server.pm ccsd configuration
- now use fs.pm
- add coda support (client and server)
- fix missing files move into cluster_fonction_common
- fix creation of lam file
- fix missing file for reading (mpi and lam)
- fix pxe (remove ka.img patch) 
- fix missing dir (mpi and lam)
- remove some requires on client node (distcc icecream)
- remove mandrake_theme require
- add mpich2 support
- fix nsswitch.conf
- add requires (ganglia-webfrontend)
- fix lam missing directory
- fix mountcdrom in setup_auto_cluster
- copy RPM data from nfs or cdrom
- dont generate gmond.conf
- adjust RESCUE name

* Tue Mar 22 2005 Antoine Ginies <aginies@n1.mandrakesoft.com> 1.1-38mdk
- add requires

* Tue Mar 22 2005 <guibo@guiboserv.guibland.com> 1.1-37mdk
- adjust requires

* Mon Mar 07 2005 <aginies@guibo.mdkc.com> 1.1-36mdk
- add ib-burn-firmware.pl
- add ib-cluster-configurator.pl

* Fri Mar 04 2005 <aginies@guibo.mdkc.com> 1.1-35mdk
- re-require idesk
- re-add require on mpich

* Fri Mar 04 2005 <aginies@guibo.mdkc.com> 1.1-34mdk
- remove display in PXE conf
- create mpi wanted dir

* Thu Mar 03 2005 <aginies@guibo.mdkc.com> 1.1-33mdk
- remove requires on mpich
- add create_hostib.pl

* Thu Mar 03 2005 <aginies@guibo.mdkc.com> 1.1-32mdk
- Mercury Release
- fix ib over ip in shorewall config
- set pxe to auto mode
- use fdisk_to_desc to create descfile on node

* Thu Feb 10 2005 <aginies@guibo.mdkc.com> 1.1-31mdk
- fix some other X configuration

* Wed Feb 09 2005 <aginies@guibo.mdkc.com> 1.1-30mdk
- fix background pb (server/client)

* Wed Feb 09 2005 <aginies@guibo.mdkc.com> 1.1-29mdk
- add fdisk_to_desc
- copy only one CD

* Thu Nov 25 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-28mdk
- copy the 4 cds

* Wed Nov 10 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-27mdk
- add requires on mclx doc (client and server)

* Thu Nov 04 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-26mdk
- adjust for Clustering2 (to fit on 1CD)

* Wed Nov 03 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-25mdk
- add require on doc

* Wed Nov 03 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-24mdk
- fix path to doc
- update index.html

* Tue Nov 02 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-23mdk
- fix xdm background

* Fri Oct 29 2004 aginies <aginies@dhcp125.mandrakesoft.com> 1.1-22mdk
- fix acpi=ht on x86_64

* Fri Oct 29 2004 aginies <aginies@dhcp125.mandrakesoft.com> 1.1-21mdk
- fix pxe x86_64 pb (freedos)

* Fri Oct 22 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-20mdk
- add post install in auto_inst.cfg.pl

* Fri Oct 22 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-19mdk
- force install of theme-mercury
- fix requires on mandrake-theme-mercury

* Thu Oct 21 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-18mdk
- fix, typo (thx pixel)

* Thu Oct 21 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-17mdk
- fix underscore :/

* Sat Oct 16 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-16mdk
- fix resetknowhosts
- fix add node without ka

* Sat Oct 16 2004 mdkc <mdkc@guiboserv.guibland.com> 1.1-15mdk
- add new file to add node without ka method (thx camille bug report).

* Fri Oct 15 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-14mdk
- fix pxe ka24.img on X86_64

* Thu Oct 14 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-13mdk
- fix auto_inst.cfg.pl (had SMP support)

* Fri Oct 08 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-12mdk
- fix a pb of copy4CD

* Tue Oct 05 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-11mdk
- copy 4cd

* Thu Sep 30 2004 aginies <mdkc@mdkc2devel.mandrakesoft.com> 1.1-10mdk
- mercury release

* Fri Sep 17 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-9mdk
- fix rc.sysinit Branding

* Wed Sep 15 2004 mdkc <mdkc@guiboserv.guibland.com> 1.1-8mdk
- fix some branding

* Thu Aug 26 2004 Erwan Velu <erwan@mandrakesoft.com> 1.1-7mdk
- MII_NOT_SUPPORTED by default in auto mode
- auto_mode also install mandrake_theme
- Removing uncessary requires

* Thu Aug 26 2004 Erwan Velu <erwan@mandrakesoft.com> 1.1-6mdk
- Adding requires

* Fri Aug 06 2004 Erwan Velu <erwan@mandrakesoft.com> 1.1-5mdk
- New release
- Fixing default background system (now using theme)
- Requires mandrake_theme

* Tue Jul 13 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-4mdk
- add user admin

* Fri Jul 09 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-3mdk
- add requires (mozilla, dssh, idesk)
- fix localtime pb (missing cp_in_workdir)

* Thu Jul 01 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-2mdk
- fix xdm dialog box
- launch draktab_configat beginning of setup_autokc@mdkc2devel.mandrakesoft.com> 1.1-3mdk
- add requires (mozilla, dssh, idesk)
- fix localtime pb (missing cp_in_workdir)

* Thu Jul 01 2004 mdkc <mdkc@mdkc2devel.mandrakesoft.com> 1.1-2mdk
- fix xdm dialog box
- launch draktab_configat beginning of setup_auto_cluster
- adjust icewm toolbar
- patching pxe for generating auto entry
- fix default nisdomain (gi+drakcluster)
- add xhost +
- add test on user's home to avoid pb of drakcluster (quit when !-d home's user )
- cleaning ntp configuration

* Sat Jun 26 2004 aginies <mdkc@mdkc2devel.mandrakesoft.com> 1.1-1mdk
- more perl_checker fix
- add comment in clusterscripts
- correct dhcpd.conf leases time
- various fix to accelerate remove node procedure
- fix dssh et wulfstat reload in a/d in admin mode
- add require on xmlsysd

* Fri Jun 25 2004 aginies <mdkc@mdkc2devel.mandrakesoft.com> 1.0-8mdk
- now when adding serveur in compute, server is disable in admin
- fix wulfstat pb
- add requires smartmontools, fix missing require gangali on client
- add smartmon tools config

* Wed Jun 23 2004 mdkc <mdkc@devel.mdkc.com> 1.0-7mdk
- fix add_srv (dns problem)
- fix ssh root on server (authorized_keys)
- fix generation of nisdomain pb
- remove sleep in dns configuration
- add comment
- fix icewm icon pb

* Tue Jun 22 2004 <mdkc@n2.mandrakesoft.com> 1.0-6mdk
- add wulfstat config
- now can add srv in cluster

* Sat Jun 12 2004 <mdkc@n2.mandrakesoft.com> 1.0-5mdk
- perl_checker recommendation

* Fri Jun 11 2004 <mdkc@n2.mandrakesoft.com> 1.0-4mdk
- add more quick launch on icewm's toolbar

* Fri Jun 11 2004 mdkc <mdkc@n2.mandrakesoft.com> 1.0-3mdk
- add dssh support (remote admin) 
- patch userdrake to support cluster user using adduserNis/deluserNis

* Tue May 25 2004 mdkc <mdkc@localhost> 1.0-2mdk
- add gsh support (remote admin)

* Tue May 18 2004 <mdkc@n2.mandrakesoft.com> 1.0-1mdk
- release 1.0

* Tue Apr 13 2004 antoine Ginies <aginies@mandrakesoft.com> 0.9-11mdk
- use alternatives ka.img (kernel 2.4.25)
- pxe_cluster: compatible drakwizard pxe, more debug 
- perl_checker recommendation
- fix PBS pb on client node
- fix ntp pb on client
- add missing requires
- fix dhcpd.conf tftpdir var
- add needed_after add/remove in cmd line
- permit ssh root login on node
- add unwanted services

* Fri Apr 09 2004 antoine Ginies <aginies@mandrakesoft.com> 0.9-10mdk
- fix some pxe pb

* Thu Apr 08 2004 antoine Ginies <aginies@mandrakesoft.com> 0.9-9mdk
- fix client scripts
- fix PXE pb server side (need more fix....)

* Tue Apr 06 2004 antoine Ginies <aginies@mandrakesoft.com> 0.9-8mdk
- fix pb on client (dhclient)
- fix PXE pb (var/lib/tftp/X86PC)
- PXE now compatible with drakwizard pxe
- fix PBS pb
- some perl_checker fix (too much to fix all this time)

* Tue Apr 06 2004 antoine Ginies <aginies@mandrakesoft.com> 0.9-7mdk
- fix require

* Tue Apr 06 2004 guibo <guibo@xp2400.guibland.com> 0.9-6mdk
- rebuild 10.0

