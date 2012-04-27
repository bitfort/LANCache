# Victor Bittorf (bittorf@cs.wisc.edu)
# David Capel (capel@cs.wisc.edu)
"""
Hanldes configuration files
"""


import json


_NET_CONF_FILE = 'netconf.json'


class ConfigError(Exception): pass


def _load_json(filename):
  """ Load json from a file on disk OR DIE """
  with open(filename) as f:
    j = json.load(f) 
    return j
  raise ConfigError('File not found: {0}'.format(filename))


class Conf(object):
  def __init__(self, js):
    self.grand_master = (js['grand_master']['host'], 
                         int(js['grand_master']['port']))
    self.local_master = (js['local_master']['host'], 
                         int(js['local_master']['port']))
    self.port = js['port']


def load_conf(filename=_NET_CONF_FILE):
  j = _load_json(filename)
  return Conf(j)
