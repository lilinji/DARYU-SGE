#!/usr/bin/python
# -*- encoding: utf8 -*-

import re
import pexpect
ipAddress = 'localhost'
# 登录用户名
loginName = 'root'
# 用户名密码
loginPassword = 'Novo2018'
yes = 'yes'
enter = '\r'
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
print child.before
