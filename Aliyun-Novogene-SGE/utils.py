#!/usr/bin/python
# -*- encoding: utf8 -*-

import subprocess
import logging
import threading
import json
import chardet

logger = logging.getLogger(__name__)

def loadConfig(config_fname):
	with open(config_fname, 'r') as f:
		data = f.read()
		code = chardet.detect(data)['encoding']
		return json.loads(data.decode(code).encode('utf-8'), 'utf-8')

class CmdHelper(object):
	def __init__(self, test_only=False):
		self.test_only = test_only

	def run_local(self, cmd, force=False):
		""" Exception raised if execute command failed. """
		logger.debug('run local cmd: {0}'.format(cmd))
		if self.test_only and not force:
			return ''
		else:
			return subprocess.check_output(cmd, shell=True)

	def run_execpt(self, cmd, check,force=False):
		""" Exception raised if execute command failed. """
		logger.debug('run local cmd: {0}'.format(cmd))
		if self.test_only and not force:
			return ''
		else:
			return subprocess.Popen(cmd,stdin=subprocess.PIPE,shell=True)

#	subprocess.Popen(["python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	def run_remote(self, host, cmd, usr='root', force=False):
		""" Exception raised if execute command failed. """
		logger.debug('[{0}] run cmd: {1}'.format(host, cmd))
		if self.test_only and not force:
			return ''
		else:
			return subprocess.check_output('ssh {0}@{1} "{2}"'.format(usr, host, cmd), shell=True)

class Deferred(object):
	""" This class runs proc(*args) in a background thread,
	join the threads with caller method, return value of proc(*args) is returned.
	"""
	def __init__(self, proc, *args):
		self._proc = proc
		self._args = args
		self._done_cb = None
		self._done_cb_args = None
		self._done = False
		self._ret = None
		self._cond = threading.Condition()
		self._thread = threading.Thread(target=self._wrapper, args=(proc, args))
		self._thread.start()

	def __call__(self):
		self._cond.acquire()
		while not self._done:
			self._cond.wait()
		self._cond.release()
		return self._ret

	def _wrapper(self, proc, args):
		self._cond.acquire()
		try:
			self._ret = proc(*args)
		except:
			raise
		self._done = True
		if self._done_cb is not None and self._done_cb_args is not None:
			self._done_cb(*self._done_cb_args)
		self._cond.notify()
		self._cond.release()

	def set_done_callback(self, proc, *args):
		self._done_cb = proc
		self._done_cb_args = args
if __name__ == '__main__':
    t = loadConfig('novogene.json')
    print(t)
