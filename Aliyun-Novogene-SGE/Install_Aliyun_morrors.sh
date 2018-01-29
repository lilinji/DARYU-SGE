#!/bin/bash
INFLAMMATORY=`lsb_release -a |grep 'CentOS Linux release 7'` 
#SWAPPINESS=(sysctl -a | grep vm.swappiness | awk -F ' = ' '{print \$2}')
echo $INFLAMMATORY
if [ "$INFLAMMATORY" ];then 
     echo -e "I have never like anyone who ram a production ready Arch Linux
Anything... install Centos7 Aliyun mirrors...
"
     sleep 3
     wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
     yum clean all && yum makecache 
     yum install -y epel-release
else
     echo -e "I have never meet anyone who ram a production ready Arch Linux 
Anything... And you think  install Centos6 Aliyun mirrors...
"    
     sleep 2
     wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
     yum clean all && yum makecache
     yum install -y epel-release
     sleep 2
fi
