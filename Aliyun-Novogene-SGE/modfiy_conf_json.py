#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Script Name    	: dir_test.py
# Author         	: lilinji
# Created        	: 22th November 2017
# Last Modified         : 
# Version            	: 1.0
# Modifications         :
# Description        	: Tests to see if the directory testdir exists, if not it will create the directory for you
import sys
import os
import argparse
import json
import time
import bisect
import re
#import encoding
################传参程序
print "程序名：", sys.argv[0]
########################
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-c','--compute', type=str, default='compute', help="set compute name")
parser.add_argument('-f','--fsname', type=str, default='gridengine', help="set install sge path")
parser.add_argument('-g','--mdir', type=str, default='https://novo-it.oss-cn-beijing.aliyuncs.com/ge2011.11.tar.gz', help="down SGE package ")
parser.add_argument('-k','--diskcnt', type=int, default=1, help="for mark install")
parser.add_argument('-m','--master', type=str, default = 'master')
parser.add_argument('-p','--passwd', type=str, default='Novo2018', help="set passwd for node")
help = 'python modfiy_conf_json.py -c compute -f gridengine -k 1 -m master -p Novo2017' 
parser.add_argument('-v','--version', type=str, help=help)
args = parser.parse_args() #参数赋值
if args.version:
         print "verbosity turned on"
os.getcwd()
#print os.getcwd()
#############TIME 
s = time.ctime()
print (s)
dict1={}
dict2=[]
################
with open('host', 'r') as f1:
         #     list3 = list3.strip('\n')
     list3 = f1.readlines()
     for line in list3:
          line = line.strip()
          if line != '':
                line4 = re.split('\s+', line, re.M | re.I)  # split 空格 输出数组行
                dict2.append(line4[0])  # 放到数组
                dict1[line4[0]] = line4[0]  # 字典 不推荐
################Add json
head = '''{
  "master": {
        "skip": true,'''
tail ='''	        ]                           
     },'''

name = '''  "compute": {
        "skip": false,
        "nasname": "Nas",'''
code = '''            ],
        "hostindex": 1,
                "packages": [
                 "http://3811.oss-cn-beijing.aliyuncs.com/hpc-sdk/python-mpmath-0.19-2.el7.noarch.rpm"
                ]
     }
}'''

