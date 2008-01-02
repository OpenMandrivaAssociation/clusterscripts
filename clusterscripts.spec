%define name clusterscripts
%define version 2.0
%define release %mkrel 18

Summary: Tools to setup a cluster server and client
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-devel.tar.bz2
License: 	GPL
Group: 		System/Cluster
BuildRoot: 	%{_tmppath}/%{name}-buildroot
Prefix: 	%{_prefix}
URL:		http://www.mandriva.com
buildarch:	noarch

%description
Multiple scripts to setup cluster server or client nodes.


%package        client
Summary:	Script to setup and retrieve information for client node
Group:		System/Cluster
Conflicts:	%{name}-server, clusterautosetup-server
Requires(post):		rpm-helper
Requires(postun):		rpm-helper
Requires:	bind-utils xli ypbind autofs wget openssh-clients openssh-server
Requires:	tftp nfs-utils gexec xinitrc rsh-server ntp ka-deploy-source-node
Requires:	oar-user oar-node clone usbutils urpmi-parallel-ka-run bc dhcpcd
Requires:	smartmontools ganglia-core qiv cloop-utils taktuk2

%description client
script to retrieve information and setup cluster client node from 
a server.

%package server 
Summary:        Script to setup a server node
Group:		System/Cluster
Conflicts:	%{name}-client, clusterautosetup-client
Requires:	bind bind-utils nfs-utils ypserv yp-tools ypbind pxe tftp-server
Requires:	xinetd make dhcp-server oar-user oar-node oar-server
Requires:	oar-draw-gantt openssh-server openssh-clients pxe xli ntp
Requires:	ganglia-gmetad urpmi-parallel-ka-run apache postfix iptables
Requires:	xpdf xterm ganglia-core icewm mutt pvm rpm-helper syslinux
Requires:	usbutils shorewall bc php-cli apache-mod_php gexec smartmontools
Requires:	monika qiv tentakel ganglia-webfrontend taktuk2 fping cloop-utils
Requires:	pure-ftpd-anonymous pure-ftpd-anon-upload
#gnbd, gnbd-kernel-BOOT, 
#maui

%description server
Script to auto setup a NIS, DNS, NFS, PXE, DHCPD, HDLIST, authd and ssh Keys.

%prep
rm -rf ${buildroot}
%setup -q -n %{name}-devel

%build
#make build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_docdir/%name-%version
make install DESTDIR=$RPM_BUILD_ROOT SHAREDOC=%_docdir/%name-%version


%post server
#%_post_service rapidnat
#if [ "`grep lsusb /etc/init.d/mandrake_everytime`" = "" ]; then
#echo "#Prevent no keyboard on ia64 systems" >>/etc/init.d/mandrake_everytime
#echo "lsusb -v >/dev/null" >>/etc/init.d/mandrake_everytime
#fi
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
if [ "`grep lsusb /etc/init.d/mandrake_everytime`" = "" ]; then
echo "#Prevent no keyboard on ia64 systems" >>/etc/init.d/mandrake_everytime
echo "lsusb -v >/dev/null" >>/etc/init.d/mandrake_everytime
fi

%preun client
%_preun_service clusterautosetup-client

%preun server
#%_preun_service rapidnat

%clean
rm -fr %{buildroot}

%files client
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/setup_client_cluster.pl
%attr(755,root,root) %{_bindir}/setup_add_media.pl
%attr(755,root,root) %{_bindir}/setup_ka_deploy.pl
%attr(755,root,root) %{_initrddir}/clusterautosetup-client
%{_bindir}/fdisk_to_desc
#%attr(755,root,root) %{_initrddir}/pbs_mom
%{perl_vendorlib}/ka_deploy_cluster.pm
%{perl_vendorlib}/client_cluster.pm
%{perl_vendorlib}/fs_client.pm
%{perl_vendorlib}/cluster_commonconf.pm
%{perl_vendorlib}/cluster_clientconf.pm
%{perl_vendorlib}/cluster_fonction_common.pm
%{perl_vendorlib}/add_media_cluster.pm
#%attr(644,root,root) /etc/X11/CLUSTER-1024.jpg
%{_bindir}/ib-burn-firmware.pl

