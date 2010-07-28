%define eap_profile default
%define eap_name jboss-eap
%define postgresql_connector_version 8.4-701

Summary:            PostgreSQL support for JBoss EAP
Name:               jboss-eap-local-ds
Version:            5.1.0.Beta
Release:            20100727
License:            LGPL
Group:              Applications/System
BuildArch:          noarch
Source0:            http://jdbc.postgresql.org/download/postgresql-%{postgresql_connector_version}.jdbc4.jar
Source1:            local-ds.xml
Source2:            jboss-eap-postgresql-preconfigure.sh

Requires:           jboss-eap

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define runuser %{name}
%define __jar_repack %{nil}

%description
JBoss Enterprise Application Platform (JBoss EAP) is the market-leading, open source enterprise Java platform for developing and deploying innovative and scalable Java applications. Combining a robust, yet flexible, architecture with an open source software license, JBoss EAP has become the most popular middleware system for developers, independent software vendors (ISVs), and enterprises alike. 

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{eap_name}-%{version}/jboss-as/server/%{eap_profile}/lib/
install -d -m 755 $RPM_BUILD_ROOT/opt/%{eap_name}-%{version}/jboss-as/server/%{eap_profile}/deploy/

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}/
install -m 744 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/%{name}/

install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/opt/%{eap_name}-%{version}/jboss-as/server/%{eap_profile}/lib/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/opt/%{eap_name}-%{version}/jboss-as/server/%{eap_profile}/deploy/

%post
/bin/echo 'host    eap         eap         127.0.0.1/32          md5' >> /var/lib/pgsql/data/pg_hba.conf

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,jboss,jboss)
/

%changelog
* Wed Jul 28 2010 Marek Goldmann 5.0.1-20100727
- Initial release