#####################
INSTALL = '''#!/usr/bin/python
# -*- encoding: utf8 -*-

import re
import pexpect
ipAddress = 'localhost'
# 登录用户名
loginName = 'root'
# 用户名密码'''
#aloginPassword = 'Novo2017'
INSTALL1 = '''yes = 'yes'
enter = '\\r'
child = pexpect.spawn('ssh -l %s %s'%(loginName, ipAddress))
#no)? yesa
child.expect('\)?')
child.sendline(yes)
child.expect('password:')
child.sendline(loginPassword)
child.expect('#')
child.sendline('cd /opt/gridengine')
child.expect('#')
child.sendline('./install_qmaster')
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#print child.before
child.expect(">>")
child.sendline(enter)
#print child.before
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#print child.before
child.expect(">>")
child.sendline(enter)
#print child.before
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#print child.before
child.expect("\) >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#print child.before
#child.sendline(enter)
child.expect("Enter cell name \[default\] >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Do you want to select another cell name? (y/n) [y] >>
child.expect("to use default \[p6444\] >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Enter a qmaster spool directory [/opt/gridengine/ge2011.11/default/spool/qmaster] >>
child.expect("qmaster\] >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Are you going to install Windows Execution Hosts? (y/n) [n] >>
child.expect("\(y/n\) \[n\] >>")
child.sendline(enter)
child.expect("\(y/n\) \[y\] >>")
child.sendline(enter)
#and set the file permissions of your distribution (enter: y) (y/n) [y] >>
#We do not verify file permissions. Hit <RETURN> to continue
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Are all hosts of your cluster in a single DNS domain (y/n) [y] >>
child.expect("\(y/n\) \[y\] >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Do you want to enable the JMX MBean server (y/n) [n] >>
child.expect("\(y/n\) \[n\] >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Please choose a spooling method (berkeleydb|classic) [berkeleydb] >>
child.expect("\[berkeleydb\] >>")
child.sendline(enter)
#Default: [/opt/gridengine/ge2011.11/default/spool/spooldb] >>
child.expect("spooldb\] >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#range [20000-20100] >>
child.expect("20100\] >>")
child.sendline(enter)
child.expect(">>")
child.sendline(enter)
#Default: [/opt/gridengine/ge2011.11/default/spool] >>
child.expect("spool\] >>")
child.sendline(enter)
#[none] >>
child.expect("\[none\] >>")
child.sendline(enter)
child.expect("\(y/n\) \[n\] >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#start qmaster at machine boot (y/n) [y] >>
child.expect("\(y/n\) \[y\] >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Do you want to use a file which contains the list of hosts (y/n) [n] >>
child.expect("\(y/n\) \[n\] >>")
child.sendline(enter)
#Host(s):
child.expect("\(s\):")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Do you want to add your shadow host(s) now? (y/n) [y] >>
child.expect("\(y/n\) \[y\] >>")
child.sendline(enter)
#Do you want to use a file which contains the list of hosts (y/n) [n] >>
child.expect("\(y/n\) \[n\] >>")
child.sendline(enter)
#Host(s):
child.expect("\(s\):")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
child.expect("Hit <RETURN> to continue >>")
child.sendline(enter)
#Default configuration is [1] >>
child.expect("Default configuration is \[1\] >>")
child.sendline(enter)
#Do you agree? (y/n) [y] >>
child.expect("\(y/n\) \[y\] >>")
child.sendline(enter)
#Hit <RETURN> to see where Grid Engine logs messages >>
child.expect("messages >>")
child.sendline(enter)
#Do you want to see previous screen about using Grid Engine again (y/n) [n] >>
child.expect("\(y/n\) \[n\] >>")
child.sendline(enter)
#Please hit <RETURN> >>
child.expect(">>")
child.sendline(enter)
########################################
child.expect("#")
child.sendline('ssh-keygen -t rsa')
child.sendline(enter)
child.expect("\):")
child.sendline(enter)
child.expect("\):")
child.sendline(enter)
child.expect("again:")
child.sendline(enter)
print child.before'''
#######################################Add host in json
def WriteToFileUsePrint():
    saveout = sys.stdout	
    fd = open('hpc-sge.json', 'w')
    sys.stdout = fd
    print head
    print '       "fsname": "'+"/opt/"+args.fsname+"\","
    print '       "hostname": "'+args.master+"\""+","
    print '       "diskcnt":'+bytes(args.diskcnt)+","
    print ' 	  	"hosts": ["'+dict2[0]+"\""+"],"
    print '       "hostindex":'+" 1,"
    print '                "packages":'+" ["
    print '       		"'+args.mdir+"\""
    print tail 
 #### conf compute    
    print name
    print '       "hostname": "'+args.compute+"\""+","
    print '       "passwd": "'+args.passwd+"\""+","
    print '       "diskcnt":'+bytes(args.diskcnt)+","
    print '	  "hosts": ['
    
 #### list compute  node    
    for n in dict2:
	if (n is ((dict2[-1]))):
		pass
	elif (n is (dict2[0])):
		pass
	else:    
        	print  '             '+"\""+n+"\""+","
    print '             '+"\""+dict2[-1]+"\""
    print code
    sys.stdout = saveout
    fd.close()
def WriteToFileUsePrint1():
    saveout = sys.stdout
    fd = open('install_sge.py', 'w')
    sys.stdout = fd
    print INSTALL
    print 'loginPassword = '+"'"+args.passwd+"'"
    print INSTALL1
    sys.stdout = saveout
    fd.close()

##################################声明
if __name__ == '__main__':
    print '''hello word'''
WriteToFileUsePrint()
WriteToFileUsePrint1()
os.system('chmod 755 hpc-sge.json')
os.system('chmod 755 install_sge.py')
