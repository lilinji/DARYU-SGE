#!/usr/bin/env python
#-*- coding: utf-8 -*-
#########################################################################
# File Name: grab_hpc.py
# Author: lilinji
# mail: lilinji@novogene.com
# Created Time: Tue 26 Dec 2017 11:06:33 AM CST
#########################################################################
"""
Aliyun SDK to Help Administrator to modify SGE-HPC Cluster 
author Lilinji In BGI study Python thanks genomics
The Program to with use Master to Add user and to automate Install HPC Cluster 
include __1) SSH_KEY
	__2) INSTALL SGE
	__3) CHANGE QUEUE
	__4) CHANGE GROUP FOR SGE
	__5) INSTALL PACKAGE FOR MASTER 
	__6) INSTALL PACKAGE FOR CLIENT
	__7) INSTALL LOADER CONFIG
	__8) MODIFY  COMPUTX CONFIG  
"""
import re
import os
import sys
import abc
import json
import logging
import shutil
import itertools
import chardet
import unittest
import subprocess

import utils

logger = logging.getLogger(__name__)

def loadConfig(config_fname):
        with open(config_fname, 'r') as f:
                data = f.read()
                code = chardet.detect(data)['encoding']
                return json.loads(data.decode(code).encode('utf-8'), 'utf-8')

############Set /etc/hosts
#GLOBAL_IP = '''127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
#::1         localhost localhost.localdomain localhost6 localhost6.localdomain6'''

class EnvSetupHelper(object):

	# Defines where novogene packages are stored.
	package_dir = '/opt/tmp'

	def __init__(self, config_fname, test_only=False, usr='root', path='opt', host='/etc/hosts'):
		self.config_fname = config_fname
		self.test_only = test_only
		self.usr = usr
		self.path =path
		self.host =host
		self.cmd_helper = utils.CmdHelper(test_only)
		self.config = loadConfig(config_fname)

	def iter_roles(self, skip_enabled=True, roles=None):
		for r, v in self.config.iteritems():
			if roles is not None and r not in roles:
				continue
			if skip_enabled and v.get('skip', False):
				continue
			yield r, v

	def install_ssh_key(self):
		""" Install ssh key to remote machines. """
		# Check if local identity is present, if not, generate one.
