storm-redhat7-rpm
---------
A set of scripts to package Apache Storm into an rpm.
Requires CentOS/RedHat 7.

Setup
-----
    sudo yum install make rpmdevtools

Building
--------
    make rpm

Resulting RPM will be avaliable at $(shell pwd)/x86_64

Installing and operating
------------------------
    sudo yum install apache-storm*.rpm

    sudo systemctl start storm-nimbus
    sudo systemctl enable storm-nimbus

    sudo systemctl start storm-supervisor
    sudo systemctl enable storm-supervisor

    sudo systemctl start storm-ui
    sudo systemctl enable storm-ui

Storm CLI is available in /opt/storm/bin -> /opt/storm/bin/storm

Default locations
-----------------
binaries: /opt/storm
data:     /var/lib/storm
logs:     /var/log/storm
configs:  /etc/storm/storm_env.sh, /etc/storm/storm.yaml
