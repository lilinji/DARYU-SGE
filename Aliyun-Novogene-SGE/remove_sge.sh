#!/bin/bash
#########################################################################
# File Name: remove_sge.sh
# Author: lilinji
# mail: lilinji@novogene.com
# Created Time: Wed 17 Jan 2018 08:39:04 PM CST
#########################################################################

##remove SGE  rpm 
rpm -aq |grep 'sge' |awk '{print $1}' |while read l; do echo "rpm -e  $l  --nodeps --force "; done |sh
## install locate 
yum install mlocate -y
sudo updatedb
########卸载 NFS 网络硬盘
mount |grep 'type nfs (' |awk '{print $3}' |while read l; do echo "umount -l $l &"; done |sh
######find SGE residue
locate sge |egrep -v  '/root|sgen|kernels|msgexec|selinux|systemtap|msg' |while read l; do echo "rm -rf $l &"; done |sh

locate gridengine |egrep -v  '/root|sgen|kernels|msgexec|selinux|systemtap|msg' |while read l; do echo "rm -rf $l &"; done |sh

#### replace 替换 /etc/hosts
unalias cp

cp -f hosts  /etc/hosts
#######删除 Key
rm -rf /root/.ssh/authorized_keys
rm -rf /root/.ssh/id_rsa
rm -rf /root/.ssh/id_rsa.pub
rm -rf /root/.ssh/known_hosts

rm -rf /opt/*
#######删除 SGE 账户

SGE_ID=`cat /etc/passwd |grep 'sge'`

if [ "$SGE_ID" ] 
then
        userdel -r sge
else 
        echo "nihao!!!"
fi
######杀掉 SGE 进程
kill -9 `pidof sge_execd`
kill -9 `pidof sge_qmaster`