#		getpasswd = list(itertools.chain([v.get('passwd') if not v.get('skip', False) else [] for v in self.config.itervalues()]))	     
		#passwd = self.config.get('compute').get('passwd')       
		if not os.path.exists('/{0}/.ssh/id_rsa.pub'.format(self.usr)):
			self.cmd_helper.run_local('ssh-keygen  -t rsa')
		# Install ssh key to all hosts.
		allhosts = [v.get('hosts') if not v.get('skip', False) else [] for v in self.config.itervalues()]
                for h in list(itertools.chain(*allhosts)):
			#sshpass -p 'Novo123' ssh-copy-id -f  -o StrictHostKeyahecking=no root@172.26.233.122
			passwd = self.config.get('compute').get('passwd')
			self.cmd_helper.run_local('sshpass -p \'{0}\' ssh-copy-id -f  -o StrictHostKeyChecking=no {1}@{2}'.format(passwd, self.usr, h))
			#self.cmd_helper.run_local('ssh-copy-id {0}@{1}'.format(self.usr, h))

	def install_master_package(self):
		### 清除 SGE 残渣
		self.cmd_helper.run_local('nohup sh remove_sge.sh >remove_sge.sh.nohup 2>remove_sge.sh.error &')
		self.cmd_helper.run_local('sleep 60')
		### get json list 
		all_hosts = [v.get('hosts') if v.get('skip', False) else [] for v in self.config.itervalues()]
		all_hostname  = [v.get('hostname') if v.get('skip', False) else [] for v in self.config.itervalues()]
		head_ip=list(itertools.chain(*all_hosts))
		n = (head_ip[-1])
		head_name=list(itertools.chain(all_hostname))
		#passwd =list(itertools.chain([v.get('passwd') if not v.get('skip', False) else [] for v in self.config.itervalues()]))
		#passwd[0])
		h= (head_name[-1])
		### change hostname to master
		GLOBAL_IP = '''127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6'''
		self.cmd_helper.run_local('hostnamectl set-hostname {0}'.format(h))
		hostslist=GLOBAL_IP+'\n'+n+'\t'+h+'\n'
		#print  hostslist
		with open(self.host, 'w') as f:
                        f.write(hostslist)
		### echo master to /etc/hosts
	
		
		p = sge_package = self.config.get('master').get('packages')[0]
		d = "/opt/gridengine.tar.gz"
		if not os.path.exists('/{0}'.format(self.path)):
			self.cmd_helper.run_local('mkdir -p /{0}'.format(self.path))
		### download SGE 
		self.cmd_helper.run_local('wget {0} -O {1}'.format(p, d))
		### tar tar.gz
		self.cmd_helper.run_local('cd /{0}&& tar -xf gridengine.tar.gz'.format(self.path))
		### YUM SGE package rpm
		#wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
		self.cmd_helper.run_local('wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo')
		self.cmd_helper.run_local('yum clean all && yum makecache')
		self.cmd_helper.run_local('yum install -y epel-release python-pip')
		self.cmd_helper.run_local('yum install sshpass jemalloc-devel openssl-devel ncurses-devel pam-devel libXmu-devel hwloc-devel hwloc hwloc-libs java-devel javacc ant-junit libdb-devel motif-devel -y')
		self.cmd_helper.run_local('yum install csh ksh xterm db4-utils perl-XML-Simple perl-Env xorg-x11-fonts-ISO8859-1-100dpi xorg-x11-fonts-ISO8859-1-75dpi -y')
		### YUM NIS package rpm
		self.cmd_helper.run_local('yum install nfs-utils ypserv pssh yp-tool -y')
		### pip install python package
		self.cmd_helper.run_local('pip install pexpect')
		self.cmd_helper.run_local('useradd sge')
		self.cmd_helper.run_local('cd /opt/ && mv ge2011.11 gridengine')
		self.cmd_helper.run_local('chown -R sge.sge /opt/gridengine')
		self.cmd_helper.run_local('/usr/bin/python install_sge.py',)
		

	def config_hostname(self):
		""" Configure machine name.
		 - Hostname is formatted: compute-<role>-<hostindex>
                """
		########Read queue conf
		queue_conf='''qname                 all.q
hostlist              @allhosts
seq_no                0
load_thresholds       np_load_avg=1.75
suspend_thresholds    NONE
nsuspend              1
suspend_interval      00:05:00
priority              0
min_cpu_interval      00:05:00
processors            UNDEFINED
qtype                 BATCH INTERACTIVE
ckpt_list             NONE
pe_list               make
rerun                 FALSE
slots                 30
tmpdir                /tmp
shell                 /bin/bash
prolog                NONE
epilog                NONE
shell_start_mode      posix_compliant
starter_method        NONE
suspend_method        NONE
resume_method         NONE
terminate_method      NONE
notify                00:00:60
owner_list            NONE
user_lists            NONE
xuser_lists           NONE
subordinate_list      NONE
complex_values        NONE
projects              NONE
xprojects             NONE
calendar              NONE
initial_state         default
s_rt                  INFINITY
h_rt                  INFINITY
s_cpu                 INFINITY
h_cpu                 INFINITY
s_fsize               INFINITY
h_fsize               INFINITY
s_data                INFINITY
h_data                INFINITY
s_stack               INFINITY
h_stack               INFINITY
s_core                INFINITY
h_core                INFINITY
s_rss                 INFINITY
h_rss                 INFINITY
s_vmem                INFINITY
h_vmem                INFINITY'''
		complex_values = '''qconf -rattr exechost complex_values virtual_free=120G,num_proc=30,h_vmem=120G  '''
		dict_cmd=[]
		#passwd = self.config.get('compute').get('passwd')
		for r, v in self.iter_roles():
			#all_hosts = [v.get('hosts') if not v.get('skip', False) else [] for v in self.config.itervalues()]
			#for i, h in enumerate(v.get('hosts'), v.get('hostindex', 1)):
			k=0
			for n in (v.get('hosts')):
				#print (cmd)
				k +=1
				m = str(k).zfill(3)
				print ('{0}	{1}{2}'.format(n, r, m))
				name = '{0}{1}'.format(r, m)
				cmd = 'echo "{0}     {1}{2}" >> /etc/hosts'.format(n, r, m)
				change_compute_hostname ='ssh {0} \'hostnamectl set-hostname {1}{2}\''.format(n, r, m)
				####Chang Compute Name
				passwd = self.config.get('compute').get('passwd')
				add_admin_exec ='sshpass -p \'{0}\'  ssh localhost \'qconf -ah {1}{2}\''.format(passwd, r, m)
				dict_cmd.append(name)
				self.cmd_helper.run_local(cmd)
				self.cmd_helper.run_local(change_compute_hostname)
				self.cmd_helper.run_local(add_admin_exec)
		######## Add list shgrphosts
		strs =' '.join([str(_).zfill(3) for _ in (dict_cmd)])
		nodename = strs
		with open('/opt/template_hostgroup', 'w') as f:
                        f.write("group_name    @allhosts"+'\n'+"hostlist    "+nodename)
			f.close()
		with open('/opt/template_queue', 'w') as f:
                        f.write(queue_conf)
                        f.close()
		#qconf -rattr aexechost complex_values
		with open('/opt/complex_values.sh', 'w') as f:
			for _ in dict_cmd:
				f.write(complex_values+str(_).zfill(3)+'\n')
			f.close()
		#print (queue_conf)
		#print (nodename)

	def prepare_packages(self):
		""" Download packages and upload to machines.
		The packages are stored in /opt/tmp directory.
		"""
		
		if not os.path.exists(self.package_dir):
			os.mkdir(self.package_dir)
		for r in self.config:
			if not os.path.exists('{0}/{1}'.format(self.package_dir, r)):
				os.mkdir('{0}/{1}'.format(self.package_dir, r))
		
		def do_download(r, p):
			d = '{0}/{1}'.format(self.package_dir, r)
			n = p.split('/')[-1]
			if os.path.exists('{0}/{1}'.format(d, n)):
				return
			#### down Package loaclhost
			self.cmd_helper.run_local('wget {0} -O {1}/{2}'.format(p, d, n))
			logger.debug('Package {0}/{1} downloaded'.format(d, n))

		def do_upload(h, r):
			d = '{0}/{1}'.format(self.package_dir, r)
			#opt_dir = '/opt/gridengine'
			opt_dir = self.config.get('master').get('fsname')
			self.cmd_helper.run_remote(h, 'mkdir -p {0}'.format(d), self.usr)
			self.cmd_helper.run_remote(h, 'mkdir -p {0}'.format(opt_dir), self.usr)
			
			#### Install RPM Packsge
			self.cmd_helper.run_local(
			        'scp {0}/* {1}@{2}:{3}/'.format(d, self.usr, h, d))
			### Scp /etc/hosts to compute
			self.cmd_helper.run_local('scp /etc/hosts  {0}@{1}:/etc/'.format(self.usr, h))
			self.cmd_helper.run_local('scp /etc/passwd  {0}@{1}:/etc/'.format(self.usr, h))
			self.cmd_helper.run_local('scp /etc/group  {0}@{1}:/etc/'.format(self.usr, h))
			### Scp SGE to Compute
			self.cmd_helper.run_local('scp -rp {0}/* {1}@{2}:{3}/'.format(opt_dir, self.usr, h, opt_dir))
			logger.debug('Packages {0} uploaded to {1}'.format(r, h))

		# Download packages
		ds = []
		for r, v in self.iter_roles():
			for p in v.get('packages'):
				d = utils.Deferred(do_download, r, p)
				ds.append(d)
		for d in ds:
			d()

		# Upload packages
		ds = []
		for r, v in self.iter_roles():
			for h in v.get('hosts'):
				d = utils.Deferred(do_upload, h, r)
				ds.append(d)
		for d in ds:
			d()

	def install_packages(self):
		""" Install packages.
		 - Assumes prepare_packages has been called.
		 - Install packages according to their order in config file.
		"""
		upgrade_packages = [
                    'libcom_err',
                    'libss',
                    'e2fsprogs-libs',
                ]

		def should_upgrade(n):
			return any(filter(lambda x: n.find(x) == 0, upgrade_packages))

		def do_install(h, r, packages):
			d = '{0}/{1}'.format(self.package_dir, r)
			# Package install ordera must be guarenteed.
			self.cmd_helper.run_remote(h, 'yum install yum install sshpass jemalloc-devel openssl-devel ncurses-devel pam-devel libXmu-devel hwloc-devel hwloc hwloc-libs java-devel javacc ant-junit libdb-devel javacc ant-junit libdb-devel motif-devel nfs-utils ypserv yp-tool -y')
			self.cmd_helper.run_remote(h,'chown -R sge.sge /opt/gridengine')
			#kill -9 `pidof sge_execd`
			#self.cmd_helper.run_remote(h,'kill -9 `pidof sge_execd`')
			#pidof sge_execd ||
			self.cmd_helper.run_remote(h,'pidof sge_execd || /opt/gridengine/default/common/sgeexecd')
                        self.cmd_helper.run_remote(h,'cp /opt/gridengine/default/common/settings.sh /etc/profile.d/sge.sh')
			for p in packages:
				n = p.split('/')[-1]
				try:
					if should_upgrade(n):
						self.cmd_helper.run_remote(
						        h, 'rpm -Uvh --nodeps --force {0}/{1}'.format(d, n))
					else:
						self.cmd_helper.run_remote(
						        h, 'yum --nogpgcheck -y install {0}/{1}'.format(d, n))
				except Exception as e:
					logger.error('do_install exception={0}'.format(str(e)))
			

		def install_done(h, r):
			logger.debug('Package install done: host={0}, role={1}'.format(h, r))

		ds = []
		for r, v in self.iter_roles():
			for h in v.get('hosts'):
				d = utils.Deferred(do_install, h, r, v.get('packages'))
				d.set_done_callback(install_done, h, r)
				ds.append(d)
		for d in ds:
			d()

	upcore_config = ['sysctl -w sunrpc.tcp_max_slot_table_entries=128','sysctl -w sunrpc.tcp_slot_table_entries=128']

	def _do_upcore_conf(self, h):
		""" Generate upcore.conf. """
		self.cmd_helper.run_remote(h, 'rm -f /etc/modprobe.d/upcore.conf')
		for l in self.upcore_config:
			self.cmd_helper.run_remote(
			        h, 'echo "{0}" >>/etc/modprobe.d/upcore.conf'.format(l))
