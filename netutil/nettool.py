"""
Discover information about your network
"""


import subprocess

def get_raw_trace():
  txt = subprocess.check_output(["/usr/sbin/traceroute", '-m', '5', 
                                 'www.google.com'], stderr=subprocess.PIPE)
  lst = []
  for l in txt.split('\n')[:5]:
    stuff = l.split(' ')
    stuff = filter(lambda x: len(x) > 0, stuff)
    num, host, ip = tuple(stuff[:3])
    lst.append((host, ip))
  return lst

