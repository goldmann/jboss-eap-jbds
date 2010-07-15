%define eap_major_version 5.0

Summary:            JBoss Enterprise Application Platform
Name:               jboss-eap
Version:            5.0.1
Release:            20100715
License:            LGPL
Group:              Applications/System
BuildArch:          noarch
Source0:            %{name}-%{version}.zip
Source2:            %{name}.init

# JBoss EAP patches
Source10:           JBPAPP-4122.zip
Source11:           JBPAPP-4038.zip
Source12:           JBPAPP-4302.zip
Source13:           JBPAPP-4220.zip
Source14:           JBPAPP-4196.zip
Source15:           JBPAPP-4350.zip
Source16:           JBPAPP-4479.zip
Source17:           JBPAPP-4496.zip

Requires(build):    unzip
Requires:           shadow-utils
Requires:           coreutils curl
Requires:           java-1.6.0-openjdk
Requires:           initscripts
Requires(post):     /sbin/chkconfig
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define runuser %{name}
%define __jar_repack %{nil}

%description
JBoss Enterprise Application Platform (JBoss EAP) is the market-leading, open source enterprise Java platform for developing and deploying innovative and scalable Java applications. Combining a robust, yet flexible, architecture with an open source software license, JBoss EAP has become the most popular middleware system for developers, independent software vendors (ISVs), and enterprises alike. 

%prep
rm -rf %{name}-%{eap_major_version}
unzip -q %{SOURCE0}

# Patches BEGIN ----------------------------
rm -rf JBPAPP-4122
unzip -q %{SOURCE10}

rm -rf JBPAPP-4038
unzip -q %{SOURCE11}

rm -rf JBPAPP-4302
unzip -q %{SOURCE12}

rm -rf JBPAPP-4220
unzip -q %{SOURCE13}

rm -rf JBPAPP-4196
unzip -q %{SOURCE14}

rm -rf JBPAPP-4350
unzip -q %{SOURCE15}

rm -rf JBPAPP-4479
unzip -q %{SOURCE16}

rm -rf JBPAPP-4496
unzip -q %{SOURCE17}
# Patches END ----------------------------

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}-%{version}
cp -R %{name}-%{eap_major_version}/* $RPM_BUILD_ROOT/opt/%{name}-%{version}

# it caused adding bad requires for package
rm -rf $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/bin/jboss_init_solaris.sh

# Patches BEGIN ----------------------------
cd JBPAPP-4122
tar -xf jboss-ejb3-core-signed.tgz
cp jboss-ejb3-core.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/common/lib/jboss-ejb3-core.jar 
cd ..

cd JBPAPP-4038
tar -xf hibernate-core-3.3.2.GA_CP01-signed.tgz
for path in jboss-as/client/hibernate-core.jar jboss-as/common/lib/hibernate-core.jar seam/lib/hibernate-core.jar
do
   cp hibernate-core-3.3.2.GA_CP01.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/$path
done
cd ..

cd JBPAPP-4302
tar -xf hibernate-core-3.3.2.GA_CP01-signed.tgz
cp hibernate-core-3.3.2.GA_CP01.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/common/lib/hibernate-core.jar
cd ..

cd JBPAPP-4220
tar -xf jboss-mdr-signed.tgz
cp jboss-mdr.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/lib/jboss-mdr.jar
cd ..

cd JBPAPP-4196
tar -xf JBPAPP-4196-signed.tgz
cp jboss-messaging.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/common/lib/jboss-messaging.jar
cp jboss-messaging-client.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/client/jboss-messaging-client.jar

profiles=( all default production standard )

for profile in ${profiles[@]} ; do
  cp *-persistence-service.xml $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/server/${profile}/deploy/messaging/ 
done
cd ..

cd JBPAPP-4350
tar -xf JBPAPP-4350-signed.tgz
cp *.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/lib/ 
cd ..

cd JBPAPP-4479
tar -xf JBPAPP-4479-signed.tgz
cp JBPAPP-4479/jbosssx-as-client.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/client/jbosssx-as-client.jar
cp JBPAPP-4479/jbosssx-server.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/common/lib/jbosssx-server.jar
cd ..

cd JBPAPP-4496
tar -xf JBPAPP-4496-signed.tgz
cp jboss-aop.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/lib/jboss-aop.jar
cp jboss-messaging.jar $RPM_BUILD_ROOT/opt/%{name}-%{version}/jboss-as/common/lib/jboss-messaging.jar
cd ..
# Patches END ----------------------------

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "JBOSS_EAP_VERSION=%{version}"                   > $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "JBOSS_EAP_HOME=/opt/%{name}-%{version}"        >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "JBOSS_HOME=/opt/%{name}-%{version}/jboss-as"   >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

chmod 600 $RPM_BUILD_ROOT/etc/sysconfig/%{name} 

%clean
rm -Rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r %{name} 2>/dev/null || :
/usr/sbin/useradd -c "JBoss EAP" -r -s /bin/bash -d /opt/%{name}-%{version} -g %{name} %{name} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} on

%files
%defattr(-,%{name},%{name})
/

%changelog
* Tue Jul 15 2010 Marek Goldmann 5.0.1-20100715
- Initial release