###################################################
	#def _do_upcore_conf(self, h):
        #      """ Generate upcore.conf. """
        #        self.cmd_helper.run_remote(h, 'rm -f /etc/modprobe.d/upcore.conf')
        #        for l in self.upcore_config:
        #                self.cmd_helper.run_remote(
        #                        h, 'echo "{0}" >>/etc/modprobe.d/upcore.conf'.format(l))
##################################################
	def do_upcore_conf(self):
		for r, v in self.iter_roles():
			for h in v.get('hosts'):
				# novogene conf
				self._do_upcore_conf(h)
		#####Add host group modify all.q
		passwd = self.config.get('compute').get('passwd')
		hostname = self.config.get('master').get('hostname')
                add_mhgrp ='sshpass -p \'{0}\'  ssh localhost \'qconf -Mhgrp /opt/template_hostgroup\''.format(passwd)
		modify_queue ='sshpass -p \'{0}\'  ssh localhost \'qconf -Mq /opt/template_queue\''.format(passwd)
		modify_complex ='sshpass -p \'{0}\'  ssh localhost \'sh /opt/complex_values.sh\''.format(passwd)
		modify_submit ='sshpass -p \'{0}\'  ssh localhost \'qconf -as {1}\''.format(passwd, hostname)
		self.cmd_helper.run_local(add_mhgrp)
		self.cmd_helper.run_local(modify_queue)
		self.cmd_helper.run_local(modify_submit)
		###################

	def _install_common_software(self, h):
		self.cmd_helper.run_local(h, 'yum install -y nfs-utils screen iftop pssh autofs ypserv ypbind yp-tool')
		# mount nas as a share folder between admin/client/mds/oss,
		# to share mpirun and IOR.
		if nas is not None:
			self.cmd_helper.run_local(h, 'mkdir -p /Nas')
			try:
				res = self.cmd_helper.run_local(
				        h, 'cat /etc/rc.local | grep nfs | grep {0}'.format(nas.split('.')[0]))
			except:
				res = ''
			if (res == ''):
				self.cmd_helper.run_local(
				        h, 'echo "mount -t nfs -o vers=3 {0}:/ /Nas" >>/etc/rc.local'.format(nas))
				self.cmd_helper.run_local(h, 'chmod +x /etc/rc.local')

	def init_novogene_server(self):
		""" Initialize SGE  servers.
		 - modprobe upcore
 		 - hostnamectl set-hostname master --all
		 - wget sge2011.tar.gz 
		 - mkdir -p /opt/gridengine && user add sge
		 - yum install 'jemalloc-devel openssl-devel ncurses-devel pam-devel libXmu-devel hwloc-devel hwloc hwloc-libs java-devel javacc ant-junit libdb-devel motif-devel csh ksh xterm db4-utils perl-XML-Simple perl-Env xorg-x11-fonts-ISO8859-1-100dpi xorg-x11-fonts-ISO8859-1-75dpi'
                 - install SGE for execpt 
                 - cp seting.sh /etc/profile.d
		"""
		mgs_ip = self.config.get('master').get('hosts')[0]
		passwd = self.config.get('compute').get('passwd')
		sge_package = self.config.get('master').get('packages')[0]
		print (passwd)
		if os.path.exists('/opt/gridengine/default/common/settings.sh'):
			### cp sge_profile /etc
			self.cmd_helper.run_local('cp /opt/gridengine/default/common/settings.sh /etc/profile.d/sge.sh')
			self.cmd_helper.run_local('chmod 755 /etc/profile.d/sge.sh')
			self.cmd_helper.run_local('source /etc/profile.d/sge.sh')
			#self.cmd_helper.run_local('qhost', env='/etc/profile.d/sge.sh')
		#print (mgs_ip)
		comp_trans = {
			'master': 'master',
			'compute': 'compute'
		}
		a2z = "abcdefghijklmnopqrstuvwxyz"


	def gen_host_file(self):
		fname = self.config_fname.split('.')[0]
		fname_all = '_templates/{0}.hosts.all'.format(fname)
		hosts_all = []
		for r, v in self.iter_roles(False):
			hosts = v.get('hosts')
			#print (hosts)
			hosts_all += hosts
			fname_this = '_templates/{0}.hosts.{1}'.format(fname, r)
			with open(fname_this, 'w') as f:
				f.write('\n'.join(hosts))
		with open(fname_all, 'w') as f:
			f.write('\n'.join(hosts_all))


