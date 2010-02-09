%define name clusterscripts
%define version 3.0
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
Conflicts:	%{name}-server, clusterautosetup-server
Requires:	bind-utils, ypbind, autofs, wget,openssh-clients, openssh-server, tftp, nfs-utils, rsh-server, ntp, ka-deploy-source-node, oar-user, oar-node, usbutils, urpmi-parallel-ka-run, bc, dhcpcd, smartmontools, ganglia-core, taktuk

%description client
script to retrieve information and setup cluster client node from 
a server.

%package server 
Summary:        Script to setup a server node
Group:		System/Cluster
Conflicts:	%{name}-client, clusterautosetup-client
Requires:	bind, bind-utils, nfs-utils, ypserv, yp-tools, ypbind, pxe, tftp-server, xinetd, make, dhcp-server, oar-user, oar-node, oar-server, openssh-server, openssh-clients, ntp, ganglia-gmetad, urpmi-parallel-ka-run, apache, postfix, iptables, ganglia-core, rpm-helper, syslinux, usbutils, bc, php-cli, apache-mod_php, smartmontools, tentakel, ganglia-webfrontend, taktuk, fping
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
perl -pi -e "s/\-x\s\/sbin\/dhclient/-x \/sbin\/dhclientsux/" /sbin/ifup

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
%{_bindir}/fdisk_to_desc
%{perl_vendorlib}/ka_deploy_cluster.pm
%{perl_vendorlib}/client_cluster.pm
%{perl_vendorlib}/fs_client.pm
%{perl_vendorlib}/cluster_commonconf.pm
%{perl_vendorlib}/cluster_clientconf.pm
%{perl_vendorlib}/cluster_fonction_common.pm
%{_bindir}/ib-burn-firmware.pl

%files server
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/ib-burn-firmware.pl
%attr(755,root,root) %{_bindir}/ib-cluster-configurator.pl
%attr(755,root,root) %{_bindir}/rapidnat
%attr(755,root,root) %{_bindir}/sauvegarde
%attr(755,root,root) %{_bindir}/fdisk_to_desc
%attr(755,root,root) %{_bindir}/setup_xconfig.pl
#%{_initrddir}/rapidnat
%attr(755,root,root) %{_sysconfdir}/rc.sysinit_diskless
%attr(755,root,root) %{_sysconfdir}/muttrc
%attr(755,root,root) %{_bindir}/dhcpnode
%attr(755,root,root) %{_bindir}/setup_test_user
%attr(644,root,root) /var/spool/pbs/pbs_config.sample
%{perl_vendorlib}/cluster_xconfig.pm
%{perl_vendorlib}/fs_server.pm
%{perl_vendorlib}/nis_cluster.pm
%{perl_vendorlib}/cluster_fonction_common.pm
%{perl_vendorlib}/cluster_serverconf.pm
%{perl_vendorlib}/cluster_commonconf.pm
%{perl_vendorlib}/install_cluster.pm
%{perl_vendorlib}/add_nodes_to_dhcp_cluster.pm
%{perl_vendorlib}/auto_add_nodes_cluster.pm
%{perl_vendorlib}/dhcpnode_cluster.pm
%{perl_vendorlib}/maui_cluster.pm
%{perl_vendorlib}/pxe_server_cluster.pm
%{perl_vendorlib}/auto_remove_nodes_cluster.pm
%{perl_vendorlib}/dns_cluster.pm
%{perl_vendorlib}/server_cluster.pm
%{perl_vendorlib}/cluster_set_admin.pm
%{perl_vendorlib}/cluster_set_compute.pm
%{perl_vendorlib}/wakeup_node_cluster.pm
%{perl_vendorlib}/user_nis_cluster.pm
%{perl_vendorlib}/postfix_cluster.pm
%{perl_vendorlib}/dhcpdconf_server_cluster.pm
%{perl_vendorlib}/pbs_cluster.pm
%attr(755,root,root) %{_bindir}/prepare_diskless_image
%attr(755,root,root) %{_bindir}/setup_pbs.pl
%attr(755,root,root) %{_sbindir}/setup_auto_cluster
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
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/clusternode.conf
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/dhcpd.conf.pxe.single
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/dhcpd.conf.cluster


%changelog