%files server
%defattr(-,root,root)
%{_docdir}/%name-%version/rpmsrate
%{_docdir}/%name-%version/compssUsers.pl
#%attr(644,root,root) /etc/X11/CLUSTER-1024.jpg
%config(noreplace) /var/www/html/iggi.html
#/var/www/html/Cluster-logo.png
%{_bindir}/ib-burn-firmware.pl
%{_bindir}/ib-cluster-configurator.pl
%{_bindir}/rapidnat
%{_bindir}/sauvegarde
%{_bindir}/fdisk_to_desc
#%{_initrddir}/rapidnat
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/muttrc
%attr(755,root,root) %{_sysconfdir}/rc.sysinit_diskless
%attr(755,root,root) %{_bindir}/dhcpnode
%attr(755,root,root) %{_bindir}/setup_test_user
#%attr(755,root,root) %{_initrddir}/pbs_mom
#%attr(755,root,root) %{_initrddir}/pbs_server
#%attr(755,root,root) %{_initrddir}/pbs_sched
#%attr(755,root,root) %{_initrddir}/pbs
%attr(644,root,root) /var/spool/pbs/pbs_config.sample
%{perl_vendorlib}/cluster_xconfig.pm
%{perl_vendorlib}/maui_cluster.pm
%{perl_vendorlib}/fs_server.pm
%{perl_vendorlib}/nis_cluster.pm
%{perl_vendorlib}/cluster_fonction_common.pm
%{perl_vendorlib}/cluster_serverconf.pm
%{perl_vendorlib}/cluster_commonconf.pm
%{perl_vendorlib}/install_cluster.pm
%{perl_vendorlib}/add_nodes_to_dhcp_cluster.pm
%{perl_vendorlib}/auto_add_nodes_cluster.pm
%{perl_vendorlib}/dhcpnode_cluster.pm
%{perl_vendorlib}/pxe_server_cluster.pm
%{perl_vendorlib}/auto_remove_nodes_cluster.pm
%{perl_vendorlib}/dns_cluster.pm
%{perl_vendorlib}/server_cluster.pm
%{perl_vendorlib}/cluster_set_admin.pm
%{perl_vendorlib}/cluster_set_compute.pm
%{perl_vendorlib}/wakeup_node_cluster.pm
%{perl_vendorlib}/user_nis_cluster.pm
%{perl_vendorlib}/hdlists_server_cluster.pm
%{perl_vendorlib}/postfix_cluster.pm
%{perl_vendorlib}/dhcpdconf_server_cluster.pm
%{perl_vendorlib}/pbs_cluster.pm
%attr(755,root,root) %{_bindir}/prepare_diskless_image
%attr(755,root,root) %{_bindir}/setup_xconfig.pl
%attr(755,root,root) %{_bindir}/setup_pbs.pl
%attr(755,root,root) %{_sbindir}/setup_auto_cluster
%attr(755,root,root) %{_bindir}/setup_hdlists_server.pl
%attr(755,root,root) %{_bindir}/setup_add_nodes_to_dhcp.pl
%attr(755,root,root) %{_bindir}/setup_add_node.pl
%attr(755,root,root) %{_bindir}/setup_install_cluster.pl
%attr(755,root,root) %{_bindir}/setup_dns.pl
%attr(755,root,root) %{_bindir}/setup_server_cluster.pl
%attr(755,root,root) %{_bindir}/setup_recup_cpus.pl
%attr(755,root,root) %{_bindir}/setup_nis.pl
%attr(755,root,root) %{_bindir}/setup_auto_remove_nodes.pl
%attr(755,root,root) %{_sbindir}/deluserNis.pl
%attr(755,root,root) %{_bindir}/wakeup_node.pl
%attr(755,root,root) %{_bindir}/setup_maui.pl
%attr(755,root,root) %{_bindir}/setup_auto_add_nodes.pl
%attr(755,root,root) %{_sbindir}/adduserNis.pl
%attr(755,root,root) %{_bindir}/setup_postfix.pl
%attr(755,root,root) %{_bindir}/setup_admin.pl
%attr(755,root,root) %{_bindir}/setup_compute.pl
%attr(755,root,root) %{_bindir}/setup_pxe_server.pl
%attr(755,root,root) %{_bindir}/setup_dhcpdconf_server.pl
%attr(755,root,root) %{_bindir}/update_cfg_after_ar_node.pl
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/clusterserver.conf
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/dhcpd.conf.pxe.single
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/dhcpd.conf.cluster