#helper.install_master_package()
#helper.install_ssh_key()
#helper.init_novogene_server()
#helper.config_hostname()
#helper.prepare_packages()
#helper.install_packages()
#helper.do_upcore_conf()
#helper.gen_host_file()
###### Test Pyton def 
class EnvSetupTest(unittest.TestCase):
	def setUp(self):
		self.env_helper = EnvSetupHelper('hpc-sge.json', test_only=False)

	@unittest.skip('passed')
        def test_install_master(self):
                self.env_helper.install_master_package()
	
	@unittest.skip('passed')
	def test_install_novogene(self):
		self.env_helper.init_novogene_server()
	
	@unittest.skip('passed')
        def test_hostname(self):
                self.env_helper.config_hostname()

	@unittest.skip('passed')
	def test_prepare_packages(self):
		self.env_helper.prepare_packages()

	@unittest.skip('passed')
	def test_install_package(self):
		self.env_helper.install_package()

	@unittest.skip('passed')
	def test_do_upcore(self):
		self.env_helper.do_upcore_conf()

	@unittest.skip('passed')
	def test_gen_host_file(self):
		self.env_helper.gen_host_file()

        @unittest.skip('passed')
        def test_iter_hosts(self):
                self.env_helper.iter_hosts()


if __name__ == '__main__':

	logging.basicConfig(level=logging.DEBUG,
                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                     datefmt='%a, %d %b %Y %H:%M:%S',
                     filename='envsetup.log',
                     filemode='w')
	unittest.main()
