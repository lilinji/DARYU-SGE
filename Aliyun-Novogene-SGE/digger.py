#!/usr/bin/python
# -*- encoding: utf8 -*-

import sys
import logging
import argparse

from  grab_hpc  import *


def setupEnv(config_fname, test_only=False):
	helper = EnvSetupHelper(config_fname, test_only)
	helper.install_master_package()
	helper.install_ssh_key()
	helper.init_novogene_server()
	helper.config_hostname()
	helper.prepare_packages()
	helper.install_packages()
	helper.do_upcore_conf()
        helper.gen_host_file()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Deploy Install SGE-HPC Cluster.')
	parser.add_argument('-c', '--config', help='JSON file containing configurations',
			    required=True)
	parser.add_argument('--logfile', help='Log file name', default='deploy.log')
	parser.add_argument('--test', help='Test only', action='store_true', default=False)
	parser.add_argument('--verbose', help='Enable debug info', action='store_true',
			    default=False)
	args = parser.parse_args()
	# Verify arguments
	if not os.path.exists(args.config):
		raise Exception('Config {0} not exists'.format(args.config))

	debug_level = logging.INFO
	if args.verbose:
		debug_level = logging.DEBUG
	logging.basicConfig(level=debug_level,
			 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
			 datefmt='%a, %d %b %Y %H:%M:%S',
			 filename=args.logfile,
			 filemode='w')

	setupEnv(args.config, args.test)
	print('****************')
	print('***** Done *****')
	print('****************')

